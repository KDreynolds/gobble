package github

import (
	"context"

	"github.com/google/go-github/v38/github"
	"golang.org/x/oauth2"
)

type Client struct {
	client *github.Client
}

func NewClient(token string) *Client {
	ctx := context.Background()
	ts := oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: token},
	)
	tc := oauth2.NewClient(ctx, ts)

	return &Client{
		client: github.NewClient(tc),
	}
}

func (c *Client) GetRepository(ctx context.Context, owner, repo string) (*github.Repository, error) {
	repository, _, err := c.client.Repositories.Get(ctx, owner, repo)
	return repository, err
}

// Add more methods as needed for fetching files, etc.
