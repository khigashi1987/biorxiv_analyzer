import pytest
from biorxiv_analyzer.analyzer import BioRxivAnalyzer

def test_search_dois():
    analyzer = BioRxivAnalyzer()
    query = "gut microbiome"
    dois = analyzer.search_dois(query, max_pages=1)
    assert isinstance(dois, list)

def test_get_metadata():
    analyzer = BioRxivAnalyzer()
    doi = "10.1101/2024.09.30.615889"
    metadata = analyzer.get_metadata(doi)
    assert "title" in metadata[0]

def test_get_xml():
    analyzer = BioRxivAnalyzer()
    metadata = {
        "jatsxml": "https://www.biorxiv.org/content/early/2024/05/30/2024.05.27.596126.source.xml"
    }
    xml_content = analyzer.get_xml(metadata)
    assert xml_content.startswith("<?xml")

