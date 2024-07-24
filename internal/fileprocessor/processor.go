package fileprocessor

import (
	"io/ioutil"
	"os"
	"path/filepath"
)

type Processor struct{}

func NewProcessor() *Processor {
	return &Processor{}
}

func (p *Processor) ProcessDirectory(dir string) (map[string]string, error) {
	files := make(map[string]string)
	err := filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}
		if !info.IsDir() {
			content, err := ioutil.ReadFile(path)
			if err != nil {
				return err
			}
			relPath, _ := filepath.Rel(dir, path)
			files[relPath] = string(content)
		}
		return nil
	})
	return files, err
}
