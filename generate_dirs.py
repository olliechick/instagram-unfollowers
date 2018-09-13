#!/usr/bin/python3

from file_io import write_to_file

STORE_LOGIN_DATA_PROMPT = "Do you want to store you login data on this computer? " \
                          "Note that it will be stored in plaintext, so don't do this on a shared computer."


def get_boolean_response(prompt):
    response = input(prompt + "\nType y/n: ").lower()

    while response[0] not in ['y', 'n']:
        response = input("Sorry, that is not a valid response. Please type only one character, either 'y' or 'n': ")

    return response[0] == 'y'


def generate_dirs():
    dirs = dict()
    dirs['data'] = input("Enter the directory where you want data to be stored: ")
    wants_to_store_logins = get_boolean_response(STORE_LOGIN_DATA_PROMPT)
    if wants_to_store_logins:
        dirs['logins'] = input("Enter the location of the text file where you store your logins: ")
    output = write_to_file('dirs.txt', str(dirs))


def main():
    generate_dirs()


if __name__ == "__main__":
    main()
