package contextualizer

import (
	"context"

	"github.com/KDreynolds/github-context/internal/claude"
	"github.com/KDreynolds/github-context/internal/fileprocessor"
	"github.com/KDreynolds/github-context/internal/github"
)

type Contextualizer struct {
	githubClient  *github.Client
	fileProcessor *fileprocessor.Processor
	claudeClient  *claude.Client
}

func NewContextualizer(githubToken, claudeApiKey string) *Contextualizer {
	return &Contextualizer{
		githubClient:  github.NewClient(githubToken),
		fileProcessor: fileprocessor.NewProcessor(),
		claudeClient:  claude.NewClient(claudeApiKey),
	}
}

func (c *Contextualizer) ProcessRepository(ctx context.Context, owner, repo string) (string, error) {
	// Fetch repository
	repository, err := c.githubClient.GetRepository(ctx, owner, repo)
	if err != nil {
		return "", err
	}

	// Clone repository (implement this part)
	repoDir, err := cloneRepository(repository)
	if err != nil {
		return "", err
	}

	// Process files
	files, err := c.fileProcessor.ProcessDirectory(repoDir)
	if err != nil {
		return "", err
	}

	// Analyze with Claude
	analysis, err := c.claudeClient.AnalyzeCodebase(files)
	if err != nil {
		return "", err
	}

	return analysis, nil
}

func cloneRepository(repo *github.Repository) (string, error) {
	// Implement repository cloning logic
	return "", nil
}
