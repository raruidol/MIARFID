import pandas as pd
import numpy as np
import os
from collections import defaultdict


class ModificaDF:
    # Rutas a ficheros
    csv_data_path = "data/Datasets_Reto_Modelling_UH2019/"
    modelar_data_path = csv_data_path + "Modelar_UH2019.txt"
    estimar_data_path = csv_data_path + "Estimar_UH2019.txt"
    imagenes_data_path = "data/imagenes_inmuebles_haya"
    provincias_data_path = "data/codigos-provincias.csv"

    # Dataframes
    df_modelar = None
    df_estimar = None

    df_modificado_modelar = None
    df_modificado_estimar = None

    df_provincias = None

    def __init__(self):
        # Carga datos en dfs
        self.df_modelar = pd.read_csv(self.modelar_data_path, delimiter="|", dtype={'HY_cod_postal': object})
        self.df_estimar = pd.read_csv(self.estimar_data_path, delimiter="|", dtype={'HY_cod_postal': object})
        self.df_provincias = pd.read_csv(self.provincias_data_path, dtype={'codigo_provincia': object})

        # Crea dfs para modificaciones
        self.df_modificado_modelar = self.df_modelar
        self.df_modificado_estimar = self.df_estimar

        # Sustituye los nan por valor medio de la zona (codigo postal) en variables zonales
        idea_columns = [col for col in self.df_modificado_modelar.columns if 'IDEA' in col]
        for columna in idea_columns:
            self.rellena_por_cod_postal(columna)

        # Sustituye los NaN restantes por valores (media)
        self.sustituir_nan_df()

        # Limpiar df
        self.limpiar_df()

        self.df_modificado_modelar = self.df_modificado_modelar.drop('TARGET', axis=1)

        print("INICIAL: ", self.df_modelar.shape, self.df_estimar.shape)

        # MODIFICACIONES

        # Imágenes
        self.columna_num_fotos()
        self.columna_tiene_fotos()

        # Tipo
        self.tipo_one_hot()

        # Código provincia a one_hot
        self.codigo_provincia_one_hot()

        # Provincia
        self.columna_tiene_provincia()

        # Descripción
        self.columna_tiene_descripcion()

        # Distribución
        self.columna_tiene_distribucion()

        # Certificado energético
        self.columna_tiene_certificado()
        self.cert_energ_one_hot()

        # Precio anterior
        self.precio_anterior()

        # Elimina columnas no numéricas
        self.df_modificado_modelar = self.df_modificado_modelar.select_dtypes(exclude=object)
        self.df_modificado_estimar = self.df_modificado_estimar.select_dtypes(exclude=object)

        # Normaliza las columnas
        self.norm_df()

        # Añade TARGET
        self.df_modificado_modelar['TARGET'] = self.df_modelar['TARGET']

        self.df_modificado_modelar.to_csv('modelar.csv', index=False)
        self.df_modificado_estimar.to_csv('estimar.csv', index=False)

        print("FINAL: ", self.df_modificado_modelar.shape, self.df_modificado_estimar.shape)
        print(list(self.df_modificado_modelar))
        print(list(self.df_modificado_estimar))

    # Normaliza una columna a valores entre 0 y 1
    def norm_column(self, nombre):

        maximo = max(self.df_modificado_modelar[nombre].max(), self.df_modificado_estimar[nombre].max())

        s = self.df_modificado_modelar[nombre]
        self.df_modificado_modelar[nombre] = s / maximo

        s = self.df_modificado_estimar[nombre]
        self.df_modificado_estimar[nombre] = s / maximo

    # Normaliza el dataset a valores entre 0 y 1
    def norm_df(self):
        self.df_modificado_modelar = self.df_modificado_modelar.drop('HY_id', axis=1)
        self.df_modificado_estimar = self.df_modificado_estimar.drop('HY_id', axis=1)

        self.df_modificado_modelar['IDEA_ind_liquidez'] = self.df_modificado_modelar['IDEA_ind_liquidez'] + 1
        self.df_modificado_estimar['IDEA_ind_liquidez'] = self.df_modificado_estimar['IDEA_ind_liquidez'] + 1

        self.df_modificado_modelar = self.df_modificado_modelar * 1
        self.df_modificado_estimar = self.df_modificado_estimar *1
        for column in list(self.df_modificado_modelar):
            self.norm_column(column)

        self.df_modificado_modelar['HY_id'] = self.df_modelar['HY_id']
        self.df_modificado_estimar['HY_id'] = self.df_estimar['HY_id']

    # Añade variable con el número de fotos del anuncio
    def columna_num_fotos(self):

        def num_fotos(row):
            identificador = int(row['HY_id'])
            return diccionario_cuenta_imagenes[identificador]

        diccionario_cuenta_imagenes = defaultdict(int)
        for file in os.scandir(self.imagenes_data_path):
            identificador = int(file.name.split("__")[0])
            diccionario_cuenta_imagenes[identificador] += 1

        self.df_modificado_modelar['num_fotos'] = self.df_modificado_modelar.apply(lambda row: num_fotos(row), axis=1)
        self.df_modificado_estimar['num_fotos'] = self.df_modificado_estimar.apply(lambda row: num_fotos(row), axis=1)

    # Crea la variable booleana que indica si el anuncio tiene fotos
    def columna_tiene_fotos(self):
        self.df_modificado_modelar['tiene_fotos'] = (self.df_modificado_modelar['num_fotos'] > 0).astype(int)
        self.df_modificado_estimar['tiene_fotos'] = (self.df_modificado_estimar['num_fotos'] > 0).astype(int)

    # Convierte la variable provincia a booleano
    def columna_tiene_provincia(self):
        self.df_modificado_modelar['tiene_provincia'] = self.df_modificado_modelar['HY_provincia'].notnull()
        self.df_modificado_modelar['tiene_provincia'] = self.df_modificado_modelar['tiene_provincia']\
            .where(self.df_modificado_modelar['tiene_provincia'] == True)
        self.df_modificado_modelar['tiene_provincia'] = self.df_modificado_modelar['tiene_provincia']\
            .where(self.df_modificado_modelar['tiene_provincia'] == True, 0)

        self.df_modificado_estimar['tiene_provincia'] = self.df_modificado_estimar['HY_provincia'].notnull()
        self.df_modificado_estimar['tiene_provincia'] = self.df_modificado_estimar['tiene_provincia'].where(
            self.df_modificado_estimar['tiene_provincia'] == True)
        self.df_modificado_estimar['tiene_provincia'] = self.df_modificado_estimar['tiene_provincia'].where(
            self.df_modificado_estimar['tiene_provincia'] == True, 0)

    # Convierte la variable descripción a booleano
    def columna_tiene_descripcion(self):
        self.df_modificado_modelar['tiene_descripcion'] = self.df_modificado_modelar['HY_descripcion'].notnull()
        self.df_modificado_modelar['tiene_descripcion'] = self.df_modificado_modelar['tiene_descripcion']\
            .where(self.df_modificado_modelar['tiene_descripcion'] == True)
        self.df_modificado_modelar['tiene_descripcion'] = self.df_modificado_modelar['tiene_descripcion']\
            .where(self.df_modificado_modelar['tiene_descripcion'] == True, 0)

        self.df_modificado_estimar['tiene_descripcion'] = self.df_modificado_estimar['HY_descripcion'].notnull()
        self.df_modificado_estimar['tiene_descripcion'] = self.df_modificado_estimar['tiene_descripcion'].where(
            self.df_modificado_estimar['tiene_descripcion'] == True)
        self.df_modificado_estimar['tiene_descripcion'] = self.df_modificado_estimar['tiene_descripcion'].where(
            self.df_modificado_estimar['tiene_descripcion'] == True, 0)

    # convierte la variable distribución a booleano
    def columna_tiene_distribucion(self):
        self.df_modificado_modelar['tiene_distribucion'] = self.df_modificado_modelar['HY_distribucion'].notnull()
        self.df_modificado_modelar['tiene_distribucion'] = self.df_modificado_modelar['tiene_distribucion']\
            .where(self.df_modificado_modelar['tiene_descripcion'] == True)
        self.df_modificado_modelar['tiene_distribucion'] = self.df_modificado_modelar['tiene_distribucion']\
            .where(self.df_modificado_modelar['tiene_descripcion'] == True, 0)

        self.df_modificado_estimar['tiene_distribucion'] = self.df_modificado_estimar['HY_distribucion'].notnull()
        self.df_modificado_estimar['tiene_distribucion'] = self.df_modificado_estimar['tiene_distribucion'].where(
            self.df_modificado_estimar['tiene_descripcion'] == True)
        self.df_modificado_estimar['tiene_distribucion'] = self.df_modificado_estimar['tiene_distribucion'].where(
            self.df_modificado_estimar['tiene_descripcion'] == True, 0)

    # Convierte la variable certificado a boolean
    def columna_tiene_certificado(self):
        self.df_modificado_modelar['tiene_certificado'] = self.df_modificado_modelar['HY_cert_energ'].notnull()
        self.df_modificado_modelar['tiene_certificado'] = self.df_modificado_modelar['tiene_certificado'].where(
            self.df_modificado_modelar['tiene_descripcion'] == True)
        self.df_modificado_modelar['tiene_certificado'] = self.df_modificado_modelar['tiene_certificado'].where(
            self.df_modificado_modelar['tiene_descripcion'] == True, 0)

        self.df_modificado_estimar['tiene_certificado'] = self.df_modificado_estimar['HY_cert_energ'].notnull()
        self.df_modificado_estimar['tiene_certificado'] = self.df_modificado_estimar['tiene_certificado'].where(
            self.df_modificado_estimar['tiene_certificado'] == True)
        self.df_modificado_estimar['tiene_certificado'] = self.df_modificado_estimar['tiene_certificado'].where(
            self.df_modificado_estimar['tiene_certificado'] == True, 0)

    # Convierte la variable tipo a representación one hot
    def tipo_one_hot(self):
        tipo_list_modelar = set(self.df_modificado_modelar['HY_tipo'].unique())
        tipo_list_estimar = set(self.df_modificado_estimar['HY_tipo'].unique())
        tipo_list = tipo_list_modelar | tipo_list_estimar

        for tipo in tipo_list:
            nombre_columna = 'tipo_' + tipo
            self.df_modificado_modelar[nombre_columna] = self.df_modificado_modelar['HY_tipo'] == tipo
            self.df_modificado_modelar[nombre_columna] = self.df_modificado_modelar[nombre_columna].where(
                self.df_modificado_modelar[nombre_columna] == True)
            self.df_modificado_modelar[nombre_columna] = self.df_modificado_modelar[nombre_columna].where(
                self.df_modificado_modelar[nombre_columna] == True, 0)

            self.df_modificado_estimar[nombre_columna] = self.df_modificado_estimar['HY_tipo'] == tipo
            self.df_modificado_estimar[nombre_columna] = self.df_modificado_estimar[nombre_columna].where(
                self.df_modificado_estimar[nombre_columna] == True)
            self.df_modificado_estimar[nombre_columna] = self.df_modificado_estimar[nombre_columna].where(
                self.df_modificado_estimar[nombre_columna] == True, 0)

    # Convierte la variable codigo postal a codigo provincia y a representación one hot
    def codigo_provincia_one_hot(self):
        def codigo_postal_to_codigo_provincia(row):
            codigo_provincia = row['HY_cod_postal'][:2]
            return codigo_provincia

        self.df_modificado_modelar['codigo_provincia'] = self.df_modificado_modelar.apply(
            lambda row: codigo_postal_to_codigo_provincia(row), axis=1)

        self.df_modificado_estimar['codigo_provincia'] = self.df_modificado_estimar.apply(
            lambda row: codigo_postal_to_codigo_provincia(row), axis=1)



        for index, row in self.df_provincias.iterrows():
            codigo_provincia = row['codigo_provincia']

            nombre_columna = 'provincia_' + codigo_provincia
            self.df_modificado_modelar[nombre_columna] = self.df_modificado_modelar['codigo_provincia'] == codigo_provincia
            self.df_modificado_modelar[nombre_columna] = self.df_modificado_modelar[nombre_columna].where(
                self.df_modificado_modelar[nombre_columna] == True)
            self.df_modificado_modelar[nombre_columna] = self.df_modificado_modelar[nombre_columna].where(
                self.df_modificado_modelar[nombre_columna] == True, 0)

            nombre_columna = 'provincia_' + codigo_provincia
            self.df_modificado_estimar[nombre_columna] = self.df_modificado_estimar['codigo_provincia'] == codigo_provincia
            self.df_modificado_estimar[nombre_columna] = self.df_modificado_estimar[nombre_columna].where(
                self.df_modificado_estimar[nombre_columna] == True)
            self.df_modificado_estimar[nombre_columna] = self.df_modificado_estimar[nombre_columna].where(
                self.df_modificado_estimar[nombre_columna] == True, 0)

    # Convierte la variable certificado energetico a representación one hot
    def cert_energ_one_hot(self):
        set_modelar = set(self.df_modificado_modelar['HY_cert_energ'].unique())
        set_estimar = set(self.df_modificado_estimar['HY_cert_energ'].unique())
        set_cert = set_modelar | set_estimar

        for cert in set_cert:
            nombre_columna = 'cert_' + str(cert)

            self.df_modificado_modelar[nombre_columna] = self.df_modificado_modelar[
                                                             'HY_cert_energ'] == cert
            self.df_modificado_modelar[nombre_columna] = self.df_modificado_modelar[nombre_columna].where(
                self.df_modificado_modelar[nombre_columna] == True)
            self.df_modificado_modelar[nombre_columna] = self.df_modificado_modelar[nombre_columna].where(
                self.df_modificado_modelar[nombre_columna] == True, 0)


            self.df_modificado_estimar[nombre_columna] = self.df_modificado_estimar[
                                                             'HY_cert_energ'] == cert
            self.df_modificado_estimar[nombre_columna] = self.df_modificado_estimar[nombre_columna].where(
                self.df_modificado_estimar[nombre_columna] == True)
            self.df_modificado_estimar[nombre_columna] = self.df_modificado_estimar[nombre_columna].where(
                self.df_modificado_estimar[nombre_columna] == True, 0)

    # Limpieza de outlayers
    def limpiar_df(self):
        clean_data = self.df_modificado_modelar
        #clean_data = clean_data.fillna(0)
        #1


        clean_data = clean_data[clean_data.TARGET <= 160]
        clean_data = clean_data[clean_data.HY_antiguedad <= 2020]  # 1 muestra
        clean_data = clean_data[clean_data.HY_antiguedad >= 1900]  # 5035 muestras
        clean_data = clean_data[clean_data.HY_metros_totales <= 500]  # 400 muestras
        clean_data = clean_data[clean_data.HY_precio <= 1000000]  # 27 muestras
        clean_data = clean_data[clean_data.HY_precio_anterior <= 1000000]  # 22 muestras
        clean_data = clean_data[clean_data.IDEA_price_sale_residential <= 450000]  # 45 muestras
        clean_data = clean_data[clean_data.IDEA_demand_sale_residential >= 45]  # 2458 muestras
        clean_data = clean_data[clean_data.GA_page_views <= 2000]  # 117 muestras
        clean_data = clean_data[clean_data.GA_mean_bounce <= 70]  # 214 muestras
        clean_data = clean_data[clean_data.GA_exit_rate <= 80]  # 270 muestras


        #2
        '''
        clean_data = clean_data[clean_data.TARGET <= 160]
        clean_data = clean_data[clean_data.HY_antiguedad <= 2020] #1 muestra
        #clean_data = clean_data[clean_data.HY_antiguedad >= 1900] #5035 muestras
        clean_data = clean_data[clean_data.HY_metros_totales <= 500] #400 muestras
        clean_data = clean_data[clean_data.HY_precio <= 1000000] #27 muestras
        clean_data = clean_data[clean_data.HY_precio_anterior <= 1000000] #22 muestras
        clean_data = clean_data[clean_data.IDEA_price_sale_residential <= 450000] #45 muestras
        clean_data = clean_data[clean_data.IDEA_demand_sale_residential >= 45] #2458 muestras
        clean_data = clean_data[clean_data.GA_page_views <= 2000] #117 muestras
        clean_data = clean_data[clean_data.GA_mean_bounce <= 70] #214 muestras
        clean_data = clean_data[clean_data.GA_exit_rate <= 80] #270 muestras
        '''

        #3
        '''
        clean_data = clean_data[clean_data.TARGET <= 160]
        clean_data = clean_data[clean_data.HY_antiguedad <= 2020]  # 1 muestra
        # clean_data = clean_data[clean_data.HY_antiguedad >= 1900] #5035 muestras
        clean_data = clean_data[clean_data.HY_metros_totales <= 500]  # 400 muestras
        clean_data = clean_data[clean_data.HY_precio <= 1000000]  # 27 muestras
        clean_data = clean_data[clean_data.HY_precio_anterior <= 1000000]  # 22 muestras
        clean_data = clean_data[clean_data.IDEA_price_sale_residential <= 450000]  # 45 muestras
        # clean_data = clean_data[clean_data.IDEA_demand_sale_residential >= 45] #2458 muestras
        clean_data = clean_data[clean_data.GA_page_views <= 2000]  # 117 muestras
        clean_data = clean_data[clean_data.GA_mean_bounce <= 70]  # 214 muestras
        clean_data = clean_data[clean_data.GA_exit_rate <= 80]  # 270 muestras
        '''

        self.df_modificado_modelar = clean_data

    # Sustituye los valores NaN por la media de la variable
    def sustituir_nan_column(self, columna):

        if (self.df_modificado_modelar[columna].dtypes != object) and (self.df_modificado_modelar[columna].isnull().values.any()):
            pass
            m = self.df_modificado_estimar[columna].mean()
            self.df_modificado_estimar[columna] = self.df_modificado_estimar[columna].fillna(m)

            m = self.df_modificado_estimar[columna].mean()
            self.df_modificado_modelar[columna] = self.df_modificado_modelar[columna].fillna(m)

    def sustituir_nan_df(self):
        for column in list(self.df_modificado_modelar):
            self.sustituir_nan_column(column)

    # Sustituye la columna precio anterior por la resta entre el precio actual y el precio anterior
    # De esta forma eliminamos NaN sin dejar valores en 0
    def precio_anterior(self):
        self.df_modificado_modelar['HY_precio_anterior'].fillna(0)
        self.df_modificado_modelar['HY_precio_anterior'] = self.df_modificado_modelar['HY_precio'] - \
                                                           self.df_modificado_modelar['HY_precio_anterior']

        self.df_modificado_estimar['HY_precio_anterior'].fillna(0)
        self.df_modificado_estimar['HY_precio_anterior'] = self.df_modificado_estimar['HY_precio'] - \
                                                           self.df_modificado_estimar['HY_precio_anterior']

    # Sustituye los valores NaN en las variables que representan medias de las zonas.
    # Se sustituyen por medias de las zonas formadas por el mismo código postal
    def rellena_por_cod_postal(self, columna):
        lista_codigos_modelar =  self.df_modificado_modelar['HY_cod_postal'].unique()
        lista_codigos_estimar = self.df_modificado_estimar['HY_cod_postal'].unique()

        for codigo in lista_codigos_modelar:
            media = self.df_modificado_modelar[self.df_modificado_modelar['HY_cod_postal'] == codigo][columna].mean()
            mask = ((self.df_modificado_modelar['HY_cod_postal'] == codigo) & self.df_modificado_modelar[columna].isnull())
            self.df_modificado_modelar.loc[mask, columna] = media

        for codigo in lista_codigos_estimar:
            media = self.df_modificado_modelar[self.df_modificado_modelar['HY_cod_postal'] == codigo][columna].mean()
            media += self.df_modificado_estimar[self.df_modificado_estimar['HY_cod_postal'] == codigo][columna].mean()
            media /= 2

            mask = ((self.df_modificado_estimar['HY_cod_postal'] == codigo) & self.df_modificado_estimar[columna].isnull())
            self.df_modificado_estimar.loc[mask, columna] = media




modifica = ModificaDF()
