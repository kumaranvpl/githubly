import csv
import getpass
import json
import requests
import sys

from requests.auth import HTTPBasicAuth


class Githubly():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.GITHUB_API = "https://api.github.com/"
        self.auth_token = self.get_auth_token()
        self.headers = {'Authorization': 'token %s' % self.auth_token}

    def _get_response_from_api(self, url):
        print url
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password), headers=self.headers)
        return json.loads((response.text).encode('utf-8'))

    def _post_to_api(self, url, data):
        print url, data
        response = requests.post(url, data=json.dumps(data), auth=HTTPBasicAuth(self.username, self.password), headers=self.headers)
        return json.loads((response.text).encode('utf-8'))

    def get_auth_token(self):
        with open('tokens.csv', 'rb') as f:
            reader = csv.reader(f)
            dict_from_csv = dict(reader)

        if self.username in dict_from_csv:
            return dict_from_csv[self.username]

        url = self.GITHUB_API + "authorizations"
        data = {"scopes": ["repo"], "note": "Authorization token for Githubly"}
        resp_dict = self._post_to_api(url, data)

        with open('tokens.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([self.username, resp_dict["token"]])

        return resp_dict["token"]

    def need_another_user(self):
        user = raw_input("Please enter username of another user to list issues, else enter no: ")
        if user in ["no", "n", "N", "NO", "No"]:
            user = self.username
        return user

    def get_repos(self, user):
        url = self.GITHUB_API + "users/" + user + "/repos?visibility=all&type=all"
        repos_list = self._get_response_from_api(url)
        return repos_list

    def print_issues(self, user, repo):
        url = self.GITHUB_API + "repos/" + user + "/" + repo + "/issues"
        issues_list = self._get_response_from_api(url)
        if not issues_list:
            return False
        for issue in issues_list:
            print str(issue["number"]) + "-" + issue["title"]
        return True

    def _print_repos(self, user):
        need_repos = raw_input("Do you want to see all repos?(y/n) ")
        if need_repos in ["yes", "Yes", "y", "Y", "YES"]:
            repos_list = self.get_repos(user)
            for repo in repos_list:
                print repo["name"]

    def list_issues(self):
        url_suffix = "/issues"
        user = self.need_another_user()
        self._print_repos(user)
        repo = raw_input("Please enter a repo name: ")

    def open_issue(self):
        user = self.need_another_user()
        self._print_repos(user)
        repo = raw_input("Please enter a repo name: ")
        title = raw_input("Please enter title for new issue: ")
        body = raw_input("Please enter body for new issue: ")
        data = {"title": title, "body": body}
        url = self.GITHUB_API + "repos" + "/" + user + "/" + repo + "/issues"
        try:
            response = self._post_to_api(url=url, data=data)
            print "Issue created successfully"
            print "Issue id - %s" % response["id"]
            print "Issue number - %s" % response["number"]
            print "Issue created_at - %s" % response["created_at"]
        except Exception as e:
            print "Error occured - %s" % str(e)

    def close_issue(self):
        user = self.need_another_user()
        self._print_repos(user)
        repo = raw_input("Please enter a repo name: ")
        issues_present = self.print_issues(user, repo)
        if not issues_present:
            print "No issues found. Please open one first"
            return
        issue_num = raw_input("Please enter issue's number to close: ")
        data = {"state": "closed"}
        url = self.GITHUB_API + "repos" + "/" + user + "/" + repo + "/issues/" + issue_num
        try:
            response = self._post_to_api(url=url, data=data)
            print response
            print "Issue closed successfully"
            print "Issue id - %s" % response["id"]
            print "Issue number - %s" % response["number"]
            print "Issue state - %s" % response["state"]
            print "Issue created_at - %s" % response["created_at"]
            print "Issue closed_at - %s" % response["closed_at"]
        except Exception as e:
            print "Error occured - %s" % str(e)



if __name__ == "__main__":
    print "Githublyyyyyyyyyyyyyyyyyyyyy"
    print "Please enter your github username, password below. This is needed to avoid github's rate limitation. "
    print "Don't worry I am not saving your credentials ;)"
    username = raw_input("Username: ")
    #password = getpass.getpass(prompt='Password: ', stream=None)
    password = raw_input("Password: ")
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
        if user_input == "1":
            githubly.list_issues()
        elif user_input == "2":
            pass
        elif user_input == "3":
            githubly.open_issue()
        elif user_input == "4":
            githubly.close_issue()
        elif user_input == "5":
            pass
        elif user_input in ["Exit", "Quit", "quit", "exit", "q"]:
            print "Bye Bye Bye!!!"
            sys.exit()
        else:
            print "Wrong choice... Try again please"
