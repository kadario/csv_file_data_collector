from tabulate import tabulate
import argparse

from data_collector import DataCollector


class MainClass:
    def __init__(self):
        self._args = None
        self._collector = None

    def __setup_parser_args(self, args=None):
        parser = argparse.ArgumentParser(description="Parsing CSV file")

        parser.add_argument("-f", "--file", help="Add csv file to parse")
        parser.add_argument("-w", "--where", help="Filter data tables by arguments")
        parser.add_argument(
            "-a", "--aggregate", help="Aggregate data tables by arguments"
        )

        return parser.parse_args(args)

    def __setup_args_data(self):
        self._collector.set_table_data_from_file()

        if self._args.file:
            if self._args.where:
                # Collector setup filter
                self._collector.setup_where_arguments()

            if self._args.aggregate:
                # Collector setup aggregator
                self._collector.setup_aggregate_arguments()

    def prepare_data(self, args=None):
        self._args = self.__setup_parser_args(args)
        self._collector = DataCollector(self._args)
        self.__setup_args_data()

    def print_result(self):
        if self._args.file is None:
            print("No file provided")
            return "No file provided"
        else:
            if len(self._collector.get_result_table_body()) == 0:
                print("No data found")
                return "No data found"
            else:
                result_table = tabulate(
                    self._collector.get_result_table_body(),
                    headers=self._collector.get_result_table_header(),
                )

                print(result_table)
