import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="Drug Side Effects Explorer", layout="wide")

st.title("💊 Drugs, Side Effects, and Medical Conditions Explorer")

# Upload CSV
uploaded_file = st.file_uploader("📁 Upload the 'drugs_side_effects_drugs_com.csv' file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Preprocessing
    df['activity'] = df['activity'].astype(str).str.replace('%', '').astype(float) / 100
    df['alcohol'] = df['alcohol'].fillna(0).replace({'X': 1})
    df['side_effects'] = df['side_effects'].fillna('Unknown')
    df['related_drugs'] = df['related_drugs'].fillna('Unknown')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0)
    df['no_of_reviews'] = pd.to_numeric(df['no_of_reviews'], errors='coerce').fillna(0)
    df['generic_name'] = df['generic_name'].fillna('Unknown')
    df['drug_classes'] = df['drug_classes'].fillna('Unknown')
    df['rx_otc'] = df['rx_otc'].fillna('Unknown')
    df['pregnancy_category'] = df['pregnancy_category'].fillna('Unknown')

    st.subheader("📊 Data Preview")
    st.dataframe(df.head())

    st.markdown("### 🔢 Distribution of Drug Ratings")
    fig1, ax1 = plt.subplots()
    sns.histplot(df['rating'], bins=10, kde=True, ax=ax1)
    st.pyplot(fig1)

    st.markdown("### 💡 Top Medical Conditions")
    st.bar_chart(df['medical_condition'].value_counts().head(10))

    st.markdown("### 🔍 Most Common Side Effects")
    side_effects = df['side_effects'].dropna().apply(lambda x: re.split(r';|,|\n', x)).explode().str.strip()
    st.bar_chart(side_effects.value_counts().head(10))

    st.markdown("### 📈 Ratings by Drug Class")
    top_classes = df['drug_classes'].value_counts().head(5).index.tolist()
    df_class = df[df['drug_classes'].isin(top_classes)]
    fig2, ax2 = plt.subplots()
    sns.boxplot(data=df_class, x='drug_classes', y='rating', ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    st.markdown("### 🧪 Filter by Condition")
    condition = st.selectbox("Select a Condition", sorted(df['medical_condition'].unique()))
    st.dataframe(df[df['medical_condition'] == condition])
else:
    st.info("Upload the CSV file to begin.")
