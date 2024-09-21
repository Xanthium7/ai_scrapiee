import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ai

# Set page config
st.set_page_config(page_title="Scrapiee >_<", page_icon="🕷️", layout="wide")

# Custom CSS for dark theme
st.markdown("""
<style>
    body {
        color: #FFFFFF;
        background-color: #0E1117;
    }
    .stTitle {
        color: #FFFFFF;
        font-size: 2.5rem !important;
        font-weight: 700;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    .stTextInput>div>div>input {
        background-color: #262730;
        color: #FFFFFF;
    }
    .stTextArea>div>div>textarea {
        background-color: #262730;
        color: #FFFFFF;
    }
    .stExpander {
        background-color: #262730;
        border-radius: 5px;
    }
    .streamlit-expanderHeader {
        color: #FFFFFF;
    }
    .stSuccess {
        background-color: #1E3D31;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.title("Scrapiee >_<")

# URL input
url = st.text_input("🌐 Enter a Website URL...",
                    placeholder="https://www.example.com")

if url == "" or "https://" not in url:
    st.warning("⚠️ Please enter a valid URL")
else:
    if st.button("🕷️ Scrape"):
        with st.spinner("Scraping the site..."):
            result = scrape_website(url)
            body_content = extract_body_content(result)
            clean_content = clean_body_content(body_content)

            st.session_state.dom_content = clean_content

        st.success("Scraping completed!")

        with st.expander("🔍 View DOM Content"):
            st.text_area("DOM Content", clean_content, height=300)

    if "dom_content" in st.session_state:
        parse_description = st.text_area("👩‍🌾 What must Scrapiee Scrape?")

        if st.button("⚗ Parse content"):
            with st.spinner("Parsing the content..."):
                dom_chunks = split_dom_content(st.session_state.dom_content)
                result = parse_with_ai(dom_chunks, parse_description)

            st.success("Parsing completed!")
            st.write(result)

# Footer
st.markdown("---")
