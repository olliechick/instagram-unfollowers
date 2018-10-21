#!/usr/bin/python3

import getpass
import os
import webbrowser
from datetime import datetime

from InstagramAPI import InstagramAPI

from file_io import write_to_file, extract_dict

INPUT_FILENAME = 'input.txt'
REPORT_FILENAME = 'Report'
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


def save_followers(followers, username):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H%M%S')
    filename = 'Followers at ' + current_datetime + '.txt'
    write_to_file(root_dir + username + '/' + ARCHIVE_DIRNAME + filename, str(followers))
    write_to_file(root_dir + username + '/' + FOLLOWERS_FILENAME, str(followers))


def generate_followers(followersRaw):
    followers = dict()
    for follower in followersRaw:
        uid = str(follower["pk"])
        username = follower["username"]
        name = follower["full_name"]
        followers.update({uid: (username, name)})
    return followers


def save_report(report, username, filetype):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H%M%S')
    archive_report_filename = 'Report generated ' + current_datetime + '.' + filetype

    write_to_file(root_dir + username + '/' + ARCHIVE_DIRNAME + archive_report_filename, report)
    filename = root_dir + username + '/' + REPORT_FILENAME + '.' + filetype
    write_to_file(filename, report)
    return filename


def generate_changed_followers(followers, username):
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
    unfollowers_list = list(unfollowers)
    unfollowers_list.sort()

    return old_followers, new_list, unfollowers_list, changed_name_users


def generate_ig_link(username):
    return '<a href="https://www.instagram.com/' + username + '/">' + username + '</a>'


def generate_html_report(followers, username):
    old_followers, new_list, unfollowers_list, changed_name_users = generate_changed_followers(followers, username)

    header = """<!-- Generated by https://github.com/olliechick/instagram-unfollowers (created by Ollie Chick) -->\n
<!DOCTYPE html>
<html>
  <head>
   <style>
      table { border-collapse: collapse; }   
      th {
        padding-top: 12px;
        padding-bottom: 12px;
        text-align: left;
        color: white;
      }
      td, th {
        padding: 8px;
      }
      
      #good th { background-color: #03a022; }
	  #good tr:hover {background-color: #effff2;}
      
      #bad th { background-color: #e50b00; }
      #bad tr:hover { background-color: #ffefef; }
      
      #neutral th { background-color: #015fa8; }
      #neutral tr:hover { background-color: #eff8ff; }
      
    </style>
  </head>
<body>
"""
    contents = header

    table_headings = '  <tr>\n' \
                     '    <th>Username</th>\n' \
                     '    <th>Name</th>\n' \
                     '  </tr>\n'

    # New followers

    if len(new_list) != 0:
        contents += '<h2>New followers</h2>\n' \
                    '<table id="good"\n' + table_headings

        for uid in new_list:
            contents += '  <tr>\n' \
                        '    <td>' + generate_ig_link(followers[uid][0]) + '</td>\n' + \
                        '    <td>' + followers[uid][1] + '</td>\n' + \
                        '  </tr>\n'

    contents += "</table>\n\n"

    # Unfollowers

    if len(unfollowers_list) != 0:
        contents += '<h2>Unfollowers</h2>\n' \
                    '<table id="bad"\n' + table_headings
        for uid in unfollowers_list:
            contents += '  <tr>\n' \
                        '    <td>' + generate_ig_link(old_followers[uid][0]) + '</td>\n' + \
                        '    <td>' + old_followers[uid][1] + '</td>\n' + \
                        '  </tr>\n'

        contents += "</table>\n\n"

    # Changed name

    if len(changed_name_users) != 0:
        contents += '<h2>Changed name</h2>\n' \
                    '<table id="neutral">\n' + '  <tr>\n' \
                                               '    <th>Old username</th>\n' \
                                               '    <th>Old name</th>\n' \
                                               '    <th>New username</th>\n' \
                                               '    <th>New name</th>\n' \
                                               '  </tr>\n'
        for uid in changed_name_users:
            contents += '  <tr>\n' \
                        '    <td>' + old_followers[uid][0] + '</td>\n' + \
                        '    <td>' + old_followers[uid][1] + '</td>\n' + \
                        '    <td>' + generate_ig_link(followers[uid][0]) + '</td>\n' + \
                        '    <td>' + followers[uid][1] + '</td>\n' + \
                        '  </tr>\n'

        contents += "</table>\n\n"

    if contents == header:
        contents = "No change.\n"
    else:
        contents += '</body></html>'

    return contents


def generate_text_report(followers, username):
    old_followers, new_list, unfollowers_list, changed_name_users = generate_changed_followers(followers, username)

    contents = ''

    if len(new_list) != 0:
        contents += '=' * 5 + ' New followers ' + '=' * 5 + '\n'
        for uid in new_list:
            contents += followers[uid][0] + ' (' + followers[uid][1] + ')\n'
        if len(unfollowers_list) != 0:
            contents += "\n"

    if len(unfollowers_list) != 0:
        contents += '=' * 5 + ' Unfollowers ' + '=' * 5 + '\n'
        for uid in unfollowers_list:
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
                else:
                    print("Error 41. Please try again.\n")
            except KeyError:
                try:
                    if (api.__dict__['LastJson']['error_type'] == 'missing_parameters'):
                        print("Please enter a username and a password.\n")
                    else:
                        print("Error 39. Please try again.\n")
                except:
                    print("Error 40. Please try again.\n")
            return

        root_dir = dirs["data"]
        create_files(username)
        ##print("Files created.")

        followersRaw = api.getTotalFollowers(user_id)
        ##print("Got total followers.")

        followers = generate_followers(followersRaw)
        text_report = generate_text_report(followers, username)
        html_report = generate_html_report(followers, username)
        ##print("Generated report.")

        save_followers(followers, username)
        save_report(text_report, username, 'txt')
        html_filename = save_report(html_report, username, 'html')
        ##print("Saved report.")

        print("\n==================================== Report ====================================\n")
        print(text_report)
        print("================================================================================")
        webbrowser.open('file://' + html_filename)
        print(html_filename)

    input("\nPress return to exit.")


if __name__ == "__main__":
    main()
