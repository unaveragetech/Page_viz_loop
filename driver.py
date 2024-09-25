import subprocess
import sys

# Function to install a package if it's not already installed
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install Selenium if not already installed
try:
    import selenium
except ImportError:
    print("Selenium not found. Installing...")
    install("selenium")

from selenium import webdriver
import time

# Function to navigate to the page and reload
def auto_reload(url, limit):
    # Initialize the WebDriver (using Chrome in this case)
    driver = webdriver.Chrome()

    try:
        # Navigate to the specified URL
        driver.get(url)

        for i in range(limit):
            print(f"Reloading... {i + 1}/{limit}")
            time.sleep(10)  # Wait for 10 seconds
            driver.refresh()  # Refresh the page
    finally:
        driver.quit()  # Ensure the browser is closed

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
