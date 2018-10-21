import os
import pandas as pd
import numpy as np
import time

import warnings
warnings.filterwarnings('ignore')

import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import seaborn as sns
# %matplotlib inline
plt.style.use('seaborn-whitegrid')
plt.rcParams['savefig.facecolor']='white'

params = {'figure.figsize': (18,12),
            'axes.titlesize': 20}
plt.rcParams.update(params)

def check_dir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

# bar chart for distribution
def plot_pie_chart(df, column, save = False):

    temp = df[column].value_counts()
    temp = pd.DataFrame({'labels': temp.index,
                       'values': temp.values
                      })
    values = temp['values']
    labels = temp['labels']

    fig = plt.figure(figsize=(12, 12), facecolor='w')
    bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.6)
    patches = plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance = 0.8,
        textprops={'fontsize': 20, 'bbox': bbox_props})
    plt.axis('equal')
    title = 'Distribution of ' + column
    plt.title(title, loc = 'center', y=1.08, fontsize = 25)
    plt.tight_layout()

    if save:
        saved_path = os.path.join(plot_dir, title).replace(' ', '-')
        fig.savefig(saved_path, dpi=200, bbox_inches="tight")
    else:
        plt.show()

    plt.close()


data_path = 'data/Glassdoor_Jobs_Data.csv'
plot_dir = 'plot'
check_dir(plot_dir)

jobs_df = pd.read_csv(data_path, encoding = "ISO-8859-1")
print(jobs_df.shape)
print(jobs_df.isnull().sum())
print(jobs_df.nunique())
jobs_df.head()

plot_pie_chart(jobs_df, 'Company Size')
plot_pie_chart(jobs_df, 'Company Size', save = True)
plot_pie_chart(jobs_df, 'Company Revenue')
