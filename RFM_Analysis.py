
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_columns',None);pd.set_option('display.max_rows',None)
pd.set_option('display.float_format',lambda x:'%.2f'%x)

df_2010_2011=pd.read_excel(r"C:\Users\Gavita\Desktop\dsmlbcc\MusteriSegmentasyonu\online_retail_II.xlsx",sheet_name="Year 2010-2011")

df=df_2010_2011.copy()

df.head()

df.isnull().sum()
df.groupby("Description").agg({"Quantity":"sum"}).head()
df.groupby("Description").agg({"Quantity":"sum"}).sort_values("Quantity",ascending=False).head()
df.head()
df["TotalPrice"]=df["Quantity"]*df["Price"]

df.head()

df[df["Invoice"].str.contains("C",na=False)].head()

df=df[~df["Invoice"].str.contains("C",na=False)]

df.head()

df.groupby("Invoice").agg({"TotalPrice":"sum"}).head()

df["Country"].value_counts()
df.groupby("Country").agg({"TotalPrice":"sum"}).sort_values("TotalPrice",ascending=False).head()

df1 = df_2010_2011.copy()
df1.head()
df1[df1["Invoice"].str.contains("C",na=False)].head()

df2=df1[df1["Invoice"].str.contains("C",na=False)]
df2["Description"].value_counts().head()
df.head()
df.isnull().sum()
df.dropna(inplace=True)
df.isnull().sum()
df.describe([0.01,0.05,0.10,0.25,0.50,0.75,0.90,0.95, 0.99]).T
df.head()
df["InvoiceDate"].min()
df["InvoiceDate"].max()
import datetime as dt
today_date=dt.datetime(2011,12,9)
today_date

df.groupby("Customer ID").agg({"InvoiceDate":"max"}).head()
df["Customer ID"] = df["Customer ID"].astype(int)
df.head()
df.groupby("Customer ID").agg({"InvoiceDate":"max"}).head()
(today_date - df.groupby("Customer ID").agg({"InvoiceDate":"max"}).head())
today_date

temp_df= (today_date) - (df.groupby("Customer ID").agg({"InvoiceDate":"max"}))
temp_df.head()
temp_df.rename(columns= {"InvoiceDate":"Recency"}, inplace=True)

temp_df.head()
temp_df.iloc[0,0].days
recency_df = temp_df["Recency"].apply(lambda x: x.days)
recency_df.head()

df.groupby("Customer ID").agg({"InvoiceDate" : lambda x: (today_date-x.max()).days}).head()
df.head()
df.groupby(["Customer ID","Invoice"]).agg({"Invoice":"nunique"}).head(50)

freq_df = df.groupby("Customer ID").agg({"InvoiceDate":"nunique"})
freq_df.head()
freq_df.rename(columns={"InvoiceDate": "Frequency"}, inplace=True)
freq_df.head()

df.head()
monetary_df = df.groupby("Customer ID").agg({"TotalPrice":"sum"})
monetary_df.head()
monetary_df.rename(columns={"TotalPrice": "Monetary"}, inplace=True)
monetary_df.head()

print(recency_df.shape,freq_df.shape,monetary_df.shape)
rfm = pd.concat([recency_df, freq_df, monetary_df],  axis=1)
rfm.head()
rfm["RecencyScore"] = pd.qcut(rfm["Recency"], 5, labels = [5, 4 , 3, 2, 1])

rfm.head()
rfm["FrequencyScore"]= pd.qcut(rfm["Frequency"].rank(method="first"),5, labels=[1,2,3,4,5])

rfm.head()
rfm["MonetaryScore"] = pd.qcut(rfm["Monetary"], 5, labels = [1,2,3,4,5])

rfm.head()
(rfm['RecencyScore'].astype(str) +
 rfm['FrequencyScore'].astype(str) +
 rfm['MonetaryScore'].astype(str)).head()

rfm["RFM_SCORE"] = (rfm['RecencyScore'].astype(str) +
                    rfm['FrequencyScore'].astype(str) +
                    rfm['MonetaryScore'].astype(str))
rfm.head()

rfm[rfm["RFM_SCORE"]=="555"].head()

rfm.describe().T

rfm[rfm["RFM_SCORE"]=="111"].head()

seg_map={
    r'[1-2][1-2]':'Hibernating' ,
    r'[1-2][3-4]':'At Risk' ,
    r'[1-2]5':'Can\'t Loose',
    r'3[1-2]':'About To Sleep' ,
    r'33' : 'Need Attention' ,
    r'[3-4][4-5]': 'Loyal Customers',
    r'41': 'Promising',
    r'51': 'New Customers',
    r'[4-5][2-3]': 'Potential Loyalists',
    r'5[4-5]': 'Champions'}

rfm['Segment']= rfm['RecencyScore'].astype(str) + rfm['FrequencyScore'].astype(str)

rfm.head()

rfm['Segment']=rfm['Segment'].replace(seg_map, regex=True)

rfm.head()

rfm[["Segment","Recency","Frequency", "Monetary"]].groupby("Segment").agg(["mean","median","count"])

segment_evaluation=rfm[["Segment","Recency","Frequency", "Monetary"]].groupby("Segment").agg(["mean","median","count"])

segment_evaluation.head(10)

rfm.shape[0]

rfm[rfm["Segment"] == "Loyal Customers"].head()

rfm[rfm["Segment"] == "Loyal Customers"].index

loyal_df=pd.DataFrame()

loyal_df["LoyalCostumerID"]=rfm[rfm["Segment"]=="Loyal Customers"].index

loyal_df.head()

loyal_df.to_excel("loyal_customers.xlsx")

loyal_df.to_excel(r'C:\Users\Gavita\Desktop\export_dataframe1.xlsx', index = False, header=True)

loyal_df.to_excel('loyal_customers.xlsx', index=False)

loyal_df.to_csv("loyal_customers.csv")

loyal_df.to_csv('loyal_customers.csv' , index=False)
