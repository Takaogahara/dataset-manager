import pandas as pd
from rdkit import Chem
import streamlit as st
from tqdm import tqdm
from chembl_structure_pipeline import standardizer

from .utils import convert_threshold, process_duplicates


class Utils:
    def shuffle_rows(path: str, delimiter=","):
        """Shuffle rows

        Args:
            path (str): path to csv file
            delimiter (str, optional): cvs file delimiter. Defaults to ",".

        Returns:
            bool: execution flag
        """
        with st.expander("Shuffle rows"):
            st.markdown("""###### Shuffle rows""")
            dataframe = pd.read_csv(path, delimiter=delimiter)

            if st.button("Shuffle"):
                shuffle = dataframe.sample(frac=1)

                shuffle.to_csv(path, index=False, sep=delimiter)
                return True

            else:
                return False


class Remover:
    def remove_nan(path: str, delimiter=","):
        """Remove rows with NaN values

        Args:
            path (str): path to csv file
            delimiter (str, optional): cvs file delimiter. Defaults to ",".

        Returns:
            bool: execution flag
        """
        with st.expander("Remove NaN"):
            st.markdown("""###### Remove NaN""")
            dataframe = pd.read_csv(path, delimiter=delimiter)

            if st.button("Remove NaN"):
                drop = dataframe.dropna(inplace=False)

                counter = dataframe.shape[0] - drop.shape[0]
                st.write(f"Rows removed: {counter}")
                drop.to_csv(path, index=False, sep=delimiter)
                return True

            else:
                return False

    def remove_outlier(path: str, delimiter=","):
        """Remove outliers

        Args:
            path (str): path to csv file
            delimiter (str, optional): cvs file delimiter. Defaults to ",".

        Returns:
            bool: execution flag
        """
        with st.expander("Remove Outliers"):
            st.markdown("""###### Remove Outliers""")
            dataframe = pd.read_csv(path, delimiter=delimiter)

            if st.button("Remove Outliers"):
                shape_init = dataframe.shape[0]

                dataframe = dataframe[(dataframe["Labels"] > dataframe[
                    "Labels"].quantile(0.1)) & (dataframe[
                        "Labels"] < dataframe["Labels"].quantile(0.9))]

                counter = shape_init - dataframe.shape[0]
                st.write(f"Rows removed: {counter}")
                dataframe.to_csv(path, index=False, sep=delimiter)
                return True

            else:
                return False

    def select_strains(path: str, delimiter=","):
        """Shuffle rows

        Args:
            path (str): path to csv file
            delimiter (str, optional): cvs file delimiter. Defaults to ",".

        Returns:
            bool: execution flag
        """
        with st.expander("Filter Organism"):
            st.markdown("""###### Filter Organism""")
            dataframe = pd.read_csv(path, delimiter=delimiter)

            try:
                organism_column = st.selectbox("Organism Column",
                                               ["Assay Organism"])
                unique_organism = dataframe[organism_column].unique()
                selected_organism = st.multiselect("Select target organisms",
                                                   unique_organism)
            except KeyError:
                df_columns = list(dataframe.columns)
                organism_column = st.selectbox("Organism Column", df_columns)
                unique_organism = dataframe[organism_column].unique()
                selected_organism = st.multiselect("Select target organisms",
                                                   unique_organism)

            shape = dataframe.shape[0]

            if st.button("Filter Organism"):
                dataframe = dataframe[dataframe[str(organism_column)].isin(
                    list(selected_organism))]

                counter = shape - dataframe.shape[0]
                st.write(f"Rows removed: {counter}")
                dataframe.to_csv(path, index=False, sep=delimiter)
                return True

            else:
                return False

    def filter_elements(path: str, delimiter=","):
        """Filter SMILES elements

        Args:
            path (str): path to csv file
            delimiter (str, optional): cvs file delimiter. Defaults to ",".

        Returns:
            bool: execution flag
        """
        with st.expander("Filter Elements"):
            st.markdown("""###### Filter Elements""")
            dataframe = pd.read_csv(path, delimiter=delimiter)

            try:
                smiles_column = st.selectbox("SMILES Column", ["Smiles"])
                smiles = dataframe[str(smiles_column)]
            except KeyError:
                df_columns = list(dataframe.columns)
                smiles_column = st.selectbox("SMILES Column", df_columns)
                smiles = dataframe[str(smiles_column)]

            if st.button("Filter Elements"):
                shape = dataframe.shape[0]
                valid_smiles = "C", "O", "N", "S", "P", "F", "I", "Br", "Cl"
                flag_list = []

                for current_smiles in smiles:
                    mol = Chem.MolFromSmiles(str(current_smiles))
                    valid_flag = True

                    for current_atom in mol.GetAtoms():
                        atom = current_atom.GetSymbol()

                        if atom in valid_smiles:
                            continue
                        else:
                            valid_flag = False

                    flag_list.append(valid_flag)

                dataframe = dataframe[flag_list]

                counter = shape - dataframe.shape[0]
                st.write(f"Rows removed: {counter}")
                dataframe.to_csv(path, index=False, sep=delimiter)
                return True

            else:
                return False


class Calc:
    def select_threshold(path: str, delimiter=","):
        """Calculate and select threshold for standard values

        Args:
            path (str): path to csv file
            delimiter (str, optional): cvs file delimiter. Defaults to ",".

        Returns:
            bool: execution flag
        """
        with st.expander("Select threshold"):
            st.markdown("""###### Select threshold""")
            st.markdown("""(Supported units: `ug.mL-1`, `nM`, `uM`)""")
            dataframe = pd.read_csv(path, delimiter=delimiter)
            shape = dataframe.shape[0]

            text = ("Select: Standard Value, Standard Units, "
                    "Molecular Weight (IN THIS ORDER)")
            default = ["Standard Value", "Standard Units", "Molecular Weight"]

            try:
                index_thr = list(dataframe.columns)
                selected_columns = st.multiselect(text, index_thr, default)

                units_dict = {"uM": "uM", "nM": "nM"}
                user_threshold_unit = st.selectbox("Choose unit for threshold",
                                                   list(units_dict.keys()))
                selected_unit = units_dict[user_threshold_unit]
            except st.errors.StreamlitAPIException:
                index_thr = list(dataframe.columns)
                selected_columns = st.multiselect(text, index_thr, None)

                units_dict = {"uM": "uM", "nM": "nM"}
                user_threshold_unit = st.selectbox("Choose unit for threshold",
                                                   list(units_dict.keys()))
                selected_unit = units_dict[user_threshold_unit]

            try:
                threshold_value = float(st.text_input("Threshold value",
                                                      "10.0"))
            except ValueError:
                st.error("Please provide a valid value. "
                         "(Decimal separator is '.')")

            if st.button("Convert values"):
                dataframe = convert_threshold(dataframe, threshold_value,
                                              selected_unit, selected_columns)

                counter = shape - dataframe.shape[0]
                st.write(f"Rows removed: {counter}")
                dataframe.to_csv(path, index=False, sep=delimiter)
                return True

            else:
                return False

    def check_duplicates(path: str, delimiter=","):
        """check and process duplicated data

        Args:
            path (str): path to csv file
            delimiter (str, optional): cvs file delimiter. Defaults to ",".

        Returns:
            bool: execution flag
        """
        with st.expander("Check duplicates"):
            st.markdown("""###### Check duplicates""")
            dataframe = pd.read_csv(path, delimiter=delimiter)
            shape = dataframe.shape[0]

            text = ("Select: Smiles, Activity, "
                    "Converted Value (IN THIS ORDER)")
            default = ["Smiles", "Activity", "Converted Value"]

            try:
                index_id = list(dataframe.columns)
                selected_duplicates = st.multiselect(text, index_id, default)
            except st.errors.StreamlitAPIException:
                index_id = list(dataframe.columns)
                selected_duplicates = st.multiselect(text, index_id, None)

            if st.button("Check duplicates"):
                dataframe = process_duplicates(dataframe, selected_duplicates)

                counter = shape - dataframe.shape[0]
                st.write(f"Rows removed: {counter}")
                dataframe.to_csv(path, index=False, sep=delimiter)
                return True

            else:
                return False

    def check_duplicates_simple(path: str, delimiter=","):
        """check and process duplicated data

        Args:
            path (str): path to csv file
            delimiter (str, optional): cvs file delimiter. Defaults to ",".

        Returns:
            bool: execution flag
        """
        with st.expander("Check duplicates (simple)"):
            st.markdown("""###### Check duplicates (simple)""")
            dataframe = pd.read_csv(path, delimiter=delimiter)
            shape = dataframe.shape[0]

            try:
                duplicate_col = [st.selectbox("Select Smiles column",
                                              ["Smiles"])]

            except KeyError:
                index_id = list(dataframe.columns)
                duplicate_col = [st.selectbox(
                    "Select Smiles column", index_id)]

            if st.button("Check simple duplicates"):
                dataframe = process_duplicates(dataframe, duplicate_col)

                counter = shape - dataframe.shape[0]
                st.write(f"Rows removed: {counter}")
                dataframe.to_csv(path, index=False, sep=delimiter)
                return True

            else:
                return False


class Standardize:
    def standardize_smiles(path: str, delimiter=","):
        with st.expander("Standardize SMILES"):
            st.markdown("""###### Standardize SMILES""")
            dataframe = pd.read_csv(path, delimiter=delimiter)
            shape = dataframe.shape[0]

            try:
                smiles_column = st.selectbox("Smiles Column", ["Smiles"])
                smiles = dataframe[str(smiles_column)]
            except KeyError:
                df_columns = list(dataframe.columns)
                smiles_column = st.selectbox("Smiles Column", df_columns)
                smiles = dataframe[str(smiles_column)]

            if st.button("Standardize SMILES"):

                std_list = []
                for current_smiles in tqdm(smiles):
                    mol = Chem.MolFromSmiles(str(current_smiles))

                    if mol is not None:
                        std_mol = standardizer.standardize_mol(mol)
                        parent_mol, _ = standardizer.get_parent_mol(std_mol)

                        if len(parent_mol.GetAtoms()) < 2:
                            std_list.append("remove")

                        else:
                            check = Chem.MolFromSmiles(
                                Chem.MolToSmiles((parent_mol)))

                            if check is not None:
                                std_list.append(Chem.MolToSmiles((parent_mol)))
                            else:
                                std_list.append("remove")

                    else:
                        std_list.append(Chem.MolToSmiles(parent_mol))

                dataframe[str(smiles_column)] = std_list

                for index, row in dataframe.iterrows():
                    if "." in row["Smiles"]:
                        dataframe.drop(index, inplace=True)

                    elif "remove" in row["Smiles"]:
                        dataframe.drop(index, inplace=True)

                counter = shape - dataframe.shape[0]
                st.write(f"Rows removed: {counter}")
                dataframe.to_csv(path, index=False, sep=delimiter)
                return True

            else:
                return False
