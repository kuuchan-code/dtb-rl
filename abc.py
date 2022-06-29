import numpy as np

a = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
print(a)

print(np.reshape(a, (1, *(3, 3))))
print(np.shape(a))