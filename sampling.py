# Imports
import pandas as pd
import numpy  as np
from sklearn.cross_validation import train_test_split

# There will be a way to talk to the interface here... in the future
db = pd.read_csv('Files/bogus_db.csv',usecols=['cedula','department','genero'])

# How to include a measure of error?
pop,sample = train_test_split(np.array(db.cedula),test_size=0.1,stratify=np.array(db.department))

# Return ids of employees.
sample.tofile('cedulas.csv',sep=',')