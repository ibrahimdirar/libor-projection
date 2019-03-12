import libor
from amortise import amortise
import pandas as pd
from datetime import date
import seaborn as sns
import matplotlib.pyplot as plt

rates = libor.libor(1000)
rates_graph = pd.DataFrame()
rates_desc = {}

rates_br = libor.BASE_RATES
rates_br['Rate'] = 'Base Rate'
rates_br.rename(columns={'base rate': 'value'}, inplace=True)

for i, rate in enumerate(rates):
    # Add column to dataframe with calculated libor ranges
    rate_d = rate.set_index('dates')
    rates_desc[i] = rate_d
    rate['Rate'] = 'LIBOR'
    rate.rename(columns={'LIBOR': 'value'}, inplace=True)
    rate.reset_index(inplace=True)
    rates_graph = rates_graph.append(rate)

rates_graph = rates_graph.append(rates_br, sort=True)
rates_desc = pd.concat(rates_desc, axis=1)
rates_desc = rates_desc.T.describe()

print(rates_desc)

ax = sns.relplot(x='dates', y='value', hue='Rate', style='Rate', kind='line',
                 data=rates_graph, palette='colorblind')
plt.show()
