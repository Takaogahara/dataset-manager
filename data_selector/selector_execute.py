import streamlit as st
from .core.structure import Sidebar, MainStructure


def _selection(uploaded_file):
    default_columns = ["Molecule ChEMBL ID", "Molecular Weight",
                       "Smiles", "Standard Value",
                       "Standard Units", "Assay Organism"]
    dataframe = Sidebar.sb_read_dataframe(uploaded_file)

    try:
        columns = Sidebar.sb_columns_selection(dataframe,
                                               default_columns)
    except st.errors.StreamlitAPIException:
        columns = Sidebar.sb_columns_selection(dataframe)

    number = Sidebar.sb_data_limit(dataframe)

    dataframe = MainStructure.data_selection_preview(dataframe,
                                                     number,
                                                     columns)

    MainStructure.download_button(dataframe, "dataframe")


def selector():
    path = "./data_cleaner/core/example_csv.csv"
    uploaded_file = None
    uploaded_file = Sidebar.sb_csv_uploader("Upload your CSV data",
                                            "Upload your input CSV file",
                                            path)

    if uploaded_file is None:
        MainStructure.awating_upload()
    else:
        _selection(uploaded_file)
