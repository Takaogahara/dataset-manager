import streamlit as st

from docs.home import about
from csv_handler.cleaner_execute import cleaner
from csv_handler.selector_execute import selector
from sdf_handler.sdf_converter import converter
from csv_handler.PaDEL_execute import PaDEL_calc


# ----------------------------------------------------------------
class MultiApp:
    """Framework for combining multiple streamlit applications."""

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        app = st.sidebar.selectbox("Navigation", self.apps,
                                   format_func=lambda app: app["title"])

        app["function"]()

# ----------------------------------------------------------------


app = MultiApp()

app.add_app("About", about)
app.add_app("SDF Dataset Converter", converter)
app.add_app("CSV Dataset Selector", selector)
app.add_app("CSV Dataset Cleaner", cleaner)
app.add_app("Fingerprint Calculator", PaDEL_calc)

app.run()
