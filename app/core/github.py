import requests

class Github:
    def __init__(self, token):
        self.token = token
        
    def get_branch_name(self, owner, repo, pr_id):
        # Define the url
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_id}"
        
        # Define the headers
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            # Make a get request to the url
            response = requests.get(url, headers=headers)
            
            # Check if the response is successful
            if response.status_code == 200:
                # Extract the branch name
                branch_name = response.json()["head"]["ref"]
                return branch_name
            else:
                return None
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_files(self, owner, repo, pr_id):
        # Define the url
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_id}/files"
        
        # Define the headers
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            # Make a get request to the url
            response = requests.get(url, headers=headers)
            
            # Check if the response is successful
            if response.status_code == 200:
                # Extract the files
                files = response.json()
                return files
            else:
                return None
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_file_content(self, owner, repo, file_path, branch):
        # Define the url
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch}"
        
        # Define the headers
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            # Make a get request to the url
            response = requests.get(url, headers=headers)
            
            # Check if the response is successful
            if response.status_code == 200:
                # Extract the file content
                file_content = response.json()["content"]
                return file_content
            else:
                return None
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_pr_title(self, owner, repo, pr_id):
        # Define the url
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_id}"
        
        # Define the headers
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            # Make a get request to the url
            response = requests.get(url, headers=headers)
            
            # Check if the response is successful
            if response.status_code == 200:
                # Extract the PR title
                pr_title = response.json()["title"]
                return pr_title
            else:
                return None
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None