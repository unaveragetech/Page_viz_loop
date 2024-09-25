import subprocess
import sys
import time

# Function to install a package if it's not already installed
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install Selenium if not already installed
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
except ImportError:
    print("Selenium not found. Installing...")
    install("selenium")
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options

# Function to navigate to the page and reload
def auto_reload(url, limit):
    # Set up Chrome options for headless mode and set headers
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--remote-debugging-port=9222")  # Needed for remote debugging

    # Add a User-Agent to mimic a real browser request
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument(f"user-agent={user_agent}")

    # Initialize the WebDriver (using Chrome in headless mode)
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Error initializing Chrome WebDriver: {e}")
        return

    try:
        # Navigate to the specified URL
        driver.get(url)
        print(f"Opened URL: {url}")

        for i in range(limit):
            print(f"Reloading page {i + 1}/{limit}")
            time.sleep(5)  # Wait for 5 seconds between reloads
            driver.refresh()  # Refresh the page
            print(f"Page reloaded successfully {i + 1}/{limit}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()  # Ensure the browser is closed
        print("Browser session closed.")

if __name__ == "__main__":
    url = "https://github.com/unaveragetech"
    
    # Prompt the user for the number of reloads
    while True:
        try:
            user_limit = int(input("Enter the number of times to reload the page: "))
            if user_limit > 0:
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    auto_reload(url, user_limit)
