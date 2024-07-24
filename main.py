import os
import sys
import argparse
from dotenv import load_dotenv
from contextualizer import Contextualizer

def extract_owner_and_repo(url):
    url = url.rstrip('.git')
    parts = url.split('/')
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL format")
    return parts[-2], parts[-1]

def main():
    load_dotenv()

    github_token = os.getenv('GITHUB_TOKEN')
    claude_api_key = os.getenv('CLAUDE_API_KEY')

    if not github_token or not claude_api_key:
        print("GITHUB_TOKEN and CLAUDE_API_KEY must be set")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Analyze a GitHub repository')
    parser.add_argument('repo_url', help='GitHub repository URL')
    args = parser.parse_args()

    try:
        owner, repo = extract_owner_and_repo(args.repo_url)
    except ValueError as e:
        print(f"Error parsing repository URL: {e}")
        sys.exit(1)

    c = Contextualizer(github_token, claude_api_key)

    try:
        analysis = c.process_repository(owner, repo)
        print("Analysis:", analysis)
    except Exception as e:
        print(f"Error processing repository: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()