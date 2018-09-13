#!/usr/bin/python3

import getpass
import os
from datetime import datetime

from InstagramAPI import InstagramAPI

from file_io import write_to_file, extract_dict

INPUT_FILENAME = 'input.txt'
REPORT_FILENAME = 'Report.txt'
FOLLOWERS_FILENAME = 'Followers.txt'
ARCHIVE_DIRNAME = 'archive/'

root_dir = "data/"


def get_username():
    """returns string username, list args"""
    inputs = input("Username: ")
    input_list = inputs.split()
    if len(input_list) == 0:
        return inputs, []
    else:
        return input_list[0], input_list[1:]


def get_password():
    return getpass.getpass()


def create_files(username):
    """Checks if the necessary files and directories exists.
       If they don't, creates them. Necessary files and directories:
       * root_dir
       * root_dir/username/
       * root_dir/username/archive/
       * root_dir/username/Followers.txt
    """

    archive = ARCHIVE_DIRNAME

    dirs = [root_dir,
            root_dir + username + "/",
            root_dir + username + "/" + archive]

    for directory in dirs:
        if not os.path.isdir(directory):
            os.makedirs(directory)
            print("Creating directory: " + directory)

    if not os.path.exists(root_dir + username + '/' + FOLLOWERS_FILENAME):
        # Followers text file doesn't exist - create empty set of followers
        write_to_file(root_dir + username + '/' + FOLLOWERS_FILENAME, '{}')


def saveFollowers(followers, username):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H%M%S')
    filename = 'Followers at ' + current_datetime + '.txt'
    write_to_file(root_dir + username + '/' + ARCHIVE_DIRNAME + filename, str(followers))
    write_to_file(root_dir + username + '/' + FOLLOWERS_FILENAME, str(followers))


def generateFollowers(followersRaw):
    followers = dict()
    for follower in followersRaw:
        uid = str(follower["pk"])
        username = follower["username"]
        name = follower["full_name"]
        followers.update({uid: (username, name)})
    return followers


def save_report(report, username):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H%M%S')
    report_filename = 'Report generated ' + current_datetime + '.txt'

    write_to_file(root_dir + username + '/' + ARCHIVE_DIRNAME + report_filename, report)
    write_to_file(root_dir + username + '/' + REPORT_FILENAME, report)


def generate_report(followers, username):
    old_followers = extract_dict(root_dir + username + '/' + FOLLOWERS_FILENAME)
    old_followers_uids = set(old_followers.keys())
    followers_uids = set(followers.keys())
    new_followers = followers_uids.difference(old_followers_uids)
    unfollowers = old_followers_uids.difference(followers_uids)
    any_changes = (set(followers.items()).symmetric_difference(set(old_followers.items())))
    changed_name_users = set([u[0] for u in any_changes]).difference(new_followers).difference(unfollowers)

    # create lists of the uids
    new_list = list(new_followers)
    new_list.sort()
    un_list = list(unfollowers)
    un_list.sort()

    contents = ''

    if len(new_followers) != 0:
        contents += '=' * 5 + ' New followers ' + '=' * 5 + '\n'
        for uid in new_list:
            contents += followers[uid][0] + ' (' + followers[uid][1] + ')\n'
        if len(unfollowers) != 0:
            contents += "\n"

    if len(unfollowers) != 0:
        contents += '=' * 5 + ' Unfollowers ' + '=' * 5 + '\n'
        for uid in un_list:
            contents += old_followers[uid][0] + ' (' + old_followers[uid][1] + ')\n'
        if len(changed_name_users) != 0:
            contents += "\n"

    if len(changed_name_users) != 0:
        contents += '=' * 5 + ' Changed name ' + '=' * 5 + '\n'
        for uid in changed_name_users:
            contents += old_followers[uid][0] + ' (' + old_followers[uid][1] + ') -> '
            contents += followers[uid][0] + ' (' + followers[uid][1] + ')\n'

    if contents == '':
        contents = "No change.\n"

    return contents


def main():
    global root_dir

    dirs = extract_dict("dirs.txt")
    if dirs is None or "data" not in dirs:
        print("Error: You must create a file in this directory ({}) called `dirs.txt`. ".format(
            os.path.dirname(os.path.realpath(__file__))) +
              "This must contain a dictionary, in the form `{'logins': '/path/to/logins.txt', 'data': 'path/to/instagram-data/'}`.")
        return

    if "logins" not in dirs:
        logins = None
    else:
        logins = extract_dict(dirs["logins"])

    username, args = get_username()
    if username == "*":
        ## use all logins
        if (logins is None):
            print("No login data found.")
            return
    elif logins is not None and username in logins:
        password = logins[username]
        logins = {username: password}
    else:
        password = get_password()
        logins = {username: password}

    for username in logins:
        password = logins[username]
        print("\nLoading {}.".format(username))
        api = InstagramAPI(username, password)
        api.login()

        try:
            user_id = api.username_id
            ##print("Loaded", user_id)
        except AttributeError:
            try:
                if (api.__dict__['LastJson']['invalid_credentials']):
                    print("Sorry, that username/password combination is invalid. Please try again.\n")
                    main()
                else:
                    print("Error 41. Please try again.\n")
                    main()
            except KeyError:
                try:
                    if (api.__dict__['LastJson']['error_type'] == 'missing_parameters'):
                        print("Please enter a username and a password.\n")
                        main()
                    else:
                        print("Error 39. Please try again.\n")
                        main()
                except:
                    print("Error 40. Please try again.\n")
                    main()

        root_dir = dirs["data"]
        create_files(username)
        ##print("Files created.")    

        followersRaw = api.getTotalFollowers(user_id)
        ##print("Got total followers.")

        followers = generateFollowers(followersRaw)
        report = generate_report(followers, username)
        ##print("Generated report.")

        saveFollowers(followers, username)
        save_report(report, username)
        ##print("Saved report.")

        print("\n==================================== Report ====================================\n")
        print(report)
        print("================================================================================")

    input("\nPress return to exit.")


if __name__ == "__main__":
    main()
