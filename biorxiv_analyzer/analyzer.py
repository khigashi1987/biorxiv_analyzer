import requests
from bs4 import BeautifulSoup
import urllib.parse

class BioRxivAnalyzer:
    def __init__(self):
        self.base_url = "https://www.biorxiv.org/search/"
        self.api_url = "https://api.biorxiv.org/details/biorxiv/"

    def search_dois(self, query, search_type="AND", max_pages=None, date_range=None):
        """
        Search bioRxiv for a specific query and return the list of DOIs from all result pages.

        Parameters:
        query (str): Search query. For example, "gut microbiome".
        search_type (str): Type of search. Either "AND" or "OR".
        max_pages (int): Maximum number of pages to fetch. If None, fetch all pages.
        date_range (str): Date range filter in the format "YYYY-MM-DD TO YYYY-MM-DD".

        Returns:
        list: List of DOIs from the search results.
        """
        # Encode the query based on the search type
        if search_type == "AND":
            search_query = "%20AND%20".join(urllib.parse.quote(word) for word in query.split())
        elif search_type == "OR":
            search_query = "%20OR%20".join(urllib.parse.quote(word) for word in query.split())
        else:
            raise ValueError("search_type must be either 'AND' or 'OR'")

        # Add date range filter if specified
        if date_range:
            start_date, end_date = date_range.split(" TO ")
            search_query += f"%20limit_from%3A{urllib.parse.quote(start_date)}%20limit_to%3A{urllib.parse.quote(end_date)}"

        search_url = f"{self.base_url}{search_query}%20numresults%3A10%20sort%3Arelevance-rank"

        doi_list = []
        seen_dois = set()
        page = 0

        while True:
            # Fetch the search results page
            current_url = f"{search_url}?page={page}"
            response = requests.get(current_url)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch bioRxiv search results. HTTP Status Code: {response.status_code}")

            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract DOIs from the current page's search results
            articles = soup.find_all("li", class_="search-result")
            if not articles:
                break  # Exit loop if no more articles are found

            new_dois = []
            for article in articles:
                doi_tag = article.find("span", class_="highwire-cite-metadata-doi")
                if doi_tag:
                    doi_text = doi_tag.get_text(strip=True).replace("https://doi.org/", "")
                    if doi_text not in seen_dois:  # Avoid duplicates
                        new_dois.append(doi_text)
                        seen_dois.add(doi_text)

            # If no new DOIs are found, stop the loop
            if not new_dois:
                break

            doi_list.extend(new_dois)

            # Stop if max_pages is reached
            page += 1
            if max_pages is not None and page >= max_pages:
                break

        return doi_list

    def get_metadata(self, doi):
        """
        Fetch metadata for a given DOI from bioRxiv API.

        Parameters:
        doi (str): DOI of the preprint.

        Returns:
        dict: Metadata of the preprint.
        """
        url = f"{self.api_url}{doi.replace('doi:', '')}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch metadata for DOI {doi}. HTTP Status Code: {response.status_code}")

        data = response.json()
        if data["messages"][0]["status"] != "ok":
            raise Exception(f"Error in API response for DOI {doi}.")

        return data["collection"]

    def get_xml(self, metadata):
        """
        Fetch and parse the JATS XML for a given preprint metadata.

        Parameters:
        metadata (dict): Metadata dictionary containing "jatsxml" key.

        Returns:
        str: JATS XML content.
        """
        xml_url = metadata.get("jatsxml")
        if not xml_url:
            raise ValueError("Metadata does not contain 'jatsxml' key.")

        response = requests.get(xml_url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch JATS XML. HTTP Status Code: {response.status_code}")

        return response.text


# Example usage
if __name__ == "__main__":
    analyzer = BioRxivAnalyzer()

    # Step 1: Search for DOIs
    query = "deep learning microbiome"
    search_type = "AND"
    max_pages = 2
    date_range = "2024-12-13 TO 2024-12-31"
    try:
        dois = analyzer.search_dois(query, search_type, max_pages, date_range)
        print("Found DOIs:", dois)

        # Step 2: Get metadata for the first DOI
        if dois:
            metadata = analyzer.get_metadata(dois[0])
            #print("Metadata:", metadata)

            # Step 3: Get XML for the first version of the metadata
            if metadata:
                xml_content = analyzer.get_xml(metadata[0])
                with open(f"xml_content.xml", "w") as f:
                    f.write(xml_content)
    except Exception as e:
        print("Error:", e)
