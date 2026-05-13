// Example: load passport-photo-specs in Go.
//
// Fetches the dataset from the public API at idphotosnap.com/api/specs
// and demonstrates lookup + validation patterns.
//
// Run: go run main.go
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

// Document mirrors the spec format. Tags match the JSON keys exactly.
type Document struct {
	ID            string   `json:"id"`
	Name          string   `json:"name"`
	Slug          string   `json:"slug"`
	WidthMm       int      `json:"widthMm"`
	HeightMm      int      `json:"heightMm"`
	WidthPx       int      `json:"widthPx"`
	HeightPx      int      `json:"heightPx"`
	DPI           int      `json:"dpi"`
	Background    string   `json:"background"`
	BgColor       string   `json:"bgColor"`
	BgColorLabel  string   `json:"bgColorLabel"`
	Requirements  []string `json:"requirements"`
}

type Country struct {
	ID        string     `json:"id"`
	Name      string     `json:"name"`
	Flag      string     `json:"flag"`
	Documents []Document `json:"documents"`
}

type Response struct {
	Countries []Country `json:"countries"`
}

func fetchSpecs(country string) (*Response, error) {
	url := "https://idphotosnap.com/api/specs?format=raw"
	if country != "" {
		url += "&country=" + country
	}

	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var r Response
	if err := json.NewDecoder(resp.Body).Decode(&r); err != nil {
		return nil, err
	}
	return &r, nil
}

func findDocument(data *Response, slug string) (*Document, *Country) {
	for i := range data.Countries {
		c := &data.Countries[i]
		for j := range c.Documents {
			if c.Documents[j].Slug == slug {
				return &c.Documents[j], c
			}
		}
	}
	return nil, nil
}

func main() {
	// Example 1: filter to Germany
	fmt.Println("=== German document specs ===")
	germany, err := fetchSpecs("germany")
	if err != nil {
		fmt.Printf("error: %v\n", err)
		return
	}
	for _, c := range germany.Countries {
		for _, doc := range c.Documents {
			fmt.Printf("  %-30s %dx%dmm  bg=%s\n", doc.Name, doc.WidthMm, doc.HeightMm, doc.BgColorLabel)
		}
	}

	// Example 2: look up Chinese visa
	fmt.Println("\n=== China visa lookup ===")
	all, err := fetchSpecs("")
	if err != nil {
		fmt.Printf("error: %v\n", err)
		return
	}
	doc, country := findDocument(all, "china-visa-photo")
	if doc != nil {
		fmt.Printf("  %s %s: %dx%dmm\n", country.Name, doc.Name, doc.WidthMm, doc.HeightMm)
		fmt.Printf("  Pixel dims @ %d DPI: %dx%d\n", doc.DPI, doc.WidthPx, doc.HeightPx)
		fmt.Printf("  Background: %s\n", doc.Background)
		fmt.Println("  Top 3 requirements:")
		for i, req := range doc.Requirements {
			if i >= 3 {
				break
			}
			fmt.Printf("    - %s\n", req)
		}
	}

	// Example 3: find all documents using a specific spec
	fmt.Println("\n=== All 35x45mm documents ===")
	count := 0
	for _, c := range all.Countries {
		for _, doc := range c.Documents {
			if doc.WidthMm == 35 && doc.HeightMm == 45 {
				if count < 10 {
					fmt.Printf("  %s %s\n", c.Name, doc.Name)
				}
				count++
			}
		}
	}
	fmt.Printf("  Total: %d documents at 35x45mm (Schengen-style)\n", count)

	// Example 4: validate spec consistency (px should match mm at DPI)
	fmt.Println("\n=== Spec consistency check ===")
	for _, c := range all.Countries {
		for _, doc := range c.Documents {
			expectedPx := int(float64(doc.WidthMm) / 25.4 * float64(doc.DPI))
			if abs(doc.WidthPx-expectedPx) > 2 {
				fmt.Printf("  WARN %s/%s: widthPx=%d expected~%d\n",
					c.Name, doc.Name, doc.WidthPx, expectedPx)
			}
		}
	}
	fmt.Println("  (all warnings printed above, if any)")

	_ = strings.Builder{} // suppress unused import if not used elsewhere
}

func abs(n int) int {
	if n < 0 {
		return -n
	}
	return n
}
