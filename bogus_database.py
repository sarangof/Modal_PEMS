# Imports
import pandas as pd
import numpy  as np
 
# Parameters
n   = 1100
np.random.seed(2016)
 
# Features 
id_ = range(1,n+1)
department = ['Finanzas','Tecnico','Ventas','Gerencia']
dep_sizes  = [5.,30.,10.,2.]
tot = sum(dep_sizes)

# Generate data frame
dep_list = list(np.random.choice(department, n, p=np.divide(dep_sizes,tot)))
pd.DataFrame({'department':dep_list},index=id_).to_csv('Files/bogus_db.csv')