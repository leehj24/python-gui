import pandas as pd
import matplotlib.pyplot as plt


# import csv
df = pd.read_csv("excel.csv")
df = df[["numEmps", "raisedAmt"]]

figure2= plt.Figure(figsize=(5,4))
plt.rcParams.update({'font.size': 22})
ax = df.set_index('numEmps')['craisedAmt'].plot(kind='line', marker='d')
ax.set_ylabel("raisedAmt")
ax.set_xlabel("numEmps")
plt.show()