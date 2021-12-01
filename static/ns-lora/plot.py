import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

sns.set_style("whitegrid")

data = pd.read_csv("telemetry-final/Success-Rate-Global-points-interval.csv", delimiter=";")

#print(data)

data = data.melt('Nsta', var_name='Configurations',  value_name='Success Rate (%)')
g = sns.catplot(x="Nsta", y="Success Rate (%)", hue='Configurations', data=data, kind='point')

g.set(xlabel='Number of stations', ylabel='Success Rate (%)', ylim=(49, 105))

plt.show()

data = pd.read_csv("telemetry-final/Ratio-Global-points-interval-new.csv", delimiter=";")

#print(data)

data = data.melt('Nsta', var_name='Configurations',  value_name='Energy efficiency ratio (KiloBytes/J)')
g = sns.catplot(x="Nsta", y="Energy efficiency ratio (KiloBytes/J)", hue='Configurations', data=data, kind='point')

g.set(xlabel='Number of stations', ylabel='Energy efficiency ratio (KiloBytes/J)')

plt.show()

data = pd.read_csv("latency/latency-tronque.csv", delimiter=";")

print(data)

data = data.melt('PayloadSize', var_name='Configurations',  value_name='Latency (s)')
g = sns.catplot(x="PayloadSize", y="Latency (s)", hue='Configurations', data=data, kind='point')

g.set(xlabel='Payload Size', ylabel='Latency (s)')

#plt.show()