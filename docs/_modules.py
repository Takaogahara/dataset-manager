import streamlit as st


def sdf_converter():
    st.markdown("""
    ### SDF Dataset Converter

    This module allows converting SDF files to CSV files.
    """)


def csv_selection():
    st.markdown("""
    ### CSV Dataset Selector

    This module allows the selection of specific columns in
    the dataset to be saved.
    """)


def csv_cleaner():
    st.markdown("""
    ### CSV Dataset Cleaner

    This module allows you to perform various operations on the dataset.

    These operations are:
    """)

    col1_df, col2_df = st.columns(2)

    col1_df.markdown("""
    - Remove NaN values
    - Filter molecules by elements
    - Filter molecules by assay organism
    """)

    col2_df.markdown("""
    - Standardize concentration units and determine activity
    - Remove duplicate entries
    - Shuffle dataset
    """)

    st.markdown("""
    Remarks:

    - Some operations require a specific order of column selection.
    - Currently filtering molecules by elements keeps molecules containing
    **ONLY**: `C`, `O`, `N`, `S`, `P`, `F`, `I`, `Br`, `Cl`.
    - Standardize concentration units and determining activity works only with
    the **INPUT** values: `ug.mL-1`,` uM`, `nM`.
    - Standardize concentration units and determining activity works only with
    the **OUTPUT** values: ` uM`, `nM`.

    """)


def fp_calculator():
    st.markdown("""
    ### Fingerprint Calculator

    This module allows the calculation of ** 2D molecular fingerprints** used
    in computational drug discovery projects such as for the construction of
    quantitative structure-activity/property relationship (QSAR/QSPR) models.

    There are 12 **molecular fingerprints** avaliable:
    """)

    col1_fp, col2_fp, col3_fp = st.columns(3)

    col1_fp.markdown("""
    - `AtomPairs2D`
    - `AtomPairs2DCount`
    - `CDK`
    - `CDKextended`
    """)

    col2_fp.markdown("""
    - `CDKgraphonly`
    - `EState`
    - `KlekotaRoth`
    - `KlekotaRothCount`
    """)

    col3_fp.markdown("""
    - `MACCS`
    - `PubChem`
    - `Substructure`
    - `SubstructureCount`
    """)
