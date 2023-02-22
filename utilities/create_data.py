import numpy as np
import pandas as pd
import os

N = 100
x = np.linspace(0, 2*np.pi,N)

#Data = a*x + b + noise
y = 4*x+1
noise = np.random.normal(0,1, N)

home = '/workspaces/DVC_SuperSimple'

df = pd.DataFrame({'x':x, 'y':y+noise})
df.to_csv(os.path.join(home,'initial_data','data.csv'), index=False)

df = pd.DataFrame({'x':x, 'y':y})
df.to_csv(os.path.join(home,'initial_data','underlying_data.csv'), index=False)