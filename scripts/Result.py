import matplotlib.pyplot as plt
import numpy as np
steps = 500
santis = 27
x = [0, 10, 20, 30, 40, 50, 60, 70]
y = [1.37, 1.5, 1.62, 2.23, 2.61, 2.78, 3.44, 4.7]
#МНК
z=np.polyfit(x, y, 1)
p=np.poly1d(z)
polif=p(x)

fig, ax = plt.subplots()
ax.set_title("График зависимости расхода от расстояния до сопла")
ax.set_xlabel("Расстояние до сопла, мм")
ax.set_ylabel("Расход, г/с")
ax.minorticks_on()
ax.grid(which='major', color = 'lightgray', linewidth = 2)
ax.grid(which='minor', color = 'lightgray', linestyle = ":")
ax.scatter(x, y, label = 'измерения')
ax.plot(x, polif, color='orange', label = 'АЦП(P)')
#ax.plot(x, k*x+b, color='orange', label = 'АЦП(P)')
ax.legend()
fig.set_figheight(5)
fig.set_figwidth(8)
plt.show()
