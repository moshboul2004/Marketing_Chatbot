import streamlit as st
from app.model.analytics_model import show_analytics
from app.util.pdf_generator import create_pdf_from_text

def handle_analytics(uploaded_file):
    if uploaded_file is not None:
        df, insights = show_analytics(uploaded_file)

        if df is not None:
            st.write("Data Preview:")
            st.dataframe(df)

            st.write("Insights:")
            st.text(insights)

            pdf_buffer = create_pdf_from_text(insights)

            return pdf_buffer
            

        else:
            st.error("Failed to process the CSV file. Please upload a valid file with relevant marketing content.")