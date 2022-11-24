import matplotlib.pyplot as plt
from matplotlib import pyplot
import numpy
import matplotlib.ticker as ticker
from math import sqrt

#Уравнение Бернулли: P = (ro_air*V^2)/2
def Bernoulli_equation(N):
    ro_air = 1.2 #Плотность воздуха
    P = 0.163*(N-1000) #Перевод из значений АЦП в давление по калибровке
    V = sqrt(2*abs(P)/ro_air)
    if P < 0 or V < 2: #исключение случаев отрицательного давления, полученных из-за погрешности измерений
        return 0
    return(V)
#Получение данных из файлов (с пересчетом из значений АЦП в скорости по калибровке и уравнению Бернулли)
with open("data00.txt", "r") as file:
    data_00 = [Bernoulli_equation(int(i)) for i in file.read().split("\n")]
with open("data10.txt", "r") as file:
    data_10 = [Bernoulli_equation(int(i)) for i in file.read().split("\n")]
with open("data20.txt", "r") as file:
    data_20 = [Bernoulli_equation(int(i)) for i in file.read().split("\n")]
with open("data30.txt", "r") as file:
    data_30 = [Bernoulli_equation(int(i)) for i in file.read().split("\n")]
with open("data40.txt", "r") as file:
    data_40 = [Bernoulli_equation(int(i)) for i in file.read().split("\n")]
with open("data50.txt", "r") as file:
    data_50 = [Bernoulli_equation(int(i)) for i in file.read().split("\n")]
with open("data60.txt", "r") as file:
    data_60 = [Bernoulli_equation(int(i)) for i in file.read().split("\n")]
with open("data70.txt", "r") as file:
    data_70 = [Bernoulli_equation(int(i)) for i in file.read().split("\n")]
with open("Calibration.txt", "r") as file:
    step_size = [(int(i)-350)*(5.56e-02)for i in file.read().split("\n")]

#Уточнение значений для графиков
for j in range(0, len(step_size)):
        if step_size[j] < -4.6 or step_size[j] > 6:
            data_00[j] = 0
        if step_size[j] < -5.2 or step_size[j] > 7:
            data_10[j] = 0
        if step_size[j] < -6 or step_size[j] > 7.7:
            data_20[j] = 0
        if step_size[j] < -6 or step_size[j] > 11.2:
            data_30[j] = 0
        if step_size[j] < -10 or step_size[j] > 12:
            data_40[j] = 0
        if step_size[j] < -10 or step_size[j] > 13:
            data_50[j] = 0
        if step_size[j] < -13 or step_size[j] > 15:
            data_60[j] = 0
        if step_size[j] < -17 or step_size[j] > 17:
            data_70[j] = 0

Data_Mass = [data_00, data_10, data_20, data_30, data_40, data_50, data_60, data_70] # массив данных
Q = [] # массив расходов струи
#Центрирование графиков относительно нуля:
for M in Data_Mass:
    k = 0
    while k != 3:
        Right = 0
        Left = 0
        d_S = 0
        for j in range(0, len(M)-1):
            r_first = abs(step_size[j]) * (1e-03)
            r_next = abs(step_size[j+1]) * (1e-03)
            V_first = M[j]
            V_next = M[j+1]
            if step_size[j] < 0:
                Left += 0.5*(V_first + V_next)*(abs(r_next - r_first))
            if step_size[j] >= 0:
                Right += 0.5 * (V_first + V_next) * (abs(r_next - r_first))
        d_S = Left - Right
        if d_S > 0:
            for j in range(0, len(M) - 1):
                M[(len(M) - 1) - j] = M[(len(M) - 1) - j - 1]
            k = k + 2
        if d_S < 0:
            for j in range(0, len(M) - 1):
                M[j] = M[j+1]
            k = 1
        if d_S == 0:
            k = 3

#Расчёт расходов для всех сечений
for m in Data_Mass:
    SS = 0
    for j in range(0, len(m)-1):
        r_first = abs(step_size[j]) * (0.001)
        r_next = abs(step_size[j+1]) * (0.001)
        V_first = m[j]
        V_next = m[j+1]
        SS += (r_first * V_first + r_next * V_next)*(abs(r_next - r_first)) * (1000)
    Q.append(str(round(SS * 3.14 * 1.2 / 2, 2)))

#Обьявление массивов скоростей (значения для оси 'y')
datay_00 = numpy.array(data_00)
datay_10 = numpy.array(data_10)
datay_20 = numpy.array(data_20)
datay_30 = numpy.array(data_30)
datay_40 = numpy.array(data_40)
datay_50 = numpy.array(data_50)
datay_60 = numpy.array(data_60)
datay_70 = numpy.array(data_70)
#значения для оси 'x'
data_steps = numpy.array(step_size)

#Построение графика
#параметры фигуры (чем меньше фигура тем выраженее пиксели и развёртка вспомогательной и главной сетки
fig, ax=pyplot.subplots(figsize=(12, 7), dpi=500)
ax.axis([-22, data_steps.max() + 2, -1.4, datay_00.max() + 1.3]) #крайние значения осей
#Параметры подписей делений
ax.tick_params(axis = 'y', which = 'major', labelsize = 14, pad = 2, length = 8)
ax.tick_params(axis = 'x', which = 'major', labelsize = 10, pad = 2, length = 8)
ax.tick_params(axis = 'both', which = 'minor', labelsize = 7, pad = 2, length = 2.5)
ax.minorticks_on() #включение видимости сетки
ax.xaxis.set_major_locator(ticker.MultipleLocator(5)) #интервал основных делений на оси 'x'
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1)) #интервал вспомогательных делений на оси 'x'
ax.yaxis.set_major_locator(ticker.MultipleLocator(5)) #интервал основных делений на оси 'y'
ax.yaxis.set_minor_locator(ticker.MultipleLocator(1)) #интервал вспомогательных делений на оси 'y'
ax.set_title('Скорость потока воздуха' + '\n' + 'в сечении затопленной струи', fontsize = 19, pad = 14, loc = 'center') #название графика
ax.grid(which='major', color = 'gray') #основная сетка
ax.grid(which='minor', color = 'darkgray', linestyle = ':') #второстепенная сетка
ax.set_xlabel("Положение трубки Пито относительно центра струи, мм", fontsize = 12) #подпись оси 'x'
ax.set_ylabel("Скорость воздуха, м/c", fontsize = 16) #подпись оси 'y'
#Построение графиков зависимости скорости воздуха от положений трубки Пито на разных расстояниях
ax.plot(data_steps, datay_00, c='r', linewidth=1.5, label = 'Q (00 мм) = '+ Q[0] + ' г/c')
ax.plot(data_steps, datay_10, c='orange', linewidth=1.5, label ='Q (10 мм) = '+ Q[1] + ' г/c')
ax.plot(data_steps, datay_20, c='y', linewidth=1.5, label ='Q (20 мм) = '+ Q[2] + ' г/c')
ax.plot(data_steps, datay_30, c='green', linewidth=1.5, label ='Q (30 мм) = '+ Q[3] + ' г/c')
ax.plot(data_steps, datay_40, c='c', linewidth=1.5, label ='Q (40 мм) = '+ Q[4] + ' г/c')
ax.plot(data_steps, datay_50, c='blue', linewidth=1.5, label ='Q (50 мм) = '+ Q[5] + ' г/c')
ax.plot(data_steps, datay_60, c='blueviolet', linewidth=1.5, label ='Q (60 мм) = '+ Q[6] + ' г/c')
ax.plot(data_steps, datay_70, c='purple', linewidth=1.5, label ='Q (70 мм) = '+ Q[7] + ' г/c')
#Легенда
ax.legend(shadow = False, loc = 'upper right', fontsize = 13)
print(Q)
plt.show()