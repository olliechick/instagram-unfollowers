## Before running the script for the first time

Run `./install_dependencies.sh` to install the relevant dependencies (and enter `y` if prompted; this may happen multiple times). If you want to see what commands this runs, run `cat install_dependencies.sh`.

Create a file called `dirs.txt` in the root directory of the repository, and make the contents:
````
{
    'data': 'path/to/instagram-data/'
}
````
Note that `path/to/instagram-data/` should be the directory where you want the output of the program to be stored (e.g. `/home/ollie/Dropbox/Other/Instagram followers/`.

### Optional extra setup for storing login data

Change `dirs.txt` to be:
````
{
    'data': 'path/to/instagram-data/',
    'logins': '/path/to/logins.txt'
}
````
Note that `/path/to/logins.txt` should be the text file where you store your login data (e.g. `/home/ollie/.hidden-files/logins.txt`).

In `/path/to/logins.txt`, store a dictionary of your login data. For example:
```
{
    'username1': 'password1',
    'username2': 'password2'
}
````

**Note**: you are storing your password in plaintext, so make sure this file is kept in a secure location! If you don't have a secure location to store it (e.g. because you are on a shared computer), I would recommend not including it.

## Where the script stores data

The program will store reports and follower lists in `path/to/instagram-data/`. If this directory doesn't exist, it will create it (and all necessary parent directories). The data it stores is organised like this:

* `path/to/instagram-data/`
  * `username/`
    * `Followers.txt`
    * `Report.txt`
    * `archive/`
      * `Followers at yyyy-mm-dd hhmmss.txt`
      * `Report generated yyyy-mm-dd hhmmss.txt`
      
For each Instagram account, it keeps the most recent list of followers (`Followers.txt`) and report generated (`Report.txt`), as well as an archive of the follower list and report from each time the script was run.

## Running the script

To run the program, run `./run.sh` from the main directory.

If you enter a username that is not included in your logins file, or you don't have a logins file, you will be prompted to enter your password, otherwise, it will use the password stored in this file. To do a bulk run of every login stored in the file, enter `*` as the username.

## Troubleshooting

Feel free to create an issue: https://github.com/olliechick/instagram-unfollowers/issues/new
