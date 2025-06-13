import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Query Tool", layout="wide")

st.title(" CSV Sheet Query & Analysis Tool")
with st.expander("How it works"):
    st.markdown("""
Here's how to use it:

1. **Upload your CSV file**
   - Go to FILE->Export-> Download as CSV UTF-8 file
   - Click the uploader and select your file.
   - The tool expects the actual column headers to be on the second row of the file.(as in the original file)

2. **Preview your data**
   - You’ll see a few rows from the file to confirm it loaded correctly.

3. **Ask a question**
   - Choose a question type from the dropdown.
   - Enter a company name, country, or keyword depending on your question.

4. **View results**
   - The tool shows how many matching projects were found.
   - It also lists all the matching rows in a table.

5. **See full data (optional)**
   - You can open the full table at the bottom to see all the data.
    """)

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Header is on second row (index 1)
    df = pd.read_csv(uploaded_file, header=1)

    # Normalize column names
    df.columns = df.columns.str.strip().str.title()

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    st.subheader("🔍 Ask a Question")

    query_type = st.selectbox("Select a query type", [
        "How many projects done for a company?",
        "Which is the last project done in a country?",
        "How many projects done on a topic (keyword)?"
    ])

    if query_type == "How many projects done for a company?":
        company = st.text_input("Enter company name (e.g., Tata Chemicals)")
        if company:
            matching_rows = df[df["Company"].str.lower() == company.lower()]
            count = len(matching_rows)
            st.success(f"{count} project(s) done for {company}")
            if count > 0:
                st.write("### Matching Projects:")
                st.dataframe(matching_rows)

    elif query_type == "Which is the last project done in a country?":
        country = st.text_input("Enter country (e.g., China)")
        if country:
            filtered = df[df["Country"].str.lower() == country.lower()]
            if not filtered.empty:
                last_project = filtered.sort_values("Year", ascending=False).iloc[0:1]
                st.success(f"Last project in {country}:")
                st.dataframe(last_project)
            else:
                st.warning(f"No projects found in {country}")

    elif query_type == "How many projects done on a topic (keyword)?":
        keyword = st.text_input("Enter topic keyword (e.g., Customer satisfaction)").lower()
        if keyword:
            keyword_cols = ['Keyword1', 'Keyword2', 'Keyword3', 'Keyword4']
            match_mask = df[keyword_cols].apply(lambda x: x.astype(str).str.lower().str.contains(keyword)).any(axis=1)
            matching_rows = df[match_mask]
            count = len(matching_rows)
            st.success(f"{count} project(s) found on topic '{keyword}'")
            if count > 0:
                st.write("### Matching Projects:")
                st.dataframe(matching_rows)

    # Optional full table view
    with st.expander("📁 Full Data Table"):
        st.dataframe(df)

else:
    st.info("Please upload a CSV file to get started.")
