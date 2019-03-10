import pandas as pd
import numpy as np

# Load the modelar dataset obtained by our data analyser
clean_data = pd.read_csv("data/modelar-local-limpieza-tocha.csv", dtype={'HY_cod_postal': object, 'HY_id': object})

clean_data = clean_data.select_dtypes(exclude=object)

# Select the target column
target = clean_data[['TARGET']]

# Select the data matrix
important = clean_data.drop('TARGET', axis=1)

# Convert the csv to numpy arrays for our regression models input
res_mat = important.to_numpy()
print(res_mat.shape)

res_targ = target.to_numpy()
print(res_targ.shape)

res_mat = np.nan_to_num(res_mat)

np.save('clean_data_matrix_local', res_mat)
np.save('clean_data_target_local', res_targ)