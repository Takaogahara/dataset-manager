"""
Streamlit structure

version: 1.1.0
date: 04/01/2022
"""


from rdkit.Chem.PandasTools import LoadSDF
import streamlit as st
import pandas as pd
import os
import subprocess


def csv_download(dataframe, file_name: str, disp_text: str, sidebar=True):
    """Provide dataframe for download

    Args:
        dataframe (DataFrame): Dataframe to be dowloaded
        file_name (str): Displayed name
        disp_text (str): Displayed text

    Returns:
        Download: Download event
    """
    csv = dataframe.to_csv(index=False, encoding="utf-8")

    if sidebar:
        st.sidebar.download_button(label=disp_text,
                                   data=csv,
                                   file_name=f"{file_name}.csv",
                                   mime="text/csv",)
    else:
        st.download_button(label=disp_text,
                           data=csv,
                           file_name=f"{file_name}.csv",
                           mime="text/csv",)


def generic_download(file, mime: str, file_name: str,
                     disp_text: str, sidebar=True):
    """Provide dataframe for download

    Args:
        file (): file to be dowloaded
        file_name (str): Displayed name
        disp_text (str): Displayed text

    Returns:
        Download: Download event
    """

    if sidebar:
        st.sidebar.download_button(label=disp_text,
                                   data=file,
                                   file_name=file_name,
                                   mime=mime,)
    else:
        st.download_button(label=disp_text,
                           data=file,
                           file_name=file_name,
                           mime=mime,)


def run_PaDEL(padel_path: str, data_path: str, selected_fp: str):
    """Run PaDEL sub process

    Args:
        padel_path (str): Path to PaDEL folder
        data_path (str): Path to data folder
        selected_fp (str): Selected fingerprint file to calc

    Returns:
        str: Path to fingerprint CSV file
    """
    smi_path = data_path + "/molecule.smi"
    out_file = data_path + "/fingerprint.csv"

    jar_path = padel_path + "/PaDEL-Descriptor.jar"
    descriptor_path = padel_path + f"/{str(selected_fp)}"

    options = "-removesalt -standardizenitro -fingerprints"

    bashCommand = (f"java -Xms2G -Xmx2G -Djava.awt.headless=true "
                   f"-jar {jar_path} {options} "
                   f"-descriptortypes {descriptor_path} "
                   f"-dir {smi_path} -file {out_file}")

    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    os.remove(f"{smi_path}")

    return out_file


class IO:
    def sb_csv_read_dataframe(file):
        """Load UploadedFile CSV into pandas dataframe

        Args:
            file (UploadedFile): File to be loaded

        Returns:
            DataFrame: loaded dataframe
        """
        with st.sidebar.header("""Please select the CSV delimiter"""):
            delimiter_dict = {",": ",", ";": ";"}
            user_delimiter = st.sidebar.selectbox("Choose CSV file delimiter",
                                                  list(delimiter_dict.keys()))
            selected_delimiter = delimiter_dict[user_delimiter]

            try:
                dataframe = pd.read_csv(file, delimiter=selected_delimiter)
            except pd.errors.ParserError:
                st.error("Plese check your selected delimiter")
                dataframe = []

            return dataframe

    def sb_sdf_read_dataframe(file):
        """Load SDF UploadedFile into pandas dataframe

        Args:
            file (UploadedFile): File to be loaded

        Returns:
            DataFrame: loaded dataframe
        """
        dataframe = LoadSDF(file, smilesName="SMILES", molColName=None)

        if dataframe.shape == (0, 0):
            st.error("Plese check your selected data")
            dataframe = []

        return dataframe


class Sidebar:
    def sb_csv_uploader(field_description: str = "Title",
                        file_description: str = "Description",
                        example_path=None,
                        example_delimiter=",",
                        example_name="example_csv",
                        example_description="Download example CSV file"):
        """Create uploader element in sidebar for CSV files

        Args:
            field_description (str): Uploader title
            file_description (str): Uploader description
            example_path (str): Path to exemple file
            example_delimiter (str): Exemple file delimiter
            example_name (str): Exemple file name
            example_description (str): Exemple file description

        Returns:
            UploadedFile: Uploaded CSV file
        """
        with st.sidebar.header(field_description):
            uploaded_file = st.sidebar.file_uploader(file_description,
                                                     type=["csv"])

            if example_path:
                exemple_file = pd.read_csv(
                    example_path, delimiter=example_delimiter)

                csv_download(exemple_file, example_name, example_description)

        return uploaded_file

    def sb_sdf_uploader(field_description: str = "Title",
                        file_description: str = "Description"):
        """Create uploader element in sidebar for CSV files

        Args:
            field_description (str): Uploader title
            file_description (str): Uploader description

        Returns:
            UploadedFile: Uploaded SDF file
        """
        with st.sidebar.header(field_description):
            uploaded_file = st.sidebar.file_uploader(file_description,
                                                     type=["sdf"])

        return uploaded_file

    def sb_columns_selector(dataframe, default: list = None):
        """Desired columns selector

        Args:
            dataframe (DataFrame): Original dataframe
            defaut (list, optional): Default selection. Defaults to None.

        Returns:
            pandas Dataframe: Dataframe with desired columns selected
        """
        with st.sidebar.header("""Select desired columns"""):
            text = "Select desired columns"
            columns_name = list(dataframe.columns)
            if default:
                molecule_column = st.sidebar.multiselect(text, columns_name,
                                                         default)
            else:
                molecule_column = st.sidebar.multiselect(text, columns_name)

            return molecule_column

    def sb_data_limit(dataframe):
        """Select data number to work with

        Args:
            dataframe (DataFrame): Original dataframe

        Returns:
            int: selection number
        """
        number = st.sidebar.slider("Compute N data",
                                   min_value=10,
                                   max_value=dataframe.shape[0],
                                   value=dataframe.shape[0], step=10)

        return number

    def sb_run(execute: bool):
        """Control execution status

        Args:
            execute (bool): Execution flag (True/False)

        Returns:
            bool: Execution flag
        """
        with st.sidebar.header("Run"):
            if st.sidebar.button("Execute"):
                execute = not execute
                return execute

    def sb_download_button(data, mime, name="file",
                           description="Download data"):
        """Create download button on sidebar

        Args:
            data (): data to be downloaded
            name (str): download file name
            description (str): displayed text

        """
        if mime == "text/csv":
            csv_download(data, name, description, True)
        else:
            generic_download(data, mime, name, description, True)


class MainStructure:
    def awating_upload():
        """Create structure to display while waiting"""
        with st.container():
            st.markdown("""## Awaiting file to be uploaded""")
            st.markdown("""Please use the sidebar menu to upload.""")

    def data_selection_preview(dataframe, display_nbr, columns):
        """Preview current selection of columns

        Args:
            dataframe ([type]): [description]
            display_nbr ([type]): [description]
            columns ([type]): [description]

        Returns:
            DataFrame: Selected dataframe
        """
        try:
            df = dataframe.iloc[:display_nbr, :]
            sel_dataframe = df[columns]

            st.subheader("Data selected")
            st.write(sel_dataframe)

            return sel_dataframe
        except ValueError:
            st.error("""Plase check your data or column selection""")

    def download_button(data, mime="text/csv", name="file",
                        description="Download data"):
        """Create download button on main structure

            Args:
            data (DataFrame): dataframe to be downloaded
            name (str): download file name
            description (str): displayed text
            """
        if mime == "text/csv":
            csv_download(data, name, description, False)
        else:
            generic_download(data, mime, name, description, False)


class Fingerprint:
    def fp_columns_selection(dataframe):
        """Column selection for PaDEL

        Args:
            dataframe (DataFrame): Dataframe

        Returns:
            list: Selected columns
        """
        with st.sidebar.header("""Select the Molecule ID and SMILES column"""):
            index_columns = list(dataframe.columns)

            if (("Molecule ChEMBL ID" in index_columns) and
                    ("Smiles" in index_columns)):
                molecule_column = "Molecule ChEMBL ID"
                st.sidebar.write(f"Auto selection: {molecule_column}")

                smiles_column = "Smiles"
                st.sidebar.write(f"Auto selection: {smiles_column}")

            else:
                molecule_column = st.sidebar.selectbox("Molecule ID",
                                                       index_columns,
                                                       index=0)
                smiles_column = st.sidebar.selectbox("SMILES", index_columns,
                                                     index=1)

            target_column = [molecule_column, smiles_column]

            return target_column

    def fp_selection(dataframe):
        """Fingerprint selection for PaDEL

        Args:
            dataframe (DataFrame): Dataframe

        Returns:
            list: Selected fingerprint
            int: Number of seected molecules
        """
        with st.sidebar.header("Set parameters"):
            fp_dict = {"AtomPairs2D": "AtomPairs2DFingerprinter.xml",
                       "AtomPairs2DCount": "AtomPairs2DFingerprintCount.xml",
                       "CDK": "Fingerprinter.xml",
                       "CDKextended": "ExtendedFingerprinter.xml",
                       "CDKgraphonly": "GraphOnlyFingerprinter.xml",
                       "EState": "EStateFingerprinter.xml",
                       "KlekotaRoth": "KlekotaRothFingerprinter.xml",
                       "KlekotaRothCount": "KlekotaRothFingerprintCount.xml",
                       "MACCS": "MACCSFingerprinter.xml",
                       "PubChem": "PubchemFingerprinter.xml",
                       "Substructure": "SubstructureFingerprinter.xml",
                       "SubstructureCount": "SubstructureFingerprintCount.xml"}

        user_fp = st.sidebar.selectbox("Choose fingerprint to calculate",
                                       list(fp_dict.keys()))

        dict_fp = fp_dict[user_fp]

        molecule_number = st.sidebar.slider("Compute N molecules",
                                            min_value=10,
                                            max_value=dataframe.shape[0],
                                            value=dataframe.shape[0], step=10)

        return [user_fp, dict_fp], molecule_number

    def execute_PaDEL(dataframe, selected_fp: list):
        """Execute PaDEL

        Args:
            dataframe (DataFrame): Dataframe
            selected_fp (list): Fingerprint selection

        Returns:
            DataFrame: Fingerprint dataframe
        """
        _, dict_fp = selected_fp
        dataframe.to_csv("./csv_handler/core/files/molecule.smi", sep="\t",
                         header=False, index=False)

        with st.spinner("Calculating descriptors..."):
            fp_dir = run_PaDEL("./csv_handler/PaDEL-Descriptor",
                               "./csv_handler/core/files", dict_fp)

            return fp_dir

    def display_fingerprints(fp_path: str, selected_fp: list):
        """Display final result

        Args:
            fp_path (str): Path to fingerprint CSV file
            selected_fp (list): Fingerprint selection
        """
        user_fp, _ = selected_fp

        fingerprint_df = pd.read_csv(fp_path)
        n_molecules = fingerprint_df.shape[0]
        n_descriptors = fingerprint_df.shape[1]

        st.success(f"Selected fingerprint: {user_fp}")
        st.success(f"Number of molecules: {str(n_molecules)}")
        st.success(f"Number of descriptors: {str(n_descriptors-1)}")

        st.subheader("PADEL output file")
        st.write(fingerprint_df)
