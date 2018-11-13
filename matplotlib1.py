import numpy as np
import matplotlib.pyplot as plt


X = np.linspace(-np.pi, np.pi, 256, endpoint = True)

C, S = np.cos(X), np.sin(X)

plt.figure(figsize = (12, 8), dpi = 70)
plt.subplot(111)

plt.plot(X, C, linestyle = '--', linewidth = 2, color = 'red', label = 'Cosine')
plt.plot(X, S, linestyle = ':', linewidth = 2, color = 'green', label = 'Sine')
plt.xlim(X.min() * 1.1, X.max() * 1.1, 6.0)
plt.xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
	[r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
plt.legend(loc = 'upper left', frameon = True)
plt.show()


