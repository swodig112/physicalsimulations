import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from copy import deepcopy
films = [
         [1, 0],
         [1.38**2,    99],
         [1.85**2,     148],
         [1.52**2,     0]]

f = []
for i in films:
    f.append([i[0]**0.5, i[1]])
films = f

c = 3 * 10**17
class Wave:
    def __init__(self, w, e, theta, pol, filmid, di, phase=1):
        self.w = w
        self.e = e
        self.filmid = filmid
        self.di = di
        self.phase = phase
        self.lam = 2 * np.pi * c / self.w
        self.pol = pol
        self.theta = theta

    def get_lam_in(self, n):
        return self.lam / n

def incident(wave, films):
    f1 = films[wave.filmid]
    f2 = films[wave.filmid + wave.di]
    sin_theta2 = f1[0] * np.sin(wave.theta) / f2[0]
    
    if np.abs(sin_theta2) >= 1.0: # Total internal reflection
        r = 1.0 + 0j
        t = 0.0 + 0j
        theta2 = wave.theta            # Angle doesn't change due to reflection
    else:
        theta2 = np.arcsin(sin_theta2)
        if wave.pol:  # s-polarization
            r = (f1[0] * np.cos(wave.theta) - f2[0] * np.cos(theta2)) / \
                (f1[0] * np.cos(wave.theta) + f2[0] * np.cos(theta2))
            t = (2 * f1[0] * np.cos(wave.theta)) / \
                (f1[0] * np.cos(wave.theta) + f2[0] * np.cos(theta2))
        else:  # p-polarization
            r = (f2[0] * np.cos(wave.theta) - f1[0] * np.cos(theta2)) / \
                (f2[0] * np.cos(wave.theta) + f1[0] * np.cos(theta2))
            t = (2 * f1[0] * np.cos(wave.theta)) / \
                (f2[0] * np.cos(wave.theta) + f1[0] * np.cos(theta2))

    wr = deepcopy(wave)
    wr.e *= r
    wr.di *= -1

    wt = deepcopy(wave)
    wt.e *= t
    wt.filmid += wt.di
    wt.theta = theta2

    return [wr, wt]
def finalamp(waves):
    return sum(w.e * w.phase for w in waves) 


def calR(w, ang, pol, films):
    amp0 = 1
    waves = [Wave(w, amp0, ang, pol, 0, 1, phase=1)]
    outwaves = []
    cc = 0
    # print(ang)
    while waves:# and cc < 20:
        # cc += 1
        # print(cc)
        newwaves = []
        for wave in waves:
            # Calculating phase shift
            if wave.filmid > 0 and wave.filmid < len(films) - 1:
                layer = films[wave.filmid]
                phase_factor = np.exp(
                    1j * 2 * np.pi * layer[1] * np.cos(wave.theta) / 
                    wave.get_lam_in(layer[0])
                )
                    # print("YUP")
                wave.phase *= phase_factor
            
            newwaves += incident(wave, films)
        
        # Reflected waves:
        outwaves += [w for w in newwaves if w.filmid == 0 and w.di == -1]

        
        waves = [
            w for w in newwaves 
            if w.filmid not in (0, len(films)-1) 
            and abs(w.e) > 1e-6   # Removing weak waves
        ]
    
    r = finalamp(outwaves) / amp0
    R = np.abs(r)**2
    return R

def inpt(desc, tp):
    while True:
        s = input(desc)
        try:
            return tp(s)
        except ValueError:
            print("Incorrect input. Try again...")

def mltinpt(desc, vals):
    while True:
        # s = input(desc + ' ' + str(tuple(["{0}: {1}".format(i, j) for i, j in enumerate(vals)])) + ' ')
        s = inpt(desc + ' ' + str(tuple(["{0}: {1}".format(i, j) for i, j in enumerate(vals)])) + ' ', int)
        if 0 <= s < len(vals):
            return s
        else:
            print("Insert a number in range")
        # try:
            # if 0 <= int(s) < len(vals):
                # return int(s)
            # else:
                # print("Insert a number in range")
        # except ValueError:
            # print("Insert a number")
            # pass

def main():
    pol = mltinpt("Insert polarization", ['p', 's'])
    dim = mltinpt("Do you want a 3D graph or a 2D one?", ['2D', '3D'])
    if dim == 0:
        var = mltinpt("Do you want the angel of incidence to be a variable or the wavelength?", ['theta (degrees)', 'lambda (nm)'])
        if var == 1:
            lami = inpt("Insert the lower limit of wavelength (nm): ", float)
            lamf = inpt("Insert the upper limit of wavelength (nm): ", float)
            ang = inpt("Insert the constant angel in degrees: ", float) * np.pi/180
            lambdas = np.linspace(lami, lamf, 100)
            R = []
            for i in lambdas:
                R.append(calR(2*np.pi*c/i, ang, pol, films)*100)
            plt.plot(lambdas, R)
            plt.xlabel("Wavelength (nm)")
            plt.ylabel("Reflection (%)")
            plt.show()
        else:
            angi = inpt("Insert the lower limit of theta (degrees): ", float) * np.pi/180
            angf = inpt("Insert the upper limit of theta (degrees): ", float) * np.pi/180
            lam = inpt("Insert the constant wavelength (nm): ", float)
            angels = np.linspace(angi, angf, 200)
            R = []
            for i in angels:
                R.append(calR(2*np.pi*c/lam, i, pol, films)*100)
            plt.plot(angels*180/np.pi, R)
            plt.xlabel("Angle of Incidence (degrees)")
            plt.ylabel("Reflection (%)")
            plt.show()
    else:
        lami = inpt("Insert the lower limit of wavelength (nm): ", float)
        lamf = inpt("Insert the upper limit of wavelength (nm): ", float)
        angi = inpt("Insert the lower limit of theta (degrees): ", float) * np.pi/180
        angf = inpt("Insert the upper limit of theta (degrees): ", float) * np.pi/180
        angels = np.linspace(angi, angf, 100)
        lambdas = np.linspace(lami, lamf, 100)
        x, y = np.meshgrid(angels, lambdas)
        z = np.zeros_like(x)
        for i in range(angels.size):
            for j in range(lambdas.size):
                z[i, j] = calR(2*np.pi*c/lambdas[i], angels[j], True, films)
        z *= 100
        x *= 180/np.pi
        fig=plt.figure()
        ax=fig.add_subplot(111, projection="3d")
        ax.set_xlabel("Angle of Incidence (degrees)")
        ax.set_ylabel("Wavelength (nm)")
        ax.set_zlabel("Reflection (%)")
        surf = ax.plot_surface(x,y,z, cmap='coolwarm')
        plt.show()
if __name__ == "__main__":
    main()
