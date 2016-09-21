# Imports
import pandas as pd
import numpy  as np
 
# Parameters
n   = 1100
np.random.seed(2016)
 
# Features 
department = ['Finanzas','Tecnico']
cedula = range(1037611242,1037611242+n,1)
genero = ['Mujer','Hombre']
dep_sizes  = [5.,30.,10.,2.]
tot = sum(dep_sizes)

# Generate data frame
dep_list = list(np.random.choice(department, n, p=np.divide(dep_sizes,tot)))
gen_list = list(np.random.choice(genero, n, p = [0.5,0.5]))
pd.DataFrame({'cedula':cedula,'department':dep_list,'genero':gen_list}).to_csv('Files/bogus_db.csv')