import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys

read_file = pd.read_excel("C:\\Users\\hp\\Downloads\\OnlineRetail.xlsx")
read_file.to_csv("C:\\Users\\hp\\Downloads\\OnlineRetail.csv",
                 index=None, header=True)

df = pd.DataFrame(pd.read_csv("C:\\Users\\hp\\Downloads\\OnlineRetail.csv"))
df_1 = df[['InvoiceNo', 'StockCode', 'Description', 'Quantity']]

df_2 = df_1.pivot_table(index='InvoiceNo', columns=[
    'Description'], values='Quantity').fillna(0)


def get_recommendations(df, item):
    r1 = df.corrwith(df[item])
    r1.dropna(inplace=True)
    r1 = pd.DataFrame(r1, columns=['correlation']).reset_index()
    r1 = r1.sort_values(by='correlation', ascending=False)
    return r1


while True:
    print("Enter 1 for [Most Popular Items]\nEnter 2 for [Popular items sorted by months]\nEnter 3 for [Popular items sorted by countries]")
    c = int(input())

    if c == 1:
        df1 = df.groupby('Description').agg(orders=('InvoiceNo', 'nunique'), quantity=(
            'Quantity', 'sum')).sort_values(by='orders', ascending=False).head(10)
        print(df1.head(10))
        rp = df1.index[0]
        r2 = get_recommendations(df_2, rp).head(10)
        print(r2.head())
        sns.barplot(x=r2['Description'],
                    y=r2['correlation'])
        plt.xticks(rotation=20)
        plt.tick_params(axis='x', which='major', labelsize=7)
        plt.show()

    elif c == 2:
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

        df['Month'] = df['InvoiceDate'].dt.strftime('%m')

        df['Quantity'] = pd.to_numeric(df['Quantity'])
        df['UnitPrice'] = pd.to_numeric(df['UnitPrice'])

        df['Sales'] = df['Quantity']*df['UnitPrice']

        df2 = df.groupby('Month').sum()
        print(df2.head())
        sns.barplot(x=df2.index, y=df2['Sales'])
        plt.show()

        hsf = df.groupby('Month').sum().sort_values(
            by='Quantity', ascending=False)

        month = int(hsf.index[0])
        m = df['InvoiceDate'].dt.month.between(month, month)
        df_m1 = df.loc[m]
        df_m2 = df_m1[['InvoiceNo', 'StockCode', 'Description', 'Quantity']]
        df3 = df_m2.groupby('Description').agg(orders=('InvoiceNo', 'nunique'), quantity=(
            'Quantity', 'sum')).sort_values(by='orders', ascending=False)
        r1 = df3.index[0]
        r3 = get_recommendations(df_2, r1).head(10)
        print(r3.head())

        sns.barplot(x=r3['Description'],
                    y=r3['correlation'])
        plt.xticks(rotation=20)
        plt.tick_params(axis='x', which='major', labelsize=7)
        plt.show()

    elif c == 3:
        df_2 = df.groupby('Country').sum().sort_values(
            by='Quantity', ascending=False)
        c1 = df_2.index[0]
        print(c1+' is the highest sells country among all of the country.')

        df_4 = df[df['Country'] == c1]
        print("Most popular items of the most popular country: ")
        print(df_4.head())
        df_4 = df_4[['InvoiceNo', 'StockCode', 'Description', 'Quantity']]
        df3 = df_4.groupby('Description').agg(orders=('InvoiceNo', 'nunique'), quantity=(
            'Quantity', 'sum')).sort_values(by='orders', ascending=False)
        rc = df3.index[0]
        r4 = get_recommendations(df_2, rc).head(10)
        print(r4.head())

        sns.barplot(x=r4['Description'],
                    y=r4['correlation'])
        plt.xticks(rotation=20)
        plt.tick_params(axis='x', which='major', labelsize=7)
        plt.show()
