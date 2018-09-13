## Before running the script for the first time

Run `./install_dependencies.sh` to install the relevant dependencies (and enter `y` if prompted; this may happen multiple times). If you want to see what commands this runs, run `cat install_dependencies.sh`.

Run `./generate_dirs.py` to run the wizard that takes you through setting up where you store your files, and optionally, where you store your logins, and what your login details are. It then stores this data in `dirs.txt`, and your login details in the file whose path you provide.

**Note**: if you choose to store your logins, you are storing your password in plaintext, so make sure this file is kept in a secure location! If you don't have a secure location to store it (e.g. because you are on a shared computer), I would recommend not including it.

## Where the script stores data

The program will store reports and follower lists in the directory referenced in `dirs.txt`. If this directory doesn't exist, it will create it (and all necessary parent directories). The data it stores is organised like this:

* `path/provided/`
  * `username/`
    * `Followers.txt`
    * `Report.txt`
    * `archive/`
      * `Followers at yyyy-mm-dd hhmmss.txt`
      * `Report generated yyyy-mm-dd hhmmss.txt`
      
For each Instagram account, it keeps the most recent list of followers (`Followers.txt`) and report generated (`Report.txt`), as well as an archive of the follower list and report from each time the script was run.

## Running the script

To run the program, run `./analyse.py` from the main directory.

If you enter a username that is not included in your logins file, or you don't have a logins file, you will be prompted to enter your password, otherwise, it will use the password stored in this file. To do a bulk run of every login stored in the file, enter `*` as the username.

## Troubleshooting

| Problem       | Solution |
| ------------- |-------------|
|When I run the program, it says `Fail to import moviepy. Need only for Video upload.`  | This is a print statement that the Instagram API this is built on generates because `moviepy` isn't installed. However, this is not needed for the functionality this program provides (`Need only for Video upload`), so you can safely ignore it. |

For any other issues, feel free to create an issue: https://github.com/olliechick/instagram-unfollowers/issues/new
