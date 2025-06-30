import re
import csv


class DataCollector:
    operators = {
        "=": "==",
        "<": "<",
        ">": ">",
        "<=": "<=",
        ">=": ">=",
    }

    pattern_converter = r"^(.*?)(<=|>=|=|<|>)(.*)$"

    def __init__(self, args):
        self.__args_file = args.file
        self.__args_where = args.where
        self.__args_aggregate = args.aggregate
        self.__table_column_names = []
        self.__table_body_rows = []

    def __aggregator(self, aggregator: str, list):
        if aggregator == "min":
            return min(list)
        elif aggregator == "max":
            return max(list)
        elif aggregator == "avg":
            return sum(list) / len(list)
        else:
            return None

    def __convert_str_to_num(self, string: str):
        try:
            return int(string)
        except ValueError:
            return float(string)

    def __parse_args_to_list(self, arg_value: str, pattern):
        args_list = re.split(pattern, arg_value)
        args_list = [p.strip() for p in args_list if p.strip()]

        return args_list

    def set_table_data_from_file(self):
        if self.__args_file is None:
            return "No file provided"
        try:
            with open(self.__args_file) as csv_file:
                csv_reader = csv.reader(csv_file)
                csv_counter = 0

                # Generate list of rows and columns
                for csv_item in csv_reader:
                    if csv_counter == 0:
                        self.__table_column_names = csv_item
                    else:
                        self.__table_body_rows.append(csv_item)
                    csv_counter += 1

        except FileNotFoundError:
            print("No file found")
            return "No file found"

    def setup_where_arguments(self):
        where_args_list = self.__parse_args_to_list(
            self.__args_where, self.pattern_converter
        )
        column_index = self.__table_column_names.index(where_args_list[0])
        result_rows = []

        for row in self.__table_body_rows:
            is_right_column_string = f'"{row[column_index]}" {self.operators[where_args_list[1]]} "{where_args_list[2]}"'
            is_right_column = eval(is_right_column_string)

            if is_right_column:
                result_rows.append(row)

        self.__table_body_rows = result_rows

    def setup_aggregate_arguments(self):
        if len(self.__table_body_rows) == 0 or self.__table_body_rows == 0:
            print("No data to aggregate")
            return "No data to aggregate"

        aggregate_args_list = self.__parse_args_to_list(
            self.__args_aggregate, self.pattern_converter
        )

        column_index = self.__table_column_names.index(aggregate_args_list[0])

        list_to_aggregate = [
            self.__convert_str_to_num(row[column_index])
            for row in self.__table_body_rows
        ]

        aggregate_num = (
            self.__aggregator(aggregate_args_list[2], list_to_aggregate)
            if list_to_aggregate
            else None
        )

        if aggregate_num is None:
            print("\nWarning: Make sure your aggregator is correct \n")
            return "\nWarning: Make sure your aggregator is correct \n"

        self.__table_column_names = [aggregate_args_list[2]]
        self.__table_body_rows = [[str(aggregate_num)]]

    def get_result_table_header(self):
        return self.__table_column_names

    def get_result_table_body(self):
        return self.__table_body_rows
