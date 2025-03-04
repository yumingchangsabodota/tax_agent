import os
import time
import tempfile
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth

TAX_DOC_PAGE = "https://fbfh.trade.gov.tw/fh/ap/listCCCf.do"

# Set your download directory (make sure it exists)
download_dir = os.path.join(os.getcwd(), "db/migration/tax_pdf")
os.makedirs(download_dir, exist_ok=True)

# Create a unique temporary directory for Chrome user data
user_data_dir = tempfile.mkdtemp()
print(f"User data directory: {user_data_dir}")

# Configure Chrome options for headless operation and auto-downloads
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument("--single-process")


prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    # Ensure PDFs are downloaded instead of opened in the browser
    "plugins.always_open_pdf_externally": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Specify the path to ChromeDriver.
# Use the environment variable set in the container or specify directly
chromedriver_path = os.environ.get(
    "CHROMEDRIVER_PATH", "/usr/bin/chromedriver")
service = Service(executable_path=chromedriver_path)

# Create the driver with the Service
driver = webdriver.Chrome(service=service, options=chrome_options)
# After creating the driver:
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

try:
    # Open the target page
    driver.get(TAX_DOC_PAGE)

    # Wait for the page to load fully
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "a")))

    download_links = driver.find_elements(
        By.XPATH, '//a[contains(@href, "javascript:downloadFile") and contains(@class, "text-success")]')
    print(f"Found {len(download_links)} download link(s).")

    # Iterate over each download link and click it
    for index, link in enumerate(download_links):
        print(link)
        try:
            # wait.until(EC.element_to_be_clickable(link))
            # link.click()
            actions = ActionChains(driver)
            actions.move_to_element(link).click().perform()
            print(f"Clicking download link {index}...")

            slp_time = random.uniform(1, 2)
            print(f"Sleeping for {slp_time} seconds...")
            driver.implicitly_wait(slp_time)

        except Exception as e:
            print(f"Could not click link {index}: {e}")

    print("Download should have completed. Check the 'downloads' folder.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
