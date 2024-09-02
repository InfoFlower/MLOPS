import numpy as np
from matplotlib import pyplot as plt

a=np.array([1,2,3])
b=np.array([4,5,6])

print(2,a+b,a-b)
print(3,a+ np.array(10) ,b+np.array(10))

print(a==b)

c=np.concatenate((a,b))
print(c)

x = np.linspace(-10,10)
y = x**2
fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()


x = np.linspace(-10,10)
y = 2*x**2 + 3
z= -x**2
fig, ax = plt.subplots()
ax.plot(x, y)
ax.plot(x, z)
ax.set_title("TIRT")
ax.set_xlabel("Xlabel")
ax.set_ylabel("Xlabel")
plt.show()
