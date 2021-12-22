"""
Streamlit structure

v - 1.0.0
"""


from rdkit.Chem.PandasTools import LoadSDF
import streamlit as st
import pandas as pd


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
        dataframe = LoadSDF(file, smilesName='SMILES', molColName=None)

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
