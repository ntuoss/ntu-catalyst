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

def plot_box(df, column, save = False):

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

#
# # bubble plot
# def plot_bubble_chart(df, column, save = False):
#
#     selected_categories = df.groupby([df.columns[0]])['Total Search'].sum().reset_index().sort_values('Total Search').tail(12)[df.columns[0]]
#     df = df[df[df.columns[0]].isin(selected_categories)]
#
#     fig = sns.relplot(x="Total Search", y=column, size="Total Search", hue="Total Search",
#         sizes=(1000, 10000), data=df, height=8, aspect=12/8, legend = False)
#     bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.6)
#     for line in range(0,df.shape[0]):
#          plt.text(df["Total Search"].iloc[line], df[column].iloc[line], df[df.columns[0]].iloc[line],
#             bbox=bbox_props, horizontalalignment='left', size='large', color='black', fontsize = 20)
#     title = column + ' vc Total Search by ' + category
#     plt.xlim(0, df['Total Search'].max()*1.1)
#     plt.ylim(0, df[column].max()*1.1)
#     x = np.linspace(0, df['Total Search'].max()*1.1, df['Total Search'].max()*1.1)
#     y = [df[column].mean()] * len(x)
#     plt.plot(x, y, linewidth = 2, color = 'red')
#     plt.title(title, loc = 'center', y=1.08, fontsize = 25)
#
#     if save:
#         saved_path = os.path.join(plot_dir, title).replace(' ', '-')
#         fig.savefig(saved_path, dpi=200, bbox_inches="tight")
#     else:
#         plt.show()
#
#     plt.close()

data_path = 'data/Glassdoor_Jobs_Data.csv'
plot_dir = 'plot'
check_dir(plot_dir)

jobs_df = pd.read_csv(data_path, encoding = "ISO-8859-1")
print(jobs_df.shape)
print(jobs_df.isnull().sum())
print(jobs_df.nunique())
print(jobs_df.describe())
jobs_df.head()

# Data Cleaning ================================================================
jobs_df = jobs_df.rename(columns = {'Comapny Description': 'Company Description'})

# Industry
# Two companies categorize itself under 2 industries
df = jobs_df.drop_duplicates(['Company', 'Industry']).groupby(['Company'])['Industry'].count().reset_index()
companies_more_than_1_industry = list(df[df['Industry'] > 1]['Company'])
companies_more_than_1_industry
jobs_df[jobs_df['Company'] == companies_more_than_1_industry[0]]['Industry'].value_counts()
jobs_df[jobs_df['Industry'] == 'Lending']['Company'].unique()
citibank_industry = jobs_df[jobs_df['Company'] == companies_more_than_1_industry[0]]['Industry'].value_counts().index[1]
jobs_df['Industry'] = jobs_df['Industry'].replace('Lending', citibank_industry)
jobs_df['Company'] = jobs_df['Company'].replace('Citibank NA', 'Citibank')
jobs_df[jobs_df['Company'] == 'Citibank NA'].shape

jobs_df[jobs_df['Company'] == companies_more_than_1_industry[1]]['Industry'].value_counts()
jobs_df[jobs_df['Industry'] == 'Wholesale']['Company'].unique()
jobs_df[jobs_df['Industry'] == 'Biotech & Pharmaceuticals']['Company'].unique()
jobs_df['Industry'] = jobs_df['Industry'].replace('Wholesale', 'Biotech & Pharmaceuticals')

jobs_df['Industry'] = jobs_df['Industry'].fillna('NA')

# Company: Take out NAs
jobs_df = jobs_df[~pd.isna(jobs_df['Company'])]

# Company Description: Concatenate description for company that has more than one company description
df = jobs_df.drop_duplicates(['Company', 'Company Description']).groupby(['Company'])['Company Description'].count().reset_index()
companies_more_than_1_desc = list(df[df['Company Description'] > 1]['Company'])
companies_more_than_1_desc
desc_concat = ' '.join(jobs_df[jobs_df['Company'] == companies_more_than_1_desc[0]]['Company Description'].value_counts().index)
jobs_df[jobs_df['Company'] == companies_more_than_1_desc[0]]
jobs_df.loc[jobs_df['Company'] == companies_more_than_1_desc[0], 'Company Description'] = desc_concat

jobs_df['Company Description'] = jobs_df['Company Description'].fillna('NA')

# Job Description: NAs
jobs_df['Job Description'] = jobs_df['Job Description'].fillna('NA')

# Head Quarter
df = jobs_df.drop_duplicates(['Company', 'Head Quarter']).groupby(['Company'])['Head Quarter'].count().reset_index()
companies_more_than_1_hq = list(df[df['Head Quarter'] > 1]['Company'])
companies_more_than_1_hq
for company in companies_more_than_1_hq:
    hq = jobs_df[jobs_df['Company'] == company]['Head Quarter'].value_counts().index[0]
    jobs_df.loc[jobs_df['Company'] == company, 'Head Quarter'] = hq

jobs_df['Head Quarter'] = jobs_df['Head Quarter'].fillna('NA')

# Company Size: NAs
df = jobs_df.drop_duplicates(['Company', 'Company Size']).groupby(['Company'])['Company Size'].count().reset_index()
companies_more_than_1_size = list(df[df['Company Size'] > 1]['Company'])
for company in companies_more_than_1_size:
    size = jobs_df[jobs_df['Company'] == company]['Company Size'].value_counts().index[0]
    jobs_df.loc[jobs_df['Company'] == company, 'Company Size'] = size

jobs_df = jobs_df[~pd.isna(jobs_df['Company Size'])]
sizes = list(jobs_df['Company Size'].value_counts().index)
sizes_map = {size: int(sum([int(size.split()[0]), int(size.split()[2])]) / 2) for size in sizes[1:]}
sizes_map[sizes[0]] = 25000
jobs_df['Company Size (Num)'] = jobs_df['Company Size'].map(sizes_map)

# Company Revenue
revenues = list(jobs_df['Company Revenue'].value_counts().index)
revenue_map = {revenue: int(sum([int(revenue.split()[0][1:]), int(revenue.split()[2][1:])]) / 2) * 10**(6 if revenue.split()[-2] == 'million' else 9) for revenue in revenues[1:-1]}
revenue_map[revenues[0]] = 25 * 10**9
revenue_map[revenues[-1]] = 0.5 * 10**6
jobs_df['Company Revenue (Num)'] = jobs_df['Company Revenue'].map(revenue_map)


# Overall Rating
df = jobs_df.drop_duplicates(['Company', 'Overall Rating']).groupby(['Company'])['Overall Rating'].count().reset_index()
companies_more_than_1_rating = list(df[df['Overall Rating'] > 1]['Company'])
companies_more_than_1_rating
for company in companies_more_than_1_rating:
    rating = jobs_df[jobs_df['Company'] == company]['Overall Rating'].value_counts().index[0]
    jobs_df.loc[jobs_df['Company'] == company, 'Overall Rating'] = rating

company_no_rating = list(set(jobs_df[pd.isna(jobs_df['Overall Rating'])]['Company']))
for company in company_no_rating:
    ratings = list(jobs_df[jobs_df['Company'] == company]['Overall Rating'].value_counts().index)
    if len(ratings) != 0:
        jobs_df.loc[jobs_df['Company'] == company, 'Overall Rating'] = ratings[0]
rating_mode = jobs_df['Overall Rating'].mode()[0]
jobs_df['Overall Rating'].fillna(rating_mode, inplace = True)

sns.distplot(jobs_df['Overall Rating'])
jobs_df.loc[jobs_df['Overall Rating'] == -1, 'Overall Rating'] = rating_mode

# Founded Year
sns.distplot(jobs_df['Founded Year'])
df = jobs_df.drop_duplicates(['Company', 'Founded Year']).groupby(['Company'])['Founded Year'].count().reset_index()
companies_more_than_1_year = list(df[df['Founded Year'] > 1]['Company'])
for company in companies_more_than_1_year:
    years = list(jobs_df[jobs_df['Company'] == company]['Founded Year'].value_counts().index)
    if 0 in years:
        years.remove(0)
    jobs_df.loc[jobs_df['Company'] == company, 'Founded Year'] = years[0]

jobs_df['Founded Year'].replace(0, np.nan, inplace = True)
year_mode = jobs_df['Founded Year'].mode()[0]
jobs_df['Founded Year'].fillna(year_mode, inplace = True)


# Data Plotting ================================================================
# Univariate
plot_pie_chart(jobs_df, 'Company Size')
plot_pie_chart(jobs_df, 'Company Size', save = True)
plot_pie_chart(jobs_df, 'Company Revenue')
plot_pie_chart(jobs_df, 'Company Revenue', save = True)

sns.distplot(jobs_df['Overall Rating'])
sns.distplot(jobs_df['Founded Year'])

sns.catplot(x="Company Size", kind="count", data=jobs_df, order=list(jobs_df[~pd.isna(jobs_df['Company Size (Num)'])].sort_values('Company Size (Num)')['Company Size'].unique()), height=8, aspect=12/8)
sns.catplot(x="Company Revenue", kind="count", data=jobs_df, order=list(jobs_df[~pd.isna(jobs_df['Company Revenue (Num)'])].sort_values('Company Revenue (Num)')['Company Revenue'].unique()), height=12, aspect=12/8)
sns.catplot(x="Company Revenue", kind="count", data=jobs_df, order=list(jobs_df.sort_values('Company Revenue (Num)')['Company Revenue'].unique()), height=8, aspect=12/8)

jobs_df.columns
Index(['Job Title', 'Company', 'Salary 50th Percentile',
       'Salary 10th Percentile', 'Salary 90th Percentile', 'Overall Rating',
       'Company Description', 'Founded Year', 'Head Quarter', 'Company Size',
       'Industry', 'Company Revenue', 'Job Description', 'Company Size (Num)',
       'Company Revenue (Num)'],
      dtype='object')

# Bivariate
sns.catplot(x="Company Size", y="Company Revenue (Num)", order=list(jobs_df.sort_values('Company Size (Num)')['Company Size'].unique()), kind="box", data=jobs_df, height=8, aspect=12/8)

sns.catplot(x="Company Size", y="Salary 50th Percentile", order=list(jobs_df.sort_values('Company Size (Num)')['Company Size'].unique()), kind="box", data=jobs_df, height=8, aspect=12/8)
sns.catplot(x="Company Size", y="Salary 10th Percentile", order=list(jobs_df.sort_values('Company Size (Num)')['Company Size'].unique()), kind="box", data=jobs_df, height=8, aspect=12/8)
sns.catplot(x="Company Size", y="Salary 90th Percentile", order=list(jobs_df.sort_values('Company Size (Num)')['Company Size'].unique()), kind="box", data=jobs_df, height=8, aspect=12/8)

df = pd.concat([jobs_df[['Company Size', 'Salary 10th Percentile']].rename(columns = {'Salary 10th Percentile': 'Salary'}), jobs_df[['Company Size', 'Salary 50th Percentile']].rename(columns = {'Salary 50th Percentile': 'Salary'}), jobs_df[['Company Size', 'Salary 90th Percentile']].rename(columns = {'Salary 90th Percentile': 'Salary'})])
df['Salary Type'] = ['Salary 10th Percentile'] * jobs_df.shape[0] + ['Salary 50th Percentile'] * jobs_df.shape[0] + ['Salary 90th Percentile'] * jobs_df.shape[0]


fig = sns.catplot(x="Company Size", y="Salary", hue = 'Salary Type', order=list(jobs_df.sort_values('Company Size (Num)')['Company Size'].unique()), kind="box", data=df, height=8, aspect=12/8)
title = "Salary Range for Company with Different Size"
plt.title(title, loc = 'center', y=1.08, fontsize = 25)
saved_path = os.path.join(plot_dir, title).replace(' ', '-')
fig.savefig(saved_path, dpi=200, bbox_inches="tight")


# Plot Word Cloud
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

text = " ".join(review for review in jobs_df['Job Description'])
print ("There are {} words in the combination of all review.".format(len(text)))

# Create stopword list:
stopwords = set(STOPWORDS)
# stopwords.update([])
wordcloud = WordCloud(width=1600, height=800, stopwords=stopwords, background_color="white").generate(text)
plt.figure( figsize=(20,10), facecolor='w')
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
# plt.show()
plt.savefig('wordcloud.png', bbox_inches='tight')
