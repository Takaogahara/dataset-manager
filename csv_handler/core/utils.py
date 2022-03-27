from collections import defaultdict


def _get_duplicates(seq):
    tally = defaultdict(list)
    for i, item in enumerate(seq):
        tally[item].append(i)
    target = ((key, locs) for key, locs in tally.items() if len(locs) > 1)

    duplicated = {}
    for item in target:
        duplicated[item[0]] = item[1]

    return duplicated


def process_duplicates(df, columns):
    remove_idx = []

    if len(columns) == 1:
        df = df.drop_duplicates(subset=columns, keep="first")

    else:
        list_id = list(df[columns[0]])
        list_activity = list(df[columns[1]])
        list_values = list(df[columns[2]])

        duplicated = _get_duplicates(list_id)

        if len(duplicated) >= 1:
            for mol_id in duplicated.keys():
                temp_activity = []
                temp_value = []

                for list_idx in duplicated[mol_id]:
                    temp_activity.append(list_activity[list_idx])
                    temp_value.append(list_values[list_idx])

                # Entry has same activity?
                if len(_get_duplicates(temp_activity)) != 1:
                    for activity_iter in duplicated[mol_id]:
                        remove_idx.append(activity_iter)

                # Get entry with higher value
                max_index = duplicated[mol_id][temp_value.index(
                    max(temp_value))]
                for value_iter in duplicated[mol_id]:
                    if value_iter != max_index:
                        remove_idx.append(value_iter)

            # Select keeped entrys
            keep_flag = [True] * len(df)
            for remove_iter in remove_idx:
                keep_flag[remove_iter] = False

            df = df[keep_flag]

    return df


def convert_threshold(df, threshold_value, threshold_unit, threshold_columns):
    allowed_units = ["ug.mL-1", "nM", "uM"]
    df = df[df[str(threshold_columns[1])].isin(allowed_units)]

    list_units = list(df[threshold_columns[1]])
    list_values = list(df[threshold_columns[0]])
    list_molweight = list(df[threshold_columns[2]])

    converted_values = []

    if threshold_unit == "uM":
        for unit_index, current_unit in enumerate(list_units):
            if current_unit == "ug.mL-1":
                new_value = ((list_values[unit_index] /
                              list_molweight[unit_index]) * 1000) * 1000
            elif current_unit == "uM":
                new_value = list_values[unit_index]
            elif current_unit == "nM":
                new_value = list_values[unit_index] / 1000

            converted_values.append(new_value)

        # Create activity column
        converted_units = ["uM"] * len(list_values)
        converted_activity = ["Inactive"] * len(list_values)

        for value_index, current_value in enumerate(converted_values):
            if current_value < threshold_value:
                converted_activity[value_index] = "Active"

        df = df.assign(converted_values=converted_values)
        df = df.assign(converted_units=converted_units)
        df = df.assign(converted_activity=converted_activity)

        df = df.rename(columns={"converted_values": "Converted Value",
                                "converted_units": "Converted Units",
                                "converted_activity": "Activity"})

    elif threshold_unit == "nM":
        for current_index, current_unit in enumerate(list_units):
            if current_unit == "ug.mL-1":
                new_value = (list_values[current_index] /
                             list_molweight[current_index]) * 1000
            elif current_unit == "uM":
                new_value = list_values[current_index] * 1000
            elif current_unit == "nM":
                new_value = list_values[current_index]

            converted_values.append(new_value)

        converted_units = ["nM"] * len(list_values)
        converted_activity = ["Inactive"] * len(list_values)

        for current_value_index, current_value in enumerate(converted_values):
            if current_value < threshold_value:
                converted_activity[current_value_index] = "Active"

        df["Converted Value"] = converted_values
        df["Converted Units"] = converted_units
        df["Activity"] = converted_activity

    return df
