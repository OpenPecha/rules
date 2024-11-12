import http.client
import json
import argparse

def set_branch_protection(owner, repo, branch, token):
    # Branch protection settings
    protection_settings = {
        "required_status_checks": {
            "strict": True,
            "contexts": []
        },
        "enforce_admins": False,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "required_approving_review_count": 1,
            "require_last_push_approval": True
        },
        "restrictions": None,
        "allow_force_pushes": False,
        "allow_deletions": False,
        "required_conversation_resolution": True
    }

    # Create the connection to GitHub API
    conn = http.client.HTTPSConnection("api.github.com")

    # Define the headers
    headers = {
        "Authorization": f"token {token}",
        "User-Agent": "PythonScript",
        "Accept": "application/vnd.github.v3+json"
    }

    # Define the endpoint for setting branch protection rules
    url = f"/repos/{owner}/{repo}/branches/{branch}/protection"

    # Send the request to set branch protection rules
    conn.request("PUT", url, body=json.dumps(protection_settings), headers=headers)

    # Get the response
    response = conn.getresponse()
    data = response.read().decode("utf-8")

    # Check if the request was successful
    if response.status == 200 or response.status == 201:
        print("Branch protection rule set successfully!")
    else:
        print("Failed to set branch protection rule.")
        print("Status code:", response.status)
        print("Response:", data)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set branch protection rule on a GitHub repository.")
    parser.add_argument("owner", help="GitHub username or organization")
    parser.add_argument("repo", help="Repository name")
    parser.add_argument("branch", help="Branch to protect")
    parser.add_argument("token", help="GitHub personal access token")

    args = parser.parse_args()

    set_branch_protection(args.owner, args.repo, args.branch, args.token)
