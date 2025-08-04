from functions.get_file_content import get_file_content 


def main():
    testcases = [("calculator", "main.py"),
                 ("calculator", "pkg/calculator.py"),
                 ("calculator", "/bin/cat"),
                 ("calculator", "pkg/does_not_exist.py")]

    for test in testcases:
        print("Result for current file:")
        print(get_file_content(test[0], test[1]))


if __name__ == "__main__":
    main()
