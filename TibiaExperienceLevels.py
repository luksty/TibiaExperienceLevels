import pandas as pd
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error


page = 'https://www.tibia.com/library/?subtopic=experiencetable' #stronka z poziomami
html_tables =  pd.read_html(page, header = 0)     #wyciągamy tabelki html
df = html_tables[0]    #pierwsza tabelka to poziomy punktów

df = df.iloc[1:,:2]    # wycinamy śmieci
df.columns = df.iloc[0]   #ustawiamy nazwy kolumn 

df = df.drop(1)    
df = df.drop(df[df['Level'] == 'Level'].index)  #usuwamy niepotrzebny wiersz
df = df.reset_index(drop=True)
df.to_clipboard()   #kopiuje do schowka - można wkleić w Excelu i podejrzeć dane

df['Level'] = df['Level'].astype('int64')
df['Experience'] = df['Experience'].astype('int64')

def func(x, a, b, c, d):
    return (a * x**3 + b * x**2 + c * x + d)

xdata = df['Level']
ydata = df['Experience']
    


#popt, pcov = curve_fit(func, xdata, ydata, bounds=([0,10.,-1.], [0.1, 25., 0.]))
popt, pcov = curve_fit(func, xdata, ydata)
popt
a, b, c, d = popt

df['fitted'] = df.apply(lambda x: func(x['Level'], a, b, c, d), axis=1)
df['fitted_and_rounded'] = df.apply(lambda x: np.round(x['fitted'], -2), axis=1)
df['error'] = df['Experience'] - df['fitted_and_rounded']
df['error'].sum()
RMSE = np.sqrt(mean_squared_error(df['Experience'], df['fitted_and_rounded']))

ax = df.plot(kind="scatter", x="Level",y="Experience", color="b", label="Experience table")
df.plot(x="Level",y="fitted_and_rounded", color="r", label="model", ax=ax)


ax.set_xlabel("horizontal label")
ax.set_ylabel("vertical label")
plt.show()
df['error'].sum()
df.to_excel('TibiaExperienceLevels.xlsx')
