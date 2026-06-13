import streamlit as st
import requests

st.set_page_config(
    page_title="News Dashboard",
    page_icon="📰",
    layout="wide"
)

st.title("📰 News Dashboard")

# API KEY
API_KEY = st.secrets["NEWS_API_KEY"]

BASE_URL = "https://newsapi.org/v2/top-headlines"

# Sidebar
st.sidebar.header("Filters")

country_map = {
    "India": "in",
    "USA": "us",
    "UK": "gb",
    "Australia": "au"
}

country_name = st.sidebar.selectbox(
    "Country",
    list(country_map.keys())
)

category = st.sidebar.selectbox(
    "Category",
    [
        "business",
        "entertainment",
        "general",
        "health",
        "science",
        "sports",
        "technology"
    ]
)

keyword = st.sidebar.text_input("Search Keyword")

articles_count = st.sidebar.slider(
    "Number of Articles",
    1,
    20,
    10
)

if st.sidebar.button("Fetch News"):

    params = {
        "apiKey": API_KEY,
        "country": country_map[country_name],
        "category": category,
        "pageSize": articles_count
    }

    try:

        response = requests.get(BASE_URL, params=params)

        st.subheader("Debug Information")

        st.write("Status Code:", response.status_code)

        data = response.json()

        st.write(data)

        if response.status_code != 200:
            st.error("API Error")
            st.stop()

        articles = data.get("articles", [])

        if keyword:
            articles = [
                article for article in articles
                if keyword.lower()
                in (
                    str(article.get("title", "")) +
                    str(article.get("description", ""))
                ).lower()
            ]

        st.success(f"{len(articles)} Articles Found")

        for article in articles:

            st.subheader(article.get("title", "No Title"))

            if article.get("urlToImage"):
                st.image(article["urlToImage"])

            st.write(
                article.get(
                    "description",
                    "No description available"
                )
            )

            if article.get("url"):
                st.link_button(
                    "Read Full Article",
                    article["url"]
                )

            st.divider()

    except Exception as e:
        st.error(str(e))