import pandas as pd
import csv

path='/home/hakem/ag/VERTICES.CSV'
df =pd.read_csv(path, header=None,index_col=0)

df.loc[2,3]= 'yes'
# print df.to_csv)


df.to_csv('/home/hakem/ag/myfile.csv', header=None)

