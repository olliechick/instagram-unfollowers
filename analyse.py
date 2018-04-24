from datetime import datetime
import webbrowser, requests, sys, platform
import os

INPUT_FILENAME = 'input.txt'
DEFAULT_REPORT_FILENAME = 'Report.txt'
DEFAULT_FOLLOWERS_FILENAME = 'Followers.txt'
ARCHIVE_DIRNAME = 'archive/'
DEFAULT_USERNAME = 'ollienickchick'

root_dir = "data/"

def open_file(filename, mode, encoding="SYS-DEFAULT", errors='ignore'):
    if platform.system() == 'Windows':
        if encoding == "SYS-DEFAULT":
            encoding = 'utf-8'
    elif platform.system() == 'Linux':
        if encoding == "SYS-DEFAULT":
            encoding = 'ISO-8859-1'
    else:
        sys.exit("Unknown system: " + platform.system())
        
    myfile = open(filename, mode, encoding=encoding, errors=errors)
    return myfile

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
    outfile = open_file(filename, 'w+')
    outfile.write(contents)
    outfile.close()
    
    
def prefix_num_with_zeroes(i, length):
    i = str(i)
    if len(i) > length:
        return i
    else:
        return '0'*(length-len(i)) + i
    
    
def save_follower_list(followers, username):
    '''Given a list of followers, saves the list to an archive and
       a live version.
    '''
    current_datetime = datetime.now().strftime('%Y-%m-%d %H%M%S')
    filename = 'Followers at ' + current_datetime + '.txt'
    write_to_file(root_dir + username + '/' + ARCHIVE_DIRNAME + filename, str(followers))
    write_to_file(root_dir + username + '/' + DEFAULT_FOLLOWERS_FILENAME, str(followers))


def generate_follower_list(filename, follower_count):
    '''Given a filename that contains the contents of a user's followers
       tab, returns a dictionary of followers.
       Dict entries are of the form {uid:(username, name)}.
    '''
    print("Location: " + filename)
    string = extract_str(filename)
    while len(string) < 3:
        input("Please populate input.txt, then press enter.")
        string = extract_str(filename)    
    followers_lines = string.split('Followers')[1]
    follower_blocks = followers_lines.split('\n\n')
    
    #Delete 'close' from end
    follower_blocks[-1] = follower_blocks[-1].split('Close')[0].strip()
    
    followers = {}
    f = [None, None]
    
    i=1
    for follower in follower_blocks:
        items = follower.split('\n')
        username = items[0]
        if follower not in ['', ' ']:
            if len(items) == 2 and items[1] in ['Follow', 'Following']:
                #User with no name
                name = ''
            elif len(items) == 3 and items[2] in ['Follow', 'Following']:
                #Normal user
                name = items[1]
            elif len(items) == 4 and items[1] == 'Verified' and items[3] in ['Follow', 'Following']:
                #Verified user
                name = items[2]
            else:
                #Error
                print("Error 42 on -->" + follower + '<--')
                print('Fatal error.')
                sys.exit()
            uid = get_details(username, 'id')
            i_s = prefix_num_with_zeroes(i, len(str(follower_count)))
            percent = round((i/follower_count) * 100, 2)
            if (follower_count == -1):
                print('Processing user {}: {} ({})'.format(i_s, name, username))
            else:
                print('Processing user {}/{} ({}%): {} ({})'.format(i_s, follower_count, percent, name, username))
            followers.update({uid:(username, name)})
            i += 1
            
    return followers


def generate_report(followers, username, save=True):
    '''Given a dictionary of followers, generates a report based on differences
       with the last follower list, which is returned as a string.
       If save is True, then this report is saved to an archived file
       and a live file.
    '''
    current_datetime = datetime.now().strftime('%Y-%m-%d %H%M%S')
    report_filename = 'Report generated ' + current_datetime + '.txt'
    
    old_followers = extract_dict(root_dir + username + '/' + DEFAULT_FOLLOWERS_FILENAME)
    print(root_dir + username + '/' + DEFAULT_FOLLOWERS_FILENAME)
    old_followers_uids = set(old_followers.keys())
    followers_uids = set(followers.keys())
    new_followers = followers_uids.difference(old_followers_uids)
    unfollowers = old_followers_uids.difference(followers_uids)
    any_changes = (set(followers.items()).symmetric_difference(set(old_followers.items())))
    changed_name_users = set([u[0] for u in any_changes]).difference(new_followers).difference(unfollowers)

    print(old_followers)    
    print("STOP")
    print(followers)
    
    ##print('Followers:', followers, '\n\nOld followers:', old_followers)
    ##print("\nNew followers:", new_followers, '\n\nUnfollowers:', unfollowers)
    ##print('\nAny changes:', any_changes, '\n\nChanged name:', changed_name_users)
    ##print('\n')
    
    #create lists of the uids
    new_list = list(new_followers)
    new_list.sort()
    un_list = list(unfollowers)
    un_list.sort()
    
    ##print()
    ##print(any_changes, '\n===== Changed name =====')
    ##for user in changed_name_users:
        ##print(followers[user][0], followers[user][1])
    ##print()
    
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
        
    if save:
        write_to_file(root_dir + username + '/' + ARCHIVE_DIRNAME + report_filename, contents)
        write_to_file(root_dir + username + '/' + DEFAULT_REPORT_FILENAME, contents)
    
    return contents


def prompt_user_to_copy_and_paste_followers(username, follower_count):
    '''Prompts the user to copy and paste their followers to the input file.
       The instagram webpage and input file are automatically opened, and
       the input file is automatically cleared before being presented to the
       user.
    '''
    url = 'http://www.instagram.com/' + username 

    if platform.system() == 'Linux':
        filename = username + '/' + INPUT_FILENAME
    elif platform.system() == 'Windows':      
        filename = username + '\\' + INPUT_FILENAME
    else:
        sys.exit("Unknown system: " + platform.system())

    f = open_file(root_dir + filename, 'w+')
    f.close()
    
    print('Opening Instagram.')
    webbrowser.open(url) #open webpage
    
    if follower_count == -1:
        follower_count_str = username + "'s"
    else:
        follower_count_str = str(follower_count)
    input('Please click ' + follower_count_str + ' followers, then scroll to the bottom. Ctrl+A, then Ctrl+C, then come back here and press the Enter key.')
    
    input('Now (in this text document) Ctrl+V, then Ctrl+S. If a popup pops up, press OK. Then come back here and press the Enter key.')
    webbrowser.open(root_dir + filename) #open input text file
    
    
def get_details(username, detail):
    '''Returns either the id of the user, or the number of people following
       the user, depending on what detail is set to.
       
       == Options for detail ==
       * "followed_by"
       * "id"
    '''
    
    url = 'http://www.instagram.com/' + username
    
    connection_successful = False
    while not connection_successful:
        try:
            myfile = requests.get(url)
            connection_successful = True
        except:
            print("Fatal error: cannot connect to {}. Trying again.".format(url))
        else:
            true = True
            false = False
            null = None
            ##print('\n\n\nLoading', url, '\n\n\n')
            ##print(myfile.text)
            try:
                false = False
                null = None
                true = True
                ##print(myfile.text)
                starts = ["<script type=\"text/javascript\">window._sharedData = ['", "<script type=\"text/javascript\">window._sharedData = "]
                ends = [";</script>", "', '</script>", "', </script>"]
                i = 1
                total = len(starts)*len(ends)
                gotit = False
                for start in starts:
                    for end in ends:
                        try:
                            string = myfile.text.split(start)[1].split(end)[0]
                            ##print(string)
                            if not gotit:
                                user = eval(string)['entry_data']['ProfilePage'][0]['graphql']['user']
                                gotit = True
                        except:
                            pass
                        i += 1

                if not gotit:
                    if detail == "followed_by":
                        user = {'edge_followed_by': {'count': -1}}
                        print("Couldn't get follower count")
                    else:
                        sys.exit("Didn't find user details")            
            except:
                print("wuh woh")
            else:
                if detail == 'followed_by':
                    return user['edge_followed_by']['count']
                elif detail == 'id':
                    return user['id']
                else:
                    return None
    
    
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

    if not os.path.exists(root_dir + username + '/' + DEFAULT_FOLLOWERS_FILENAME):
        #Followers text file doesn't exist - create empty set of followers
        write_to_file(root_dir + username + '/' + DEFAULT_FOLLOWERS_FILENAME, '{}')
        

def main():
    global root_dir
    
    
    
    root_username = input("Username: ")
    if root_username == '':
        root_username = DEFAULT_USERNAME
        
    print('Loading.')    
    root_dir = extract_str("root_dir.txt")    #TODO ask user
    create_files(root_username)  
    follower_count = get_details(root_username, 'followed_by')
    prompt_user_to_copy_and_paste_followers(root_username, follower_count)
    
    print('Generating follower list.')
    followers = generate_follower_list(root_dir + root_username + '/' + INPUT_FILENAME, follower_count)
    
    print('Generating report.\n')
    report = generate_report(followers, root_username)##, False)
    
    save_follower_list(followers, root_username)
    
    print(report)
    input()


if __name__ == '__main__':
    main()
    ##print(get_details(DEFAULT_USERNAME, "id"))