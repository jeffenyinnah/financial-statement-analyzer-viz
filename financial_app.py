import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import io
from io import BytesIO

# Title of the app
st.title('Analyze and Visualize your Financial Data')

# Sample data loading and uploading
uploaded_file = st.file_uploader("Upload your financial data", type=["csv", "xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file, index_col=False)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.write("### Raw Data", df)
    
    # Multi-level Filtering
    st.sidebar.header("Filter Data")
    columns_to_filter = st.sidebar.multiselect("Select columns to filter", df.columns)
    if columns_to_filter:
        for column in columns_to_filter:
            unique_values = df[column].unique()
            selected_values = st.sidebar.multiselect(f"Filter {column}", unique_values)
            if selected_values:
                df = df[df[column].isin(selected_values)]
    
    # Data Transformation Tools
    st.sidebar.header("Data Transformation")
    group_by_column = st.sidebar.selectbox("Group by column", df.columns)
    aggregation_function = st.sidebar.selectbox("Aggregation function", ["sum", "mean", "max", "min"])
    
    if group_by_column and aggregation_function:
        df_grouped = df.groupby(group_by_column).agg(aggregation_function)
        st.write("### Transformed Data", df_grouped)
        
    # Financial Metrics and Ratios
    st.sidebar.header("Financial Ratios")
    ratio_options = st.sidebar.multiselect("Select financial ratios to calculate", 
        ["Current Ratio", "Quick Ratio", "Debt to Equity", "Net Profit Margin"])

    ratios = {}
    if "Current Ratio" in ratio_options:
        ratios["Current Ratio"] = df["Current Assets"].sum() / df["Current Liabilities"].sum()

    if "Quick Ratio" in ratio_options:
        ratios["Quick Ratio"] = (df["Current Assets"].sum() - df["Inventory"].sum()) / df["Current Liabilities"].sum()

    if "Debt to Equity" in ratio_options:
        ratios["Debt to Equity"] = df["Total Liabilities"].sum() / df["Shareholder Equity"].sum()

    if "Net Profit Margin" in ratio_options:
        ratios["Net Profit Margin"] = (df["Net Income"].sum() / df["Revenue"].sum()) * 100

    if ratios:
        st.write("### Financial Ratios", ratios)

    # Data Visualization Enhancements
    st.sidebar.header("Data Visualization")
    chart_type = st.sidebar.selectbox("Select chart type", ["Bar", "Line", "Pie", "Scatter"])
    x_axis = st.sidebar.selectbox("X-axis", df.columns)
    y_axis = st.sidebar.selectbox("Y-axis", df.columns)

    if chart_type == "Bar":
        fig = px.bar(df, x=x_axis, y=y_axis)
    elif chart_type == "Line":
        fig = px.line(df, x=x_axis, y=y_axis)
    elif chart_type == "Pie":
        fig = px.pie(df, names=x_axis, values=y_axis)
    elif chart_type == "Scatter":
        fig = px.scatter(df, x=x_axis, y=y_axis)

    st.plotly_chart(fig)

    # Drill-Down Capabilities
    if st.button("Drill Down"):
        drill_down_col = st.selectbox("Select column to drill down", df.columns)
        drill_down_value = st.selectbox("Select value", df[drill_down_col].unique())
        df_drilled = df[df[drill_down_col] == drill_down_value]
        st.write("### Drill-Down Data", df_drilled)
        
    # Custom Reporting
    st.sidebar.header("Download Report")
    download_format = st.sidebar.selectbox("Select format", ["Excel", "PDF"])

    if download_format == "Excel":
        output = BytesIO()
        
        # Use XlsxWriter as an engine for ExcelWriter
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Financial Data')
        
        # Get the Excel file as bytes
        processed_data = output.getvalue()
        
        # Create download button for Excel file
        st.download_button(label="Download Excel Report", data=processed_data, file_name="financial_report.xlsx", mime="application/vnd.ms-excel")

    elif download_format == "PDF":
        # Placeholder for PDF export feature
        st.write("PDF export feature is under development.")

