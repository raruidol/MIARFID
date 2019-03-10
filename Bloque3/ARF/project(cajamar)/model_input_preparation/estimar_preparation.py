import pandas as pd
import numpy as np

# Load the estimar dataset obtained by our data analyser
clean_data = pd.read_csv("data/estimar-local-limpieza-tocha.csv", dtype={'HY_cod_postal': object})

clean_data = clean_data.select_dtypes(exclude=object)


# Select the ID column
id = clean_data[['HY_id']]

# Select the data matrix
important = clean_data.drop('HY_id', axis=1)

# Convert the csv to numpy array
res_id = id.to_numpy()
res_mat = important.to_numpy()

print(res_id.shape)
print(res_mat.shape)

res_mat = np.nan_to_num(res_mat)

np.save('estimar_ids', res_id)
np.save('estimar_matrix', res_mat)