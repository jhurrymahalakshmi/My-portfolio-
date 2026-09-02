# ------------------------------ IMPORT LIBRARIES-----------------------------------

# First of all, we have to import the libraries.
# Honestly I watch a video on how does streamlit function, and I understand that we need to
# re-do the same things like we do in the previous part. So import and reorganise the data
# as a firsts steps.

import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------ UPLOAD AND CLEAN DATA -----------------------------------

# I upload the dataset 

df_account = pd.read_csv("data/Datasets/account-statement-1-1-2024-12-31-2024.csv", sep=";")
df_country_raw = pd.read_csv("data/Datasets/country.csv")
df_symbols = pd.read_csv("data/Datasets/symbols.csv", sep=";")

# And then I clean the dataset like we do before

df_account = df_account.dropna(subset=["IDTransaction"])
df_account = df_account.drop(columns=["Unnamed: 5"], errors="ignore")
df_account["Date"] = pd.to_datetime(df_account["Date"], format="%d/%m/%Y %H:%M:%S")

# For the first question we need just the BUY and SELL 

df_account = df_account[df_account["TransactionType"].isin(["BUY", "SELL"])]

# Then I do the merge with "Symbols", because we want all the rows that match each other.
# So for that transactionst that do not have the correponded symbol, will not be included in the 
# visualizations.

df = df_account.merge(df_symbols, left_on="Symbol", right_on="symbol", how="inner")


# ------------------------------ SET THE PAGE CONFIG -----------------------------------

# I set the title and the layout, and the title of page 1. 

st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("Financial Transactions Dashboard")
st.header("Page 1 - Time Analysis")

# ------------------------------ SET THE COLUMNS ---------------------------------

# The columns are two, from which we deine the range of the time period. 

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start date", value=pd.to_datetime("2024-01-01"))
with col2:
    end_date = st.date_input("End date", value=pd.to_datetime("2024-12-31"))

# Filter dataframe by date range that allow us to filter the data based on the 
# period that we want to visualize. 
# if there's no transactions found for a specific range period, there will be 
# a warning. 

mask = (df["Date"].dt.date >= start_date) & (df["Date"].dt.date <= end_date)
df_filtered = df[mask]

if df_filtered.empty:
    st.warning("No transactions found for the selected date range.")
    st.stop()

# ------------------------------ SET THE GRAPH ---------------------------------

# The first graph is the total transaction over time. 

# If there's no any kink of instructions the standard output is a line color blue.
# So I introduce some instructions to make the graph better

st.subheader("Total Transactions Over Time (BUY & SELL)")
# I group each line by the df_filtered we do above
line_data = df_filtered.groupby(df_filtered["Date"].dt.date).size().reset_index(name="num_transactions")
    
# render_mode="svg" and line_shape="spline" allow to make the curve more smoothy
fig1 = px.line(line_data, x="Date", y="num_transactions", 
                labels={"Date": "Date", "num_transactions": "Transactions"},
                template="plotly_dark") # to make the line sharper and more readable
# Then I set the line_shape, color and "fill=tazeroy" (to fill the color until the zero of the y axes) and "fillcolor=rgba(31, 78, 91, 0.4)"
# that allow to define transparency of the fill (r: red, g: green, b:blue, a:lpha. The firsts one are the ccordinate of y color
# while the alpha is the opacity)
fig1.update_traces(line_shape="spline", line_color="#328fb7", fill="tozeroy", fillcolor="rgba(31, 78, 91, 0.4)")
st.plotly_chart(fig1, width="stretch")



# The second graph concern the top 3 symbols by transaction count. 

st.subheader("Top 3 Traded Symbols by Transaction Count")
# In this case i have to group by the Symbol
top_symbols = df_filtered.groupby("Symbol").size().reset_index(name="num_transactions").sort_values("num_transactions", ascending=False).head(3)
    
fig2 = px.bar(top_symbols, x="Symbol", y="num_transactions", 
              color_discrete_sequence=["#328fb7"], 
              labels={"num_transactions": "Transactions"},
              template="plotly_dark")
st.plotly_chart(fig2, width="stretch")



# In the tirdh graph we have to show the top 5 sector by transaction count.

st.subheader("Top 5 Sector by Transaction Count")
# In this case i have to group by the sector
top_symbols = df_filtered.groupby("sector").size().reset_index(name="num_transactions").sort_values("num_transactions", ascending=False).head(5)
    
fig3 = px.bar(top_symbols, x="sector", y="num_transactions", 
              color_discrete_sequence=["#328fb7"], 
              labels={"num_transactions": "Transactions"},
              template="plotly_dark")
st.plotly_chart(fig3, width="stretch")



# In this last graph we have to show the top 5 industries by transaction count

st.subheader("Top 5 Industries by Transaction Count")
# In this case i have to group by the industry
top_symbols = df_filtered.groupby("industry").size().reset_index(name="num_transactions").sort_values("num_transactions", ascending=False).head(5)
    
fig4 = px.bar(top_symbols, x="industry", y="num_transactions", 
              color_discrete_sequence=["#328fb7"], 
              labels={"num_transactions": "Transactions"},
              template="plotly_dark")
st.plotly_chart(fig4, width="stretch")