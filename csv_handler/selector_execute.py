import streamlit as st
from .core.structure import Sidebar, MainStructure, IO


def _selection(uploaded_file):
    default_columns = ["Molecule ChEMBL ID", "Molecular Weight",
                       "Smiles", "Standard Value",
                       "Standard Units", "Assay Organism"]
    dataframe = IO.sb_csv_read_dataframe(uploaded_file)

    try:
        columns = Sidebar.sb_columns_selector(dataframe,
                                              default_columns)
    except st.errors.StreamlitAPIException:
        columns = Sidebar.sb_columns_selector(dataframe)

    number = Sidebar.sb_data_limit(dataframe)

    dataframe = MainStructure.data_selection_preview(dataframe,
                                                     number,
                                                     columns)

    MainStructure.download_button(dataframe, name="dataframe")


def selector():
    path = "./csv_handler/core/files/selector_example_csv.csv"
    uploaded_file = None
    uploaded_file = Sidebar.sb_csv_uploader("Upload your CSV data",
                                            "Upload your input CSV file",
                                            path)

    if uploaded_file is None:
        MainStructure.awating_upload()
    else:
        _selection(uploaded_file)
