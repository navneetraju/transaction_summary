import streamlit as st
import pandas as pd
from report import generate_report
from clean import clean_df

st.set_page_config(layout='wide')
st.title("📊 Transactions Summary Report")
st.write("Upload the transaction excel file")

# Custom CSS for file upload boxes
st.markdown("""
    <style>
        .big-box {
            border: 2px dashed #ccc;
            padding: 30px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
            border-radius: 10px;
            background-color: #f9f9f9;
        }
        .st-emotion-cache-16txtl3 {
            max-width: 100% !important;
        }
    </style>
""", unsafe_allow_html=True)


file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"], key="transactions")

# Ensure the file is uploaded
if file:
    # Load the file into a Pandas DataFrame
    df = pd.read_excel(file, header=None)

    cleaned_df = clean_df(df)

    # # Display the DataFrame
    # st.write(cleaned_df.head())

    output = generate_report(cleaned_df)

    st.download_button(
        label="📥 Download Report",
        data=output,
        file_name="Transactions_Summary.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )