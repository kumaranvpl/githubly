import getpass
import requests
import sys

from requests.auth import HTTPBasicAuth


class Githubly():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.GITHUB_API = "https://api.github.com/users/"
        self.user_api = self.GITHUB_API + username + "/"

    def get_response_from_api(self, url_suffix):
        response = requests.get(self.user_api+url_suffix, auth=HTTPBasicAuth(self.username, self.password))
        print response


if __name__ == "__main__":
    print "Githublyyyyyyyyyyyyyyyyyyyyy"
    print "Please enter your github username, password below. Don't worry I am not saving your credentials ;)"
    username = raw_input("Username: ")
    password = getpass.getpass(prompt='Password: ', stream=None)
    try:
        githubly = Githubly(username=username, password=password)
    except Exception as e:
        print "Something broke :("
        print "Exception for geeks - %s" % str(e)

    while True:
        print "Menu"
        print "1. List issues"
        print "2. Detailed issue"
        print "3. Open new issue"
        print "4. Close issue"
        print "5. Add comment to an issue"
        print "Exit or Ctrl + C to quit"
        user_input = raw_input("Please enter your choice: ")
        if user_input == 1:
            pass
        elif user_input == 2:
            pass
        elif user_input == 3:
            pass
        elif user_input == 4:
            pass
        elif user_input == 5:
            pass
        elif user_input in ["Exit", "Quit", "quit", "exit", "q"]:
            print "Bye Bye Bye!!!"
            sys.exit()
        else:
            print "Wrong choice... Try again please"
