import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="Supply Chain Profit Dashboard",
    page_icon="📦",
    layout="wide"
)

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------

df = pd.read_csv("cleaned_data.csv")

# -----------------------------------------------------
# CUSTOM CSS
# -----------------------------------------------------

st.markdown("""
<style>

.main{
    background-color:#F8FAFC;
}

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
    padding-left:2rem;
    padding-right:2rem;
}

h1{
    color:#0F172A;
}

div[data-testid="metric-container"]{
    background:white;
    border-radius:15px;
    padding:20px;
    box-shadow:0px 3px 12px rgba(0,0,0,0.08);
}

section[data-testid="stSidebar"]{
    background:#EEF2FF;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# HEADER
# -----------------------------------------------------

st.title("📦 Supply Chain Profit Analysis Dashboard")

st.write(
    "Interactive dashboard for logistics, sales, customer and supply chain performance."
)

# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------

st.sidebar.title("📊 Dashboard Filters")

market = st.sidebar.multiselect(
    "Select Market",
    options=sorted(df["Market"].unique()),
    default=sorted(df["Market"].unique())
)

segment = st.sidebar.multiselect(
    "Customer Segment",
    options=sorted(df["Customer Segment"].unique()),
    default=sorted(df["Customer Segment"].unique())
)

filtered_df = df[
    (df["Market"].isin(market)) &
    (df["Customer Segment"].isin(segment))
]

# -----------------------------------------------------
# DOWNLOAD BUTTON
# -----------------------------------------------------

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    "⬇ Download Filtered Data",
    csv,
    file_name="filtered_supply_chain.csv",
    mime="text/csv"
)

st.sidebar.markdown("---")

st.sidebar.success(
    f"""
Rows : {len(filtered_df)}

Markets : {filtered_df['Market'].nunique()}

Customers : {filtered_df['Customer Id'].nunique()}
"""
)

# -----------------------------------------------------
# KPI CARDS
# -----------------------------------------------------

sales = filtered_df["Sales"].sum()
profit = filtered_df["Benefit per order"].sum()
orders = len(filtered_df)
customers = filtered_df["Customer Id"].nunique()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("💰 Total Sales", f"${sales:,.0f}")

with c2:
    st.metric("📈 Total Profit", f"${profit:,.0f}")

with c3:
    st.metric("📦 Orders", f"{orders:,}")

with c4:
    st.metric("👥 Customers", f"{customers:,}")

st.markdown("---")
# ======================================================
# TOP ROW
# ======================================================

left, right = st.columns(2)

# ------------------------------------------------------
# TOP CATEGORIES
# ------------------------------------------------------

with left:

    category = (
        filtered_df.groupby("Category Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        category,
        x="Category Name",
        y="Sales",
        color="Sales",
        color_continuous_scale="Blues",
        title="🏆 Top 10 Categories by Sales"
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="Sales ($)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=450,
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------
# PROFIT BY MARKET
# ------------------------------------------------------

with right:

    market_profit = (
        filtered_df.groupby("Market")["Benefit per order"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        market_profit,
        x="Market",
        y="Benefit per order",
        color="Market",
        title="💹 Profit by Market"
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="",
        yaxis_title="Profit ($)",
        height=450,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# SECOND ROW
# ======================================================

left, right = st.columns(2)

# ------------------------------------------------------
# SHIPPING MODE
# ------------------------------------------------------

with left:

    shipping = (
        filtered_df["Shipping Mode"]
        .value_counts()
        .reset_index()
    )

    shipping.columns = ["Shipping Mode", "Orders"]

    fig = px.pie(
        shipping,
        names="Shipping Mode",
        values="Orders",
        hole=0.60,
        color_discrete_sequence=px.colors.sequential.Blues_r,
        title="🚚 Shipping Mode Distribution"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig.update_layout(
        height=500,
        paper_bgcolor="white",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------
# CUSTOMER SEGMENT
# ------------------------------------------------------

with right:

    segment_sales = (
        filtered_df.groupby("Customer Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        segment_sales,
        names="Customer Segment",
        values="Sales",
        hole=0.60,
        title="👥 Sales by Customer Segment",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_layout(
        height=500,
        paper_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
# ======================================================
# THIRD ROW
# ======================================================

left, right = st.columns(2)

# ------------------------------------------------------
# TOP PRODUCTS
# ------------------------------------------------------

with left:

    top_products = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        color="Sales",
        color_continuous_scale="Tealgrn",
        title="📦 Top 10 Products by Sales"
    )

    fig.update_layout(
        coloraxis_showscale=False,
        xaxis_title="Sales ($)",
        yaxis_title="",
        yaxis={"categoryorder": "total ascending"},
        height=500,
        paper_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------
# SALES BY REGION
# ------------------------------------------------------

with right:

    region_sales = (
        filtered_df.groupby("Order Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig = px.bar(
        region_sales,
        x="Order Region",
        y="Sales",
        color="Sales",
        color_continuous_scale="Sunset",
        title="🌍 Sales by Region"
    )

    fig.update_layout(
        coloraxis_showscale=False,
        xaxis_title="",
        yaxis_title="Sales ($)",
        height=500,
        paper_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ======================================================
# FOURTH ROW
# ======================================================

left, right = st.columns(2)

# ------------------------------------------------------
# LATE DELIVERY RISK
# ------------------------------------------------------

with left:

    risk = (
        filtered_df["Late_delivery_risk"]
        .value_counts()
        .reset_index()
    )

    risk.columns = ["Late Delivery", "Orders"]

    fig = px.pie(
        risk,
        names="Late Delivery",
        values="Orders",
        hole=0.6,
        title="🚚 Late Delivery Risk",
        color_discrete_sequence=["#2ECC71", "#E74C3C"]
    )

    fig.update_layout(
        height=450,
        paper_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------
# SHIPPING DELAY
# ------------------------------------------------------

with right:

    delay = (
        filtered_df.groupby("Shipping Mode")["Shipping Delay"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        delay,
        x="Shipping Mode",
        y="Shipping Delay",
        color="Shipping Delay",
        color_continuous_scale="Oranges",
        title="📦 Average Shipping Delay"
    )

    fig.update_layout(
        coloraxis_showscale=False,
        height=450,
        paper_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")  # =====================================================
# DATA TABLE
# =====================================================

st.subheader("📋 Filtered Dataset")

st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")

# =====================================================
# SUMMARY
# =====================================================

st.subheader("📈 Dashboard Summary")

left, right = st.columns(2)

with left:

    st.info(f"""
### Key Highlights

• Total Orders : **{len(filtered_df):,}**

• Total Customers : **{filtered_df['Customer Id'].nunique():,}**

• Total Markets : **{filtered_df['Market'].nunique()}**

• Categories : **{filtered_df['Category Name'].nunique()}**
""")

with right:

    st.success(f"""
### Financial Summary

💰 Total Sales : **${filtered_df['Sales'].sum():,.0f}**

📈 Total Profit : **${filtered_df['Benefit per order'].sum():,.0f}**

📦 Average Sales : **${filtered_df['Sales'].mean():,.2f}**

🚚 Average Shipping Delay :
**{filtered_df['Shipping Delay'].mean():.2f} Days**
""")

st.markdown("---")

# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
<center>

## 📦 Supply Chain Profit Analysis Dashboard

Developed by **Radhika UR**

**Data Analytics Internship Project**

Technologies Used

Python • Pandas • Plotly • Streamlit

</center>
""",
    unsafe_allow_html=True
)
