import os
import tempfile
from github import Github
from git import Repo
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from file_processor import FileProcessor

class Contextualizer:
    def __init__(self, github_token, claude_api_key):
        self.github_client = Github(github_token)
        self.file_processor = FileProcessor()
        self.claude_client = Anthropic(api_key=claude_api_key)

    def process_repository(self, owner, repo):
        repository = self.github_client.get_repo(f"{owner}/{repo}")

        with tempfile.TemporaryDirectory() as repo_dir:
            self.clone_repository(repository.clone_url, repo_dir)
            files = self.file_processor.process_directory(repo_dir)
            analysis = self.analyze_codebase(files)

        return analysis

    def clone_repository(self, url, path):
        Repo.clone_from(url, path)

    def analyze_codebase(self, files):
        prompt = self.format_prompt(files)
        try:
            response = self.claude_client.completions.create(
                model="claude-2",
                prompt=f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}",
                max_tokens_to_sample=1000,
            )
            return response.completion
        except Exception as e:
            return f"Error analyzing codebase: {str(e)}"

    def format_prompt(self, files):
        prompt = "Analyze the following codebase:\n\n"
        for path, content in files.items():
            prompt += f"File: {path}\n\n{content[:1000]}...\n\n"  # Limit each file to 1000 characters
        prompt += "\nPlease provide a brief analysis of this codebase."
        return prompt[:100000]  # Limit total prompt to 100,000 characters