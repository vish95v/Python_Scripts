import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuration ---
BLOG_PAGE_URL = "https://networkdepot.us/blog"  # <-- **UPDATE THIS**
# The CSS selector for the "Load More" button. Inspect the element on your page!
LOAD_MORE_BUTTON_SELECTOR = "button.load-more"  # <-- **UPDATE THIS**
# The CSS selector for the individual blog post link elements (e.g., <a> tags)
BLOG_LINK_SELECTOR = "a.read-more"  # <-- **UPDATE THIS**
# Path to your WebDriver executable (e.g., chromedriver)
# If the driver is in your PATH, you can use 'Chrome' directly in the service setup.
DRIVER_PATH = "/path/to/your/chromedriver"  # **Optional: UPDATE if needed**


# ---------------------

def get_all_blog_links(url):
    """
    Loads the blog page, clicks 'Load More' until all blogs are visible,
    and returns a set of unique blog post URLs.
    """
    # 1. Setup the WebDriver
    try:
        # Use ChromeOptions to run headless (no visible browser window)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--log-level=3")  # Suppress console warnings

        # Initialize the driver
        # Use Service if you need to specify the driver path, otherwise just use webdriver.Chrome()
        service = Service(DRIVER_PATH) if DRIVER_PATH and DRIVER_PATH != "/path/to/your/chromedriver" else None
        driver = webdriver.Chrome(service=service, options=options)

    except Exception as e:
        print(f"Error setting up WebDriver. Make sure Chrome/Driver are installed and paths are correct. Error: {e}")
        return set()

    print(f"Loading page: {url}")
    driver.get(url)

    # 2. Repeatedly click 'Load More'
    wait = WebDriverWait(driver, 10)

    while True:
        try:
            # Wait until the Load More button is clickable
            load_more_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, LOAD_MORE_BUTTON_SELECTOR))
            )
            print("Clicking 'Load More' button...")
            load_more_button.click()
            # Wait for content to load (adjust time if needed)
            time.sleep(2)

        except:
            # If the button is no longer found or clickable (all content is loaded), break the loop
            print("All blogs loaded or 'Load More' button not found.")
            break

    # 3. Extract all blog links
    blog_links = set()
    try:
        # Find all <a> tags that represent the individual blog post links
        link_elements = driver.find_elements(By.CSS_SELECTOR, BLOG_LINK_SELECTOR)

        for element in link_elements:
            href = element.get_attribute('href')
            if href and href not in blog_links:
                blog_links.add(href)

    except Exception as e:
        print(f"Error extracting links: {e}")

    # 4. Cleanup and return
    driver.quit()
    return blog_links


# --- Execution ---
if __name__ == "__main__":

    if BLOG_PAGE_URL == "YOUR_BLOG_PAGE_URL_HERE":
        print("🛑 ERROR: Please update the 'BLOG_PAGE_URL' variable with your actual blog page URL.")
    else:
        links = get_all_blog_links(BLOG_PAGE_URL)

        if links:
            print("-" * 30)
            print(f"✅ Extracted {len(links)} unique blog links.")
            # Print the first few for a quick check
            print("Sample links:")
            for i, link in enumerate(list(links)[:5]):
                print(f"  {i + 1}. {link}")
            print("-" * 30)

            # Save the full list of links to a file for the next step
            with open("all_blog_urls.txt", "w") as f:
                for link in links:
                    f.write(link + "\n")
            print("Full list of blog URLs saved to 'all_blog_urls.txt'")