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
        self.auth_token = self._get_auth_token()
        self.headers = {'Authorization': 'token %s' % self.auth_token}

    def _get_response_from_api(self, url, need_links=None):
        print url
        response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password), headers=self.headers)
        if need_links:
            return json.loads((response.text).encode('utf-8')), response.links["next"], response.links["last"]
        return json.loads((response.text).encode('utf-8'))

    def _post_to_api(self, url, data):
        print url, data
        response = requests.post(url, data=json.dumps(data), auth=HTTPBasicAuth(self.username, self.password), headers=self.headers)
        return json.loads((response.text).encode('utf-8'))

    def _get_auth_token(self):
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

    def _need_another_user(self):
        user = raw_input("Please enter username of another user to list issues, else enter no: ")
        if user in ["no", "n", "N", "NO", "No"]:
            user = self.username
        return user

    def _get_repos(self, user):
        url = self.GITHUB_API + "users/" + user + "/repos?visibility=all&type=all"
        repos_list = self._get_response_from_api(url)
        return repos_list

    def _print_issues(self, user, repo, url=None):
        if not url:
            url = self.GITHUB_API + "repos/" + user + "/" + repo + "/issues"
        issues_list, next_url, last_url = self._get_response_from_api(url, need_links=True)

        if not issues_list:
            print "No issues found. Please open one first"
            return False
        for issue in issues_list:
            print str(issue["number"]) + "-" + issue["title"]

        print "Next - %s" % next_url["url"]
        print "Last - %s" % last_url["url"]

        new_choice = raw_input("Please enter next/last to navigate to next/last page. Enter exit to quit: ")
        if new_choice not in ["Exit", "Quit", "quit", "exit", "q"]:
            if new_choice in ["Next", "next", "NEXT"]:
                new_url = next_url["url"]
            elif new_choice in ["Last", "last", "LAST"]:
                new_url = last_url["url"]
            else:
                print "Bad choice :("
                return True
            self._print_issues(user=user, repo=repo, url=new_url)

        return True

    def _print_repos(self, user):
        need_repos = raw_input("Do you want to see all repos?(y/n) ")
        if need_repos in ["yes", "Yes", "y", "Y", "YES"]:
            repos_list = self._get_repos(user)
            for repo in repos_list:
                print repo["name"]

    def list_issues(self):
        user = self._need_another_user()
        self._print_repos(user)
        repo = raw_input("Please enter a repo name: ")
        issues_present = self._print_issues(user, repo)

    def issue_in_detail(self):
        user = self._need_another_user()
        self._print_repos(user)
        repo = raw_input("Please enter a repo name: ")
        issues_present = self._print_issues(user, repo)
        if not issues_present: return
        issue_num = raw_input("Please enter issue's number to check its details: ")
        url = self.GITHUB_API + "repos" + "/" + user + "/" + repo + "/issues/" + issue_num
        try:
            response = self._post_to_api(url=url, data={})
            print response
            print "Issue details:"
            print "Issue id - %s" % response["id"]
            print "Issue number - %s" % response["number"]
            print "Issue title - %s" % response["title"]
            print "Issue body - %s" % response["body"]
            print "Issue state - %s" % response["state"]
            print "Issue url - %s" % response["url"]
            print "Issue repository_url - %s" % response["repository_url"]
            print "Issue html_url - %s" % response["html_url"]
            print "Issue comments - %s" % response["comments"]
            print "Issue created_at - %s" % response["created_at"]
            print "Issue closed_at - %s" % response["closed_at"]
        except Exception as e:
            print "Error occured - %s" % str(e)

    def open_issue(self):
        user = self._need_another_user()
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
        user = self._need_another_user()
        self._print_repos(user)
        repo = raw_input("Please enter a repo name: ")
        issues_present = self._print_issues(user, repo)
        if not issues_present: return
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

    def add_comment(self):
        user = self._need_another_user()
        self._print_repos(user)
        repo = raw_input("Please enter a repo name: ")
        issues_present = self._print_issues(user, repo)
        if not issues_present: return
        issue_num = raw_input("Please enter issue's number to add comment: ")
        comment = raw_input("Please enter your comment: ")
        data = {"body": comment}
        url = self.GITHUB_API + "repos" + "/" + user + "/" + repo + "/issues/" + issue_num + "/comments"
        try:
            response = self._post_to_api(url=url, data=data)
            print response
            print "Comment added successfully"
            print "Comment id - %s" % response["id"]
            print "Comment message - %s" % response["body"]
            print "Comment html_url - %s" % response["html_url"]
            print "Comment created_at - %s" % response["created_at"]
        except Exception as e:
            print "Error occured - %s" % str(e)



if __name__ == "__main__":
    print "Githublyyyyyyyyyyyyyyyyyyyyy"
    print "Please enter your github username, password below. This is needed to avoid github's rate limitation. "
    print "Don't worry I am not saving your credentials ;)"
    username = raw_input("Username: ")
    password = getpass.getpass(prompt='Password: ', stream=None)
    #password = raw_input("Password: ")
    try:
        githubly = Githubly(username=username, password=password)
    except Exception as e:
        print "Something broke :("
        print "Exception for geeks - %s" % str(e)

    while True:
        print "Menu"
        print "1. List issues"
        print "2. Issue in detail"
        print "3. Open new issue"
        print "4. Close issue"
        print "5. Add comment to an issue"
        print "Exit or Ctrl + C to quit"
        user_input = raw_input("Please enter your choice: ")
        if user_input == "1":
            githubly.list_issues()
        elif user_input == "2":
            githubly.issue_in_detail()
        elif user_input == "3":
            githubly.open_issue()
        elif user_input == "4":
            githubly.close_issue()
        elif user_input == "5":
            githubly.add_comment()
        elif user_input in ["Exit", "Quit", "quit", "exit", "q"]:
            print "Bye Bye Bye!!!"
            sys.exit()
        else:
            print "Wrong choice... Try again please"
