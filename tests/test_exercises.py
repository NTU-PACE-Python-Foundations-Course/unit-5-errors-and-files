import csv

from conftest import NOTEBOOK


def test_exercise_1_safe_conversion(tb):
    ages_raw = ["25", "31", "twenty", "19", "", "45"]
    expected_valid = []
    expected_invalid = []
    for value in ages_raw:
        try:
            expected_valid.append(int(value))
        except ValueError:
            expected_invalid.append(value)

    assert tb.ref("valid_ages") == expected_valid
    assert tb.ref("invalid_entries") == expected_invalid


def test_exercise_2_file_io(tb):
    shopping_list = ["Milk", "Eggs", "Bread", "Coffee"]

    shopping_file = NOTEBOOK.parent / "shopping.txt"
    assert shopping_file.exists(), "shopping.txt was not created"

    lines = [line.strip() for line in shopping_file.read_text().splitlines() if line.strip()]
    assert lines == shopping_list

    out = tb.cell_output_text(5)
    for i, item in enumerate(shopping_list, start=1):
        assert f"{i}" in out
        assert item in out


def test_exercise_3_csv_average(tb):
    out = tb.cell_output_text(7)

    grades = [82, 67, 91, 45, 73]
    average = sum(grades) / len(grades)

    assert f"{average:.1f}" in out


def test_exercise_4_pipeline(tb):
    report_file = NOTEBOOK.parent / "grade_report.csv"
    assert report_file.exists(), "grade_report.csv was not created"

    with open(report_file) as f:
        rows = list(csv.DictReader(f))

    assert {row["name"] for row in rows} == {"Alice", "Bob", "Carol", "Dan", "Eve"}

    statuses = {row["name"]: row["status"] for row in rows}
    assert statuses["Dan"] == "needs support"
    assert statuses["Alice"] == "pass"

    out = tb.cell_output_text(9)
    assert "1 student" in out
