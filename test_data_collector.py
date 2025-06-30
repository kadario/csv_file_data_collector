import pytest
import argparse
from data_collector import DataCollector


def test_setup_aggregate_arguments_file():
    args = argparse.Namespace(file="example.csv", where="", aggregate="col1=max")
    collector = DataCollector(args)

    collector.set_table_data_from_file()

    assert collector._DataCollector__table_column_names is not None
    assert len(collector._DataCollector__table_body_rows) > 0


def test_setup_where_arguments_is_from_file():
    args = argparse.Namespace(file="example.csv", where="brand=apple", aggregate="")
    collector = DataCollector(args)
    collector.set_table_data_from_file()
    collector.setup_where_arguments()

    print(collector._DataCollector__table_body_rows)

    assert len(collector._DataCollector__table_body_rows) == 1
    assert collector._DataCollector__table_body_rows == [
        ["iphone 15 pro", "apple", "999", "4.9"]
    ]


def test_setup_where_arguments_is_from_file_less_equal():
    args = argparse.Namespace(file="example.csv", where="rating<=4.6", aggregate="")
    collector = DataCollector(args)
    collector.set_table_data_from_file()
    collector.setup_where_arguments()

    print(collector._DataCollector__table_body_rows)

    assert len(collector._DataCollector__table_body_rows) == 2
    assert collector._DataCollector__table_body_rows == [
        ["redmi note 12", "xiaomi", "199", "4.6"],
        ["poco x5 pro", "xiaomi", "299", "4.4"],
    ]


def test_setup_where_arguments_is_from_file_more_than_two():
    args = argparse.Namespace(file="example.csv", where="brand=xiaomi", aggregate="")
    collector = DataCollector(args)
    collector.set_table_data_from_file()
    collector.setup_where_arguments()

    print(collector._DataCollector__table_body_rows)


def test_setup_aggregate_arguments_is_from_file_avg():
    args = argparse.Namespace(
        file="example.csv", where="brand=xiaomi", aggregate="rating=avg"
    )
    collector = DataCollector(args)

    collector.set_table_data_from_file()
    collector.setup_where_arguments()
    collector.setup_aggregate_arguments()

    assert len(collector._DataCollector__table_body_rows) == 1
    assert collector._DataCollector__table_body_rows[0] == ["4.5"]


def test_setup_aggregate_arguments_is_from_file_min():
    args = argparse.Namespace(
        file="example.csv", where="brand=xiaomi", aggregate="rating=min"
    )
    collector = DataCollector(args)

    collector.set_table_data_from_file()
    collector.setup_where_arguments()
    collector.setup_aggregate_arguments()

    assert len(collector._DataCollector__table_body_rows) == 1
    assert collector._DataCollector__table_body_rows[0] == ["4.4"]


def test_setup_aggregate_arguments_is_from_file_max():
    args = argparse.Namespace(
        file="example.csv", where="brand=xiaomi", aggregate="rating=max"
    )
    collector = DataCollector(args)

    collector.set_table_data_from_file()
    collector.setup_where_arguments()
    collector.setup_aggregate_arguments()

    assert len(collector._DataCollector__table_body_rows) == 1
    assert collector._DataCollector__table_body_rows[0] == ["4.6"]


def test_setup_aggregate_arguments_no_data():
    args = argparse.Namespace(
        file="example.csv", where="brand=apple", aggregate="col1=max"
    )

    collector = DataCollector(args)
    result = collector.setup_aggregate_arguments()

    assert result == "No data to aggregate"


def test_setup_aggregate_arguments_invalid_aggregator():
    args = argparse.Namespace(
        file="example.csv", where="brand=apple", aggregate="col1=invalid"
    )
    collector = DataCollector(args)
    collector._DataCollector__table_body_rows = [["1"], ["2"], ["3"]]
    collector._DataCollector__table_column_names = ["col1"]

    result = collector.setup_aggregate_arguments()
    assert result == "\nWarning: Make sure your aggregator is correct \n"


def test_setup_aggregate_arguments_valid_max_aggregator():
    args = argparse.Namespace(
        file="example.csv", where="brand=apple", aggregate="col1=max"
    )
    collector = DataCollector(args)
    collector._DataCollector__table_body_rows = [["1"], ["2"], ["3"]]
    collector._DataCollector__table_column_names = ["col1"]

    collector.setup_aggregate_arguments()
    assert collector._DataCollector__table_column_names == ["max"]
    assert collector._DataCollector__table_body_rows == [["3"]]


def test_setup_aggregate_arguments_valid_min_aggregator():
    args = argparse.Namespace(
        file="example.csv", where="brand=apple", aggregate="col1=min"
    )
    collector = DataCollector(args)
    collector._DataCollector__table_body_rows = [["1"], ["2"], ["3"]]
    collector._DataCollector__table_column_names = ["col1"]

    collector.setup_aggregate_arguments()
    assert collector._DataCollector__table_column_names == ["min"]
    assert collector._DataCollector__table_body_rows == [["1"]]


def test_setup_aggregate_arguments_valid_average_aggregator():
    args = argparse.Namespace(
        file="example.csv", where="brand=apple", aggregate="col1=avg"
    )
    collector = DataCollector(args)
    collector._DataCollector__table_body_rows = [["1"], ["2"], ["3"]]
    collector._DataCollector__table_column_names = ["col1"]

    collector.setup_aggregate_arguments()
    assert collector._DataCollector__table_column_names == ["avg"]
    assert collector._DataCollector__table_body_rows == [["2.0"]]


def test_setup_where_arguments_no_data():
    args = argparse.Namespace(file="example.csv", where="col1=1", aggregate="")
    collector = DataCollector(args)
    collector._DataCollector__table_column_names = ["col1"]
    collector._DataCollector__table_body_rows = [["1"], ["2"], ["3"]]

    collector.setup_where_arguments()
    assert collector._DataCollector__table_body_rows == [["1"]]


def test_setup_where_arguments_valid_filter():
    args = argparse.Namespace(file="example.csv", where="brand=apple", aggregate="")
    collector = DataCollector(args)
    collector._DataCollector__table_body_rows = [
        ["apple", "1"],
        ["banana", "2"],
        ["apple", "3"],
    ]
    collector._DataCollector__table_column_names = ["brand", "quantity"]

    collector.setup_where_arguments()
    assert collector._DataCollector__table_body_rows == [["apple", "1"], ["apple", "3"]]


def test_setup_where_arguments_invalid_column():
    args = argparse.Namespace(file="example.csv", where="color=red", aggregate="")
    collector = DataCollector(args)
    collector._DataCollector__table_body_rows = [["apple", "1"], ["banana", "2"]]
    collector._DataCollector__table_column_names = ["brand", "quantity"]

    try:
        collector.setup_where_arguments()
    except ValueError as e:
        assert str(e) == "'color' is not in list"


def test_setup_where_arguments_no_match():
    args = argparse.Namespace(file="example.csv", where="brand=orange", aggregate="")
    collector = DataCollector(args)
    collector._DataCollector__table_body_rows = [["apple", "1"], ["banana", "2"]]
    collector._DataCollector__table_column_names = ["brand", "quantity"]

    collector.setup_where_arguments()
    assert collector._DataCollector__table_body_rows == []


def test_setup_where_arguments_valid_column():
    args = argparse.Namespace(file="example.csv", where="brand=apple", aggregate="")
    collector = DataCollector(args)
    collector._DataCollector__table_body_rows = [["apple", "1"], ["banana", "2"]]
    collector._DataCollector__table_column_names = ["brand", "quantity"]

    collector.setup_where_arguments()
    assert collector._DataCollector__table_body_rows == [["apple", "1"]]
    assert len(collector._DataCollector__table_body_rows) == 1


def test_setup_where_arguments_more_than_one():
    args = argparse.Namespace(file="example.csv", where="brand=banana", aggregate="")
    collector = DataCollector(args)
    collector._DataCollector__table_body_rows = [
        ["apple", "1"],
        ["banana", "2"],
        ["banana", "2"],
    ]
    collector._DataCollector__table_column_names = ["brand", "quantity"]

    collector.setup_where_arguments()

    assert len(collector._DataCollector__table_body_rows) == 2
