# HTML & JavaScript Collection Utility

Python-based utility for rendering JavaScript-heavy web applications and extracting fully rendered HTML together with inline and external JavaScript assets.

The tool was developed to support dynamic data extraction workflows involving modern client-side rendered platforms where traditional request-based scraping approaches are insufficient.

## Features

- Full JavaScript page rendering using headless Chrome
- Extraction of rendered HTML content
- Inline and external JavaScript collection
- Relative-to-absolute URL resolution
- API endpoint pattern discovery
- DOM structure visualization
- Consolidated output generation
- Automated external script retrieval
- Output organization for offline analysis

## Tech Stack

- Python
- Selenium
- BeautifulSoup4
- Requests
- Chrome / ChromeDriver

## Architecture

```text
Target URL
     ↓
Headless Browser Rendering
     ↓
Rendered HTML Extraction
     ↓
Script Discovery & Collection
     ↓
External JavaScript Retrieval
     ↓
API Pattern Scanning
     ↓
Consolidated Output Generation
```

## Project Structure

```text
html-collector/
│
├── output/
│
├── collect.py
├── requirements.txt
└── README.md
```

## Key Components

- Headless Selenium rendering engine
- HTML parsing and DOM traversal
- JavaScript extraction workflows
- External asset retrieval utilities
- API endpoint detection module
- Consolidated report generation


## Notes

Designed for dynamic website inspection and JavaScript-heavy scraping workflows involving client-side rendered applications, asynchronous content loading, and reverse-engineering of structured web platforms. The utility was used as part of larger automated data collection pipelines handling dynamic patent marketplace platforms and structured data extraction workflows.
