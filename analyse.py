#!/usr/bin/python3

from InstagramAPI import InstagramAPI
from datetime import datetime
import webbrowser, requests, sys, platform
import os

INPUT_FILENAME = 'input.txt'
REPORT_FILENAME = 'Report.txt'
FOLLOWERS_FILENAME = 'Followers.txt'
ARCHIVE_DIRNAME = 'archive/'

root_dir = "data/"

def getUsername():
    return input("Username: ")

def getPassword():
    return input("Password: ")

def extract_str(filename):
    """returns a (stripped) string from file"""
    myfile = open_file(filename, 'r')
    s = myfile.read()
    myfile.close()
    s = s.strip()
    return s

def extract_list(filename):
    """returns a list from file"""
    myfile = open_file(filename, 'r')
    s = myfile.read()
    myfile.close
    sanitised_s = ''
    in_double_quotes = False
    for char in s:
        if char == '"' and in_double_quotes:
            in_double_quotes = False
            sanitised_s += char
        elif char == '"':
            in_double_quotes = True
            sanitised_s += char
        elif char == "'" and in_double_quotes:
            sanitised_s += '\\' + "'"
        else:
            sanitised_s += char
    l = eval(sanitised_s.strip())
    return l

def extract_dict(filename):
    """returns a dictionary from file"""
    myfile = open_file(filename, 'r')
    s = myfile.read()
    myfile.close()
    d = eval(s)
    return d    

def write_to_file(filename, contents):    
    '''Writes contents to file filename'''
    outfile = open_file(filename, 'w+', encoding="utf-8")
    outfile.write(contents)
    outfile.close()

def open_file(filename, mode, encoding="utf-8", errors='ignore'):        
    myfile = open(filename, mode, encoding=encoding, errors=errors)
    return myfile

def create_files(username):
    '''Checks if the necessary files and directories exists.
       If they don't, creates them. Necessary files and directories:
       * root_dir
       * root_dir/username/
       * root_dir/username/archive/
       * root_dir/username/Followers.txt
    '''
    
    archive = ARCHIVE_DIRNAME

    dirs = [root_dir,
            root_dir + username + "/",
            root_dir + username + "/" + archive]
    
    for directory in dirs:
        if not os.path.isdir(directory):
            os.makedirs(directory)
            print("Creating directory: " + directory)

    if not os.path.exists(root_dir + username + '/' + FOLLOWERS_FILENAME):
        #Followers text file doesn't exist - create empty set of followers
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
        followers.update({uid:(username, name)})
    return followers


def saveReport(report, username):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H%M%S')
    report_filename = 'Report generated ' + current_datetime + '.txt'    
    
    write_to_file(root_dir + username + '/' + ARCHIVE_DIRNAME + report_filename, report)
    write_to_file(root_dir + username + '/' + REPORT_FILENAME, report)

def generateReport(followers, username):
    old_followers = extract_dict(root_dir + username + '/' + FOLLOWERS_FILENAME)
    old_followers_uids = set(old_followers.keys())
    followers_uids = set(followers.keys())
    new_followers = followers_uids.difference(old_followers_uids)
    unfollowers = old_followers_uids.difference(followers_uids)
    any_changes = (set(followers.items()).symmetric_difference(set(old_followers.items())))
    changed_name_users = set([u[0] for u in any_changes]).difference(new_followers).difference(unfollowers)
    
    #create lists of the uids
    new_list = list(new_followers)
    new_list.sort()
    un_list = list(unfollowers)
    un_list.sort()
    
    contents = ''
    
    if len(new_followers) != 0:
        contents += '='*5 + ' New followers ' + '='*5 + '\n'
        for uid in new_list:
            contents += followers[uid][0] + ' (' + followers[uid][1] + ')\n'
        
    if len(unfollowers) != 0:
        contents += '\n' + '='*5 + ' Unfollowers ' + '='*5 + '\n'
        for uid in un_list:
            contents += old_followers[uid][0] + ' (' + old_followers[uid][1] + ')\n'
            
    if len(changed_name_users) != 0:
        contents += '\n' + '='*5 + ' Changed name ' + '='*5 + '\n'
        for uid in changed_name_users:
            contents += old_followers[uid][0] + ' (' + old_followers[uid][1] + ') -> '
            contents += followers[uid][0] + ' (' + followers[uid][1] + ')\n'
    
    return contents


def main():
    global root_dir
        
    username = getUsername()
    password = getPassword() #TODO use config file
    print("Loading.")
    api = InstagramAPI(username, password)
    api.login()
    
    root_dir = extract_str("root_dir.txt")    #TODO ask user
    create_files(username)

    user_id = api.username_id
    followersRaw = api.getTotalFollowers(user_id)
    
    followers = generateFollowers(followersRaw)
    report = generateReport(followers, username)
    
    saveFollowers(followers, username)
    saveReport(report, username)
    
    print(report)
    input()    


if __name__ == "__main__":
    main()
