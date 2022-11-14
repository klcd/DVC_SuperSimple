import numpy as np

N = 100
x = np.linspace(0, 2*np.pi,N)

#Data = a*x + b + noise
y = np.random.uniform(-5,5,1)*x+np.random.uniform(-5,5,1)
noise = np.random.normal(0,.7, N)

with open('./data/underlying_data.txt', 'w') as fid:
    np.savetxt(fid, np.stack([x,y]).T)

with open('./data/data.txt', 'w') as fid:
    np.savetxt(fid, np.stack([x,y+noise]).T)