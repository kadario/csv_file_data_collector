import pytest
from main_class import MainClass


test_file_arg_cases = [
    (["--file", "example.csv"], "example.csv"),
    (["--file", "test_file.csv"], "test_file.csv"),
]


@pytest.mark.parametrize("command, expected_output", test_file_arg_cases)
def test_file_arg(command, expected_output):
    main = MainClass()
    main.prepare_data(command)

    assert main._args.file == expected_output


@pytest.mark.parametrize("option", (["-f", "hello.csv"], ["--file", "hello.csv"]))
def test_file_arg_empty(capsys, option):
    main = MainClass()

    try:
        main.prepare_data(option)
    except SystemExit:
        pass

    output = capsys.readouterr().out
    assert "No file found" in output


def test_args_with_empty_filter():
    main = MainClass()

    with pytest.raises(SystemExit) as exception_info:
        main.prepare_data(["--file", "example.csv", "--where"])

    assert str(exception_info.value) == "2"


def test_args_with_empty_aggregator():
    main = MainClass()

    with pytest.raises(SystemExit) as exception_info:
        main.prepare_data(["--file", "example.csv", "--aggregate"])

    assert str(exception_info.value) == "2"


def test_init():
    main = MainClass()

    assert main._args is None
    assert main._collector is None


def test_set_args():
    main = MainClass()
    args = "test_args"
    main._args = args

    assert main._args == args
    assert main._collector is None


def test_set_collector():
    main = MainClass()
    collector = "test_collector"
    main._collector = collector

    assert main._args is None
    assert main._collector == collector


def test_print_result_no_file():
    main = MainClass()
    main.prepare_data()

    assert main.print_result() == "No file provided"


def test_setup_parser_args_without_args():
    main = MainClass()
    main.prepare_data()

    main._MainClass__setup_parser_args()
    args = main._args

    assert args.file is None
    assert args.where is None
    assert args.aggregate is None
