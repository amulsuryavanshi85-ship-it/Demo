from turtle import st

from IPython.core import display
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("D:/marketing_campaign_data.csv")

df["Dt_Customer"] = pd.to_datetime(
    df["Dt_Customer"],
    dayfirst=False,
    errors="coerce"
)

# Remove duplicate customers
df = df.drop_duplicates(subset="ID")

# Age
REFERENCE_YEAR = 2025
df["Age"] = REFERENCE_YEAR - df["Year_Birth"]

# Remove implausible ages
df.loc[(df["Age"] < 18) | (df["Age"] > 100), "Age"] = np.nan

# Children
df["Children"] = df["Kidhome"] + df["Teenhome"]

spend_cols = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds"
]

purchase_cols = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
    "NumDealsPurchases"
]

campaign_cols = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5",
    "Response"
]

df["Total_Spend"] = df[spend_cols].sum(axis=1)
df["Total_Purchases"] = df[purchase_cols].sum(axis=1)
df["Total_Campaign_Accepted"] = df[campaign_cols].sum(axis=1)

df["Campaign_Acceptance_Rate"] = (
    df["Total_Campaign_Accepted"] / len(campaign_cols)
)

df["Customer_Tenure_Days"] = (
    pd.Timestamp("2025-01-01") - df["Dt_Customer"]
).dt.days


print(df[["Dt_Customer", "Customer_Tenure_Days"]].head())

df.to_csv("D:/marketing_campaign_data_cleaned new.csv", index=False)

print("Data cleaning completed. Cleaned data saved to 'marketing_campaign_data_cleaned new.csv'.")


df["High_Income"] = np.where(
    df["Income"] > 75000,
    "High Income",
    "Other"
)

df["Young_Customer"] = np.where(
    df["Age"] < 30,
    "Young Customer",
    "Other"
)

df["Campaign_Responder"] = np.where(
    df["Response"] == 1,
    "Campaign Responder",
    "Non Responder"
)

df["High_Web_Engagement"] = np.where(
    df["NumWebVisitsMonth"] > 5,
    "High Web Engagement",
    "Low Web Engagement"
)

df["Family_Customer"] = np.where(
    df["Children"] > 0,
    "Family Customer",
    "No Children"
)

spend_threshold = df["Total_Spend"].quantile(0.90)

df["High_Spender"] = np.where(
    df["Total_Spend"] > spend_threshold,
    "High Spender",
    "Regular Spender"
)



campaign_response = df[
    ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3",
     "AcceptedCmp4", "AcceptedCmp5", "Response"]
].mean().sort_values(ascending=False)

campaign_response.plot(
    kind="bar",
    title="Campaign Acceptance Rate"
)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("D:/marketing_campaign_data.csv")
dictionary = pd.read_csv("D:/marketing_data_dictionary.csv")

print(df.shape)
print(df.head())
print(df.info())
print(df.describe(include="all").T)

# convert date columns to datetime format
df["Dt_Customer"] = pd.to_datetime(
    df["Dt_Customer"],
    errors="coerce",
    dayfirst=True
)

#dataset
reference_date = df["Dt_Customer"].max()

df["Customer_Tenure_Days"] = (
    reference_date - df["Dt_Customer"]
).dt.days

#for age
df["Age"] = reference_date.year - df["Year_Birth"]

#Remove unrealistic ages
df = df[(df["Age"] >= 18) & (df["Age"] <= 100)]

#for income, investigate rather than bindli deleting
df["Income"].isna().sum()
df["Income"].describe()


#If there are a small number of missing incomes, median imputation can be used:
df["Income"] = df["Income"].fillna(df["Income"].median())


#Total spending
spend_cols = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds"
]

df["Total_Spend"] = df[spend_cols].sum(axis=1)

#Total purchases
purchase_cols = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
    "NumDealsPurchases"
]

df["Total_Purchases"] = df[purchase_cols].sum(axis=1)


#Children
df["Children"] = df["Kidhome"] + df["Teenhome"]

# Total compaign acceptance
campaign_cols = [
    "AcceptedCmp1",
    "AcceptedCmp2",
    "AcceptedCmp3",
    "AcceptedCmp4",
    "AcceptedCmp5"
]

df["Total_Campaign_Acceptances"] = df[campaign_cols].sum(axis=1)


# Compaign responder
df["Campaign_Responder"] = (
    df["Response"] == 1
).astype(int)


# High web engagement
df["High_Web_Engagement"] = (
    df["NumWebVisitsMonth"] > 5
).astype(int)


# High spender
spend_90th = df["Total_Spend"].quantile(0.90)

df["High_Spender"] = (
    df["Total_Spend"] > spend_90th
).astype(int)


# Age bands
df["Age_Band"] = pd.cut(
    df["Age"],
    bins=[0, 29, 39, 49, 59, 69, 100],
    labels=[
        "18-29",
        "30-39",
        "40-49",
        "50-59",
        "60-69",
        "70+"
    ]
)


# Income bands
df["Income_Band"] = pd.cut(
    df["Income"],
    bins=[0, 30000, 50000, 75000, 100000, np.inf],
    labels=[
        "Low",
        "Medium",
        "Upper-Medium",
        "High",
        "Very High"
    ]
)


# Buseness rule segment
def assign_segment(row):
    if row["High_Spender"] == 1:
        return "High Spender"
    elif row["Response"] == 1:
        return "Campaign Responder"
    elif row["Income"] > 75000:
        return "High Income"
    elif row["Age"] < 30:
        return "Young Customer"
    elif row["Children"] > 0:
        return "Family Customer"
    elif row["NumWebVisitsMonth"] > 5:
        return "High Web Engagement"
    else:
        return "General Customer"

df["Customer_Segment"] = df.apply(assign_segment, axis=1)


# Univerate Analysis
plt.figure(figsize=(8, 5))
sns.histplot(df["Age"], bins=30, kde=True)
plt.title("Customer Age Distribution")
plt.xlabel("Age")
plt.ylabel("Customers")
plt.show()

# Product spending 
product_spend = df[spend_cols].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 5))
sns.barplot(
    x=product_spend.values,
    y=product_spend.index
)
plt.title("Total Spending by Product Category")
plt.xlabel("Total Spend")
plt.ylabel("Product")
plt.show()

# Calculate overall response 
response_rate = df["Response"].mean() * 100
print(f"Response Rate: {response_rate:.2f}%")

# Compaign wise response
campaign_rates = df[campaign_cols].mean() * 100
print(campaign_rates)

# visualise
campaign_rates.sort_values().plot(
    kind="barh",
    figsize=(8, 5)
)

plt.xlabel("Acceptance Rate (%)")
plt.title("Campaign Acceptance Rates")
plt.show()


# Customer Segmentation Analysis
df.groupby("Customer_Segment").agg(
    Customers=("ID", "count"),
    Avg_Income=("Income", "mean"),
    Avg_Spend=("Total_Spend", "mean"),
    Avg_Purchases=("Total_Purchases", "mean"),
    Avg_Web_Visits=("NumWebVisitsMonth", "mean"),
    Response_Rate=("Response", "mean")
).sort_values("Avg_Spend", ascending=False)

# Compare chanrl
channel_cols = [
    "NumWebPurchases",
    "NumCatalogPurchases",
    "NumStorePurchases",
    "NumDealsPurchases"
]

df.groupby("High_Spender")[channel_cols].mean()



