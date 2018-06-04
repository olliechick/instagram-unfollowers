To run the code, first create a file called `dirs.txt` in the root directory of the repository, and make the contents:
````
{
    'logins': '/path/to/logins.txt',
    'data': 'path/to/instagram-data/'
}
````

In `/path/to/logins.txt`, store a dictionary of your login data. For example:
```
{
    'username1': 'password1',
    'username2': 'password2'
}
````

The program will store reports and follower lists in `path/to/instagram-data/`. If this directory doesn't exist, it will create it (and all neccesary parent directories). The data it stores is organised like this:

* path/to/instagram-data/
  * username
    * Followers.txt
    * Report.txt
    * archive
      * Followers at yyyy-mm-dd hhmmss.txt
      * Report generated yyyy-mm-dd hhmmss.txt
      
For each Instagram account, it keeps the most recent list of followers (`Followers.txt`) and report generated (`Report.txt`), as well as an archive of the follower list and report from each time the script was run.

To run the program, run `./run.sh` from that directory.

**Note**: you may need to run `./install_dependencies.sh` to install the relevant dependencies first.
