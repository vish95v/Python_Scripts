import requests
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ThreadPoolExecutor

# --- Configuration ---
# File containing all the blog URLs (output from the previous script)
BLOG_URLS_FILE = "all_blog_urls.txt"
# The CSS selector for the element containing the blog post description/content.
# 🚨🚨🚨 You MUST inspect a single blog post page to find this unique selector! 🚨🚨🚨
DESCRIPTION_CONTAINER_SELECTOR = ".container .single-page-blog-content"  # <-- **UPDATE THIS**
# User-Agent to avoid being blocked by some servers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}


# ---------------------

def check_link_status(url):
    """Checks a single URL using a HEAD request."""
    try:
        # Use HEAD request for speed and bandwidth saving
        response = requests.head(url, timeout=10, headers=HEADERS, allow_redirects=True)
        return response.status_code
    except requests.exceptions.RequestException:
        # Catch network errors (timeout, connection refused, etc.)
        return "ERROR"


def find_broken_links_in_blog(blog_url):
    """Visits a single blog, finds all links in the description, and checks them."""
    broken_links = []

    try:
        # 1. Fetch the blog page content
        blog_response = requests.get(blog_url, timeout=15, headers=HEADERS)
        blog_response.raise_for_status()  # Raise exception for 4xx or 5xx status codes

        # 2. Parse the HTML
        soup = BeautifulSoup(blog_response.content, 'html.parser')

        # Find the description container
        desc_container = soup.select_one(DESCRIPTION_CONTAINER_SELECTOR)
        if not desc_container:
            return [(blog_url, "N/A", "ERROR", f"Description selector '{DESCRIPTION_CONTAINER_SELECTOR}' not found.")]

        # 3. Extract all links from the description
        extracted_links = set()
        for a_tag in desc_container.find_all('a', href=True):
            link = a_tag['href']
            # Convert relative links to absolute URLs
            if link.startswith('/'):
                link = requests.compat.urljoin(blog_url, link)

            # Simple filtering for non-http links (like mailto:, #anchors)
            if link.startswith('http'):
                extracted_links.add(link)

        # 4. Check each extracted link
        for link in extracted_links:
            status_code = check_link_status(link)

            if str(status_code) not in ('200', '301', '302'):
                # Log non-successful codes as broken or suspicious
                broken_links.append({
                    'blog_url': blog_url,
                    'broken_link': link,
                    'status_code': status_code,
                    'status': 'BROKEN' if status_code == 404 else 'ERROR/REDIRECT'
                })

    except requests.exceptions.RequestException as e:
        broken_links.append({
            'blog_url': blog_url,
            'broken_link': 'N/A',
            'status_code': 'FETCH_FAIL',
            'status': f"Failed to fetch blog URL: {e}"
        })

    return broken_links


# --- Execution ---
if __name__ == "__main__":

    # 1. Load the blog URLs
    try:
        with open(BLOG_URLS_FILE, 'r') as f:
            blog_urls = [line.strip() for line in f if line.strip()]
        print(f"Loaded {len(blog_urls)} blog URLs for validation.")
    except FileNotFoundError:
        print(f"🛑 ERROR: File '{BLOG_URLS_FILE}' not found. Run the previous Selenium script first.")
        exit()

    all_broken_links = []

    # Use ThreadPoolExecutor for concurrent checking (faster!)
    MAX_WORKERS = 15
    print(f"Starting link validation using {MAX_WORKERS} concurrent threads...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Map the function to the list of URLs and get results as they complete
        results = executor.map(find_broken_links_in_blog, blog_urls)

        for result in results:
            all_broken_links.extend(result)

    # 2. Generate the CSV Report
    report_filename = "broken_links_report.csv"
    if all_broken_links:

        # Filter only the truly broken links (404, ERROR, FETCH_FAIL, 5xx) for the client report
        client_report_data = [
            link for link in all_broken_links
            if link['status_code'] in (404, 'ERROR', 'FETCH_FAIL') or str(link['status_code']).startswith('5')
        ]

        if client_report_data:
            fieldnames = ['blog_url', 'broken_link', 'status_code', 'status']
            with open(report_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(client_report_data)

            print("-" * 50)
            print(f"✅ Validation Complete! Found {len(client_report_data)} broken/error links.")
            print(f"📄 Report saved to '{report_filename}'")
            print("-" * 50)
        else:
            print("🎉 Validation Complete! No truly broken links (404 or Server Errors) found in the descriptions.")

    else:
        print("No issues found in any blog post description.")