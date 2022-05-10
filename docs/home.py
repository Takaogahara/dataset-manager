import streamlit as st

from ._modules import sdf_converter, csv_selection, csv_cleaner, fp_calculator


def about():
    st.markdown("""## Modules:""")

    with st.expander("SDF Dataset Converter"):
        sdf_converter()

    with st.expander("CSV Dataset Selector"):
        csv_selection()

    with st.expander("CSV Dataset Cleaner"):
        csv_cleaner()

    with st.expander("Fingerprint Calculator"):
        fp_calculator()
