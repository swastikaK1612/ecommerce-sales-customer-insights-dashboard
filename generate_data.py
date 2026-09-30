eimport streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Commerce Sales & Customer Insights Dashboard")
st.markdown(
    "Analyze sales, customers, products and geographical performance."
)

# ---------------------------------------------------
# SAMPLE E-COMMERCE DATA
# ---------------------------------------------------

data = {
    "Order_ID": [
        1001, 1002, 1003, 1004, 1005,
        1006, 1007, 1008, 1009, 1010,
        1011, 1012, 1013, 1014, 1015
    ],

    "Order_Date": [
        "2026-01-05", "2026-01-10", "2026-01-15",
        "2026-02-02", "2026-02-10", "2026-02-18",
        "2026-03-03", "2026-03-12", "2026-03-20",
        "2026-04-05", "2026-04-15", "2026-04-25",
        "2026-05-05", "2026-05-15", "2026-05-25"
    ],

    "Customer_ID": [
        "C001", "C002", "C003", "C001", "C004",
        "C005", "C002", "C006", "C007", "C003",
        "C008", "C009", "C001", "C010", "C005"
    ],

    "Product": [
        "Laptop", "Smartphone", "Headphones", "Laptop",
        "Smartwatch", "Tablet", "Smartphone", "Keyboard",
        "Mouse", "Laptop", "Tablet", "Headphones",
        "Smartwatch", "Smartphone", "Laptop"
    ],

    "Category": [
        "Electronics", "Electronics", "Accessories",
        "Electronics", "Wearables", "Electronics",
        "Electronics", "Accessories", "Accessories",
        "Electronics", "Electronics", "Accessories",
        "Wearables", "Electronics", "Electronics"
    ],

    "Quantity": [
        1, 2, 3, 1, 2,
        1, 1, 2, 3, 1,
        2, 2, 1, 1, 1
    ],

    "Price": [
        60000, 25000, 2000, 60000, 8000,
        30000, 25000, 1500, 1000, 60000,
        30000, 2000, 8000, 25000, 60000
    ],

    "Region": [
        "South", "North", "South", "East", "West",
        "South", "North", "East", "West", "South",
        "North", "South", "East", "West", "South"
    ]
}

df = pd.DataFrame(data)

# ---------------------------------------------------
# DATA CLEANING
# ---------------------------------------------------

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Remove duplicate orders
df = df.drop_duplicates(subset="Order_ID")

# Remove missing values
df = df.dropna()

# Calculate revenue
df["Revenue"] = df["Quantity"] * df["Price"]

# Create month column
df["Month"] = df["Order_Date"].dt.strftime("%B")

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("🔎 Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories))
]

# ---------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------

total_revenue = filtered_df["Revenue"].sum()

total_orders = filtered_df["Order_ID"].nunique()

total_customers = filtered_df["Customer_ID"].nunique()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0 else 0
)

# Repeat customers
customer_orders = filtered_df.groupby(
    "Customer_ID"
)["Order_ID"].nunique()

repeat_customers = (customer_orders > 1).sum()

repeat_customer_rate = (
    repeat_customers / total_customers * 100
    if total_customers > 0 else 0
)

# ---------------------------------------------------
# KPI DISPLAY
# ---------------------------------------------------

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Revenue",
    f"₹{total_revenue:,.0f}"
)

col2.metric(
    "Total Orders",
    total_orders
)

col3.metric(
    "Customers",
    total_customers
)

col4.metric(
    "Average Order Value",
    f"₹{average_order_value:,.0f}"
)

col5.metric(
    "Repeat Customer Rate",
    f"{repeat_customer_rate:.1f}%"
)

# ---------------------------------------------------
# MONTHLY SALES TREND
# ---------------------------------------------------

st.subheader("📈 Monthly Revenue Trend")

monthly_sales = (
    filtered_df
    .groupby("Month")["Revenue"]
    .sum()
)

month_order = [
    "January", "February", "March",
    "April", "May", "June",
    "July", "August", "September",
    "October", "November", "December"
]

monthly_sales = monthly_sales.reindex(
    [m for m in month_order if m in monthly_sales.index]
)

st.line_chart(monthly_sales)

# ---------------------------------------------------
# PRODUCT ANALYSIS
# ---------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top Products")

    top_products = (
        filtered_df
        .groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(top_products)

with col2:
    st.subheader("📦 Sales by Category")

    category_sales = (
        filtered_df
        .groupby("Category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_sales)

# ---------------------------------------------------
# REGIONAL ANALYSIS
# ---------------------------------------------------

st.subheader("🌍 Sales by Region")

region_sales = (
    filtered_df
    .groupby("Region")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(region_sales)

# ---------------------------------------------------
# CUSTOMER ANALYSIS
# ---------------------------------------------------

st.subheader("👥 High-Value Customers")

customer_sales = (
    filtered_df
    .groupby("Customer_ID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(
    customer_sales.reset_index().rename(
        columns={"Revenue": "Total Revenue"}
    ),
    use_container_width=True
)

# ---------------------------------------------------
# TOP PRODUCTS TABLE
# ---------------------------------------------------

st.subheader("🛍️ Product Performance")

product_performance = (
    filtered_df
    .groupby(["Product", "Category"])
    .agg(
        Quantity_Sold=("Quantity", "sum"),
        Revenue=("Revenue", "sum")
    )
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

st.dataframe(
    product_performance,
    use_container_width=True
)

# ---------------------------------------------------
# BUSINESS RECOMMENDATIONS
# ---------------------------------------------------

st.subheader("💡 Data-Driven Recommendations")

if not filtered_df.empty:

    best_product = (
        filtered_df.groupby("Product")["Revenue"]
        .sum()
        .idxmax()
    )

    best_region = (
        filtered_df.groupby("Region")["Revenue"]
        .sum()
        .idxmax()
    )

    best_category = (
        filtered_df.groupby("Category")["Revenue"]
        .sum()
        .idxmax()
    )

    st.write(
        f"• **Promote {best_product}** because it generates the highest revenue."
    )

    st.write(
        f"• **Focus on the {best_region} region** because it has the highest sales."
    )

    st.write(
        f"• **Strengthen the {best_category} category** through promotions and product offers."
    )

    st.write(
        "• Encourage repeat purchases using loyalty programs and personalized offers."
    )

else:
    st.warning("No data available for the selected filters.")

# ---------------------------------------------------
# RAW DATA
# ---------------------------------------------------

with st.expander("📄 View Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )

st.markdown("---")
st.caption("E-Commerce Sales & Customer Insights Dashboard | Python + Pandas + Streamlit")