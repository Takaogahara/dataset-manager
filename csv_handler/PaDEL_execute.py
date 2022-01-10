from .core.structure import Sidebar, MainStructure, IO, Fingerprint


def PaDEL_calc():
    path = "./csv_handler/core/files/cleaner_dummy.csv"
    uploaded_file = None
    uploaded_file = Sidebar.sb_csv_uploader("Upload your CSV data",
                                            "Upload your input CSV file",
                                            path)

    if uploaded_file is None:
        MainStructure.awating_upload()
        execute_status = False

    else:
        execute_status = False
        dataframe = IO.sb_csv_read_dataframe(uploaded_file)
        columns = Fingerprint.fp_columns_selection(dataframe)
        selected_fp, mol_nbr = Fingerprint.fp_selection(dataframe)

        dataframe = MainStructure.data_selection_preview(dataframe, mol_nbr,
                                                         columns)
        execute_status = Sidebar.sb_run(execute_status)

    if execute_status:
        execute_status = False
        fingerprint = Fingerprint.execute_PaDEL(dataframe, selected_fp)
        Fingerprint.display_fingerprints(fingerprint, selected_fp)
