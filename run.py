import streamlit as st

from data_cleaner.cleaner_execute import cleaner
from data_selector.selector_execute import selector

# ----------------------------------------------------------------


class MultiApp:
    """Framework for combining multiple streamlit applications."""

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        # app = st.sidebar.radio(
        app = st.sidebar.selectbox("Navigation", self.apps,
                                   format_func=lambda app: app["title"])

        app["function"]()

# ----------------------------------------------------------------


app = MultiApp()

app.add_app("Dataset Selector", selector)
app.add_app("Dataset Cleaner", cleaner)

app.run()
