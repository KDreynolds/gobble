package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/KDreynolds/gobble/internal/contextualizer"
)

func main() {
	githubToken := os.Getenv("GITHUB_TOKEN")
	claudeApiKey := os.Getenv("CLAUDE_API_KEY")

	if githubToken == "" || claudeApiKey == "" {
		log.Fatal("GITHUB_TOKEN and CLAUDE_API_KEY must be set")
	}

	ctx := context.Background()
	c := contextualizer.NewContextualizer(githubToken, claudeApiKey)

	owner := "exampleowner"
	repo := "examplerepo"

	analysis, err := c.ProcessRepository(ctx, owner, repo)
	if err != nil {
		log.Fatalf("Error processing repository: %v", err)
	}

	fmt.Println("Analysis:", analysis)
}
