import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

csvpath = './atlanta_weather.csv'

with open(csvpath, 'r')as file:
    read_weather = pd.read_csv(file)
    weatherMonth = read_weather.Month
    weatherHigh = read_weather.High
    weatherLow = read_weather.Low

plt.title("Atlanta - Monthly Temperature", fontsize = '20')
plt.plot(weatherMonth, weatherHigh,'b--.' , label='High')
plt.plot(weatherMonth, weatherLow,'g:^', label='Low')
plt.annotate("Highest of the year", arrowprops=dict(facecolor='red'), xy=('Jul',89), xytext=('Jul', 75), fontsize= '16')
plt.legend(fontsize = '20')
plt.ylabel("Temperature(Fahrenheit)", fontsize = '16')
plt.xlabel("Month", fontsize='16')
plt.show()
