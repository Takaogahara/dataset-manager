import streamlit as st
from .core.structure import Sidebar, MainStructure, IO


def _convert(uploaded_file):
    dataframe = IO.sb_sdf_read_dataframe(uploaded_file)

    try:
        columns = Sidebar.sb_columns_selector(dataframe)
    except st.errors.StreamlitAPIException:
        columns = Sidebar.sb_columns_selector(dataframe)

    number = Sidebar.sb_data_limit(dataframe)

    dataframe = MainStructure.data_selection_preview(dataframe,
                                                     number,
                                                     columns)

    MainStructure.download_button(dataframe, name="dataframe")


def converter():
    uploaded_file = None
    uploaded_file = Sidebar.sb_sdf_uploader("Upload your file",
                                            "Upload your input SDF file")

    if uploaded_file is None:
        MainStructure.awating_upload()
    else:
        _convert(uploaded_file)
