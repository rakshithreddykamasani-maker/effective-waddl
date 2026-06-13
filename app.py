import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET

st.set_page_config(
    page_title="Advanced News Dashboard",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Advanced News Dashboard")
st.markdown("Latest News Headlines")

rss_feeds = {
    "World": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "Business": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    "Technology": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "Sports": "https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml"
}

st.sidebar.header("Filters")

category = st.sidebar.selectbox(
    "Category",
    list(rss_feeds.keys())
)

keyword = st.sidebar.text_input(
    "Search Keyword"
)

num_articles = st.sidebar.slider(
    "Number of Articles",
    5,
    30,
    10
)

if st.sidebar.button("Fetch News"):

    try:
        response = requests.get(rss_feeds[category])

        root = ET.fromstring(response.content)

        articles = []

        for item in root.findall(".//item"):

            title = item.find("title").text if item.find("title") is not None else ""

            link = item.find("link").text if item.find("link") is not None else ""

            description = (
                item.find("description").text
                if item.find("description") is not None
                else ""
            )

            articles.append({
                "title": title,
                "description": description,
                "link": link
            })

        if keyword:
            articles = [
                a for a in articles
                if keyword.lower() in (
                    a["title"] + a["description"]
                ).lower()
            ]

        articles = articles[:num_articles]

        st.success(f"{len(articles)} Articles Found")

        for article in articles:

            st.subheader(article["title"])

            st.write(article["description"])

            st.link_button(
                "Read Full Article",
                article["link"]
            )

            st.divider()

    except Exception as e:
        st.error(str(e))