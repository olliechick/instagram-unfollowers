#!/usr/bin/python3
import errno
import os

from file_io import write_to_file

STORE_LOGIN_DATA_PROMPT = "Do you want to store you login data on this computer? " \
                          "Note that it will be stored in plaintext, so don't do this on a shared computer."


def get_boolean_response(prompt):
    response = input(prompt + "\nType y/n: ").lower()

    while len(response) > 0 and response[0] not in ['y', 'n']:
        response = input("Sorry, that is not a valid response. Please type only one character, either 'y' or 'n': ")

    return response[0] == 'y'


def ends_in_slash(string):
    return len(string) > 0 and string[-1] in ['/', '\\']


def is_valid_dir(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            return False
    return True


def is_valid_filepath(filepath):
    directory = filepath[:filepath.rindex('/') + 1]
    return is_valid_dir(directory)


def generate_dirs():
    dirs = dict()

    data_dir = input("Enter the directory where you want data to be stored: ")
    good_dir = is_valid_dir(data_dir) and ends_in_slash(data_dir)
    while not (good_dir):
        if not ends_in_slash(data_dir):
            data_dir = input("That is not a valid directory. Valid directories must end in a slash. Please try again: ")
        else:
            data_dir = input("That is not a directory you can create. Please try again: ")
        good_dir = is_valid_dir(data_dir) and ends_in_slash(data_dir)
    dirs['data'] = data_dir

    wants_to_store_logins = get_boolean_response(STORE_LOGIN_DATA_PROMPT)
    if wants_to_store_logins:
        logins_dir = input("Enter the location of the text file where you store your logins: ")
        while not (is_valid_filepath(data_dir)):
            logins_dir = input("That is not a file you can create. Please try again: ")
        dirs['logins'] = logins_dir

    # Save dirs.txt
    write_to_file('dirs.txt', str(dirs))

    # Get login details
    if wants_to_store_logins:
        print("Now enter the user details you want to save. To finish, enter * as a username:")
        logins = dict()

        username = input("Username: ").strip()
        keep_going = username != '*'
        while keep_going:
            password = input("Password: ").strip()
            logins[username] = password
            username = input("Username: ").strip()
            keep_going = username != '*'

        # Save logins file
        write_to_file(logins_dir, str(logins))


def main():
    generate_dirs()


if __name__ == "__main__":
    main()
