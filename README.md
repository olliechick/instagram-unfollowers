## Before running the script for the first time

1. Run `./install_dependencies.sh` to install the relevant dependencies.

2. Create a file called `dirs.txt` in the root directory of the repository, and make the contents:
````
{
    'logins': '/path/to/logins.txt',
    'data': 'path/to/instagram-data/'
}
````

3. In `/path/to/logins.txt`, store a dictionary of your login data. For example:
```
{
    'username1': 'password1',
    'username2': 'password2'
}
````

**Note**: you are storing your password in plaintext, so make sure this file is kept in a secure location! If you don't have a secure location to store it, I would recommend not including it.

If you enter a username that is not included in this file, you will be prompted to enter your password, otherwise, it will use the password stored in this file. To do a bulk run of every login stored in the file, enter `*` as the username.

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

## Troubleshooting

Feel free to create an issue: https://github.com/olliechick/instagram-unfollowers/issues/new
