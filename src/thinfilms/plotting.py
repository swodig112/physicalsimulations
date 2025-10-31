from thinfilms import *

lam0 = 550
lams = np.linspace(350, 850, 1000)
# A
films = [[1, 0],
         [1.65, lam0 / 1.65 / 4],
         [2.1, lam0 / 2.1 / 4],
         [1.52, 0]]
ra = []
rb = []
rc = []
for i in lams:
    ra.append(calR(2*np.pi*c/i, 0, 1, films)*100)

films = [[1, 0],
         [1.38, lam0 / 1.38 / 4],
         [1.6, lam0 / 1.6 / 2],
         [1.52, 0]]
for i in lams:
    rb.append(calR(2*np.pi*c/i, 0, 1, films)*100)

films = [[1, 0],
         [1.38, lam0 / 1.38 / 4],
         [1.85, lam0 / 1.85 / 2],
         [1.52, 0]]
for i in lams:
    rc.append(calR(2*np.pi*c/i, 0, 1, films)*100)

plt.plot(lams, ra, label='a')
plt.plot(lams, rb, label='b')
plt.plot(lams, rc, label='c')
plt.plot(lams, 4.2*np.ones(lams.size), '--', label='Uncoated Glass')
plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflection (%)")
plt.grid()
plt.legend()
plt.show()
