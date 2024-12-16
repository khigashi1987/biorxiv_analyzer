# BioRxiv Analyzer

A Python library for searching, retrieving, and analyzing metadata and XML content from bioRxiv.

## Features
1. Query bioRxiv to retrieve DOIs based on search criteria.
2. Fetch metadata for a given DOI using the bioRxiv API.
3. Download and parse JATS XML content for a preprint.

## Installation
Clone the repository and install required dependencies:
```bash
git clone <repository-url>
cd biorxiv-analyzer
pip install -r requirements.txt
```

## Usage
```python
from biorxiv_analyzer import BioRxivAnalyzer

analyzer = BioRxivAnalyzer()

# Search for DOIs
query = "gut microbiome"
dois = analyzer.search_dois(query, search_type="AND", max_pages=2)

# Fetch metadata
if dois:
    metadata = analyzer.get_metadata(dois[0])

# Fetch XML
if metadata:
    xml_content = analyzer.get_xml(metadata[0])
```

## Dependencies
- `requests`
- `beautifulsoup4`

## License
MIT License
