import pandas as pd
import streamlit as st

from .core.structure import Sidebar, MainStructure, IO
from .core.process import Remover, Calc, Utils, Standardize


@st.cache
def _init_():
    path = "./csv_handler/core/files/cleaner_dummy.csv"
    sep = ","
    st.session_state['status'] = False

    return path, sep


def _process(path, sep):

    _ = Remover.remove_nan(path, sep)
    _ = Standardize.standardize_smiles(path, sep)
    _ = Remover.filter_elements(path, sep)
    _ = Remover.select_strains(path, sep)
    _ = Calc.select_threshold(path, sep)
    _ = Calc.check_duplicates_simple(path, sep)
    _ = Calc.check_duplicates(path, sep)
    _ = Utils.shuffle_rows(path, sep)


def cleaner():
    example_path = "./csv_handler/core/files/cleaner_example_csv.csv"
    path, sep = _init_()
    uploaded_file = None
    uploaded_file = Sidebar.sb_csv_uploader("Upload CSV data",
                                            "Upload input CSV file",
                                            example_path)

    if uploaded_file and not st.session_state['status']:
        uploaded = IO.sb_csv_read_dataframe(uploaded_file)
        if st.sidebar.button("Go!"):
            uploaded.to_csv(path, index=False, sep=sep)
            st.session_state['status'] = True

    if uploaded_file and st.session_state['status']:
        st.subheader('Data preview')
        matrix = st.empty()
        info = st.empty()

        _process(path, sep)

        dataframe = pd.read_csv(path, delimiter=sep)
        matrix.dataframe(dataframe)
        info.info(f"Dataset shape: {dataframe.shape}")

        MainStructure.download_button(dataframe, name="processed_dataframe")

    else:
        MainStructure.awating_upload()
