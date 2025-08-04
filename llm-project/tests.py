from functions.run_python_file import run_python_file


def main():
    testcases = [
        ["calculator", "main.py"],
        ["calculator", "main.py", ["3 + 5"]],
        ["calculator", "tests.py"],
        ["calculator", "../main.py"],
        ["calculator", "nonexistent.py"],
            ]

    for test in testcases:
        print("Result for current file:")
        if len(test) == 3:
            print(run_python_file(test[0], test[1], test[2]))
        else:
            print(run_python_file(test[0], test[1]))


if __name__ == "__main__":
    main()
