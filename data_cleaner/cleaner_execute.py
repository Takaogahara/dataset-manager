import pandas as pd
import streamlit as st

from .core.structure import Sidebar, MainStructure
from .core.process import Remover, Calc, Utils


@st.cache
def _init_():
    path = "./data_cleaner/core/dummy.csv"
    sep = ","
    st.session_state['status'] = False

    return path, sep


def _process(path, sep):

    _ = Remover.remove_nan(path, sep)
    _ = Remover.filter_elements(path, sep)
    _ = Remover.select_strains(path, sep)
    _ = Calc.select_threshold(path, sep)
    _ = Calc.check_duplicates(path, sep)
    _ = Utils.shuffle_rows(path, sep)


def cleaner():
    path = "./data_cleaner/core/example_csv.csv"
    path, sep = _init_()
    uploaded_file = None
    uploaded_file = Sidebar.sb_csv_uploader("Upload CSV data",
                                            "Upload input CSV file",
                                            path)

    if uploaded_file and not st.session_state['status']:
        uploaded = Sidebar.sb_read_dataframe(uploaded_file)
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

        MainStructure.download_button(dataframe, "processed_dataframe")

    else:
        MainStructure.awating_upload()
