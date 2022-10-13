# deactive plt.show() by 'Agg'
import matplotlib
matplotlib.use('Agg')
print("Hello from TEXT3")
import numpy as np 
import matplotlib.pyplot as plt 
a = np.linspace(0, 10, 100)
b = np.sin(a)
plt.plot(a, b)
plt.savefig('lepythonbot/picture.png')