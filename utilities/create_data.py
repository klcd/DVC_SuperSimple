import numpy as np
import pandas as pd

N = 100
x = np.linspace(0, 2*np.pi,N)

#Data = a*x + b + noise
y = np.random.uniform(-5,5,1)*x+np.random.uniform(-5,5,1)
noise = np.random.normal(0,.7, N)

df = pd.DataFrame({'x':x, 'y':y+noise})
df.to_csv('./data/data.csv', index=False)

df = pd.DataFrame({'x':x, 'y':y})
df.to_csv('./data/underlying_data.csv', index=False)