import streamlit as st
import requests

# API Configuration
API_KEY = st.secrets["NEWS_API_KEY"]
BASE_URL = "https://newsapi.org/v2/top-headlines"

st.set_page_config(
    page_title="News Dashboard",
    page_icon="📰",
    layout="wide"
)

st.title("📰 News Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Country",
    {
        "India": "in",
        "USA": "us",
        "UK": "gb",
        "Australia": "au"
    }
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

keyword = st.sidebar.text_input(
    "Search Keyword"
)

num_articles = st.sidebar.slider(
    "Number of Articles",
    5,
    20,
    10
)

if st.sidebar.button("Fetch News"):

    params = {
        "apiKey": API_KEY,
        "country": {
            "India": "in",
            "USA": "us",
            "UK": "gb",
            "Australia": "au"
        }[country],
        "category": category,
        "pageSize": num_articles
    }

    response = requests.get(BASE_URL, params=params)
    st.write("Status Code:", response.status_code)
st.write(response.json())

    if response.status_code == 200:

        data = response.json()

        articles = data.get("articles", [])

        if keyword:
            articles = [
                article
                for article in articles
                if keyword.lower() in (
                    str(article.get("title", "")) +
                    str(article.get("description", ""))
                ).lower()
            ]

        st.success(f"{len(articles)} Articles Found")

        for article in articles:

            st.subheader(article["title"])

            if article.get("urlToImage"):
                st.image(article["urlToImage"])

            st.write(article.get("description"))

            st.link_button(
                "Read More",
                article["url"]
            )

            st.divider()

    else:
        st.error("Failed to fetch news")