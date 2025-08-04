from functions.get_files_info import get_files_info


def main():
    testcases = [("calculator", "."),
                 ("calculator", "pkg"),
                 ("calculator", "/bin"),
                 ("calculator", "../")]

    for test in testcases:
        print("Result for current directory:")
        print(get_files_info(test[0], test[1]))



if __name__ == "__main__":
    main()
