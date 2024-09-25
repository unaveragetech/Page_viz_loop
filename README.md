### README: Proof of Concept for Artificial Visitor & Profile View Inflation

---

# **Artificial Visitor & Profile View Inflation**  
This repository showcases a **Proof of Concept (PoC)** for how some repositories or GitHub profiles could artificially inflate their **visitor count** and **profile view** metrics by using automated scripts to simulate page visits.

## **Introduction**

GitHub provides metrics like **"visitors"** and **"profile views"** that give insight into how many users are viewing a repository or profile. Unfortunately, it's possible to artificially inflate these metrics using automated scripts, which gives a misleading impression of a repository's popularity or activity.

This project serves as a proof of concept for demonstrating how easy it is to create a script that refreshes a GitHub page repeatedly, simulating multiple visitors. It automates page reloads and mimics the behavior of a browser user visiting a page multiple times.

---

## **Table of Contents**
- [Installation](#installation)
- [How the Script Works](#how-the-script-works)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
  - [Automatic Library Installation](#automatic-library-installation)
  - [Headless Chrome Setup](#headless-chrome-setup)
  - [User Input and Feedback](#user-input-and-feedback)
  - [Real Browser Simulation](#real-browser-simulation)
- [Disclaimer](#disclaimer)

---

## **Installation**

This script runs in **GitHub Codespaces** or any environment that supports Python with headless Chrome. You’ll need the following:

### **Requirements:**
- Python 3.6+
- Selenium
- Chrome or Chromium WebDriver

### **Steps:**
1. **Clone this repository**:
    ```bash
    git clone https://github.com/yourusername/Page_viz_loop
    cd Page_viz_loop
    ```

2. **Run the script**:
    In GitHub Codespaces or a local environment, run:
    ```bash
    python driver.py
    ```
    The script will automatically install any missing dependencies.

3. **Enter the number of reloads**:
    When prompted, enter the number of times you want the page to be refreshed.

---

## **How the Script Works**

The script automates page reloads, mimicking a user visiting a GitHub page multiple times. It uses **Selenium** to automate the Chrome browser in a headless mode, simulating real browser behavior with custom headers (like `User-Agent`). 

Key functionalities:
- **User input**: It asks how many times the page should be reloaded.
- **Browser automation**: Selenium automates Chrome in headless mode, refreshing the target GitHub page.
- **Feedback**: The script provides live feedback in the console after each reload.
- **Mimic real behavior**: The browser is set up with realistic headers to look like a genuine visitor.

---

## **Usage**

1. **Launch the Script**:
   After running the script in a GitHub Codespace or local environment, you’ll be prompted to enter the number of times the page should be reloaded.

2. **Example Run**:
    ```bash
    Enter the number of times to reload the page: 10
    Opened URL: https://github.com/unaveragetech
    Reloading page 1/10
    Page reloaded successfully 1/10
    Reloading page 2/10
    Page reloaded successfully 2/10
    ...
    Browser session closed.
    ```

3. **Observe**:
   The script will repeatedly visit the page and simulate visitor behavior, artificially inflating the page view metrics.

---

## **Code Explanation**

### **Automatic Library Installation**

At the beginning of the script, the function `install` checks if the required packages (such as `selenium`) are installed, and installs them if not. This makes the script easy to run without manual setup.

```python
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
```

This ensures that the environment is set up correctly, even in a fresh GitHub Codespace instance.

### **Headless Chrome Setup**

Since GitHub Codespaces and some other environments don't have a GUI, we run Chrome in **headless mode**. This mode allows the browser to run in the background without displaying a user interface.

```python
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resources
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--remote-debugging-port=9222")  # Required for headless
```

These options help ensure that the browser runs smoothly in environments without a graphical interface.

### **User Input and Feedback**

The script asks the user how many times they want the page to be reloaded. If the input is invalid (e.g., not a number or negative), the script will prompt the user to input again:

```python
while True:
    try:
        user_limit = int(input("Enter the number of times to reload the page: "))
        if user_limit > 0:
            break
        else:
            print("Please enter a positive integer.")
    except ValueError:
        print("Invalid input. Please enter a number.")
```

For each page reload, the console outputs feedback to let the user know the progress:

```python
for i in range(limit):
    print(f"Reloading page {i + 1}/{limit}")
    time.sleep(10)  # Wait for 10 seconds
    driver.refresh()  # Refresh the page
    print(f"Page reloaded successfully {i + 1}/{limit}")
```

### **Real Browser Simulation**

To simulate real browser traffic, we set a `User-Agent` header in Chrome to make the requests look like they are coming from a normal browser:

```python
user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument(f"user-agent={user_agent}")
```

This step ensures that the requests are not flagged as bot traffic and appear to be legitimate visitors.

---

## **Disclaimer**

This proof of concept is for **educational purposes only**. Inflating metrics like profile views or visitor counts in an artificial manner is unethical and may violate GitHub’s terms of service. Use this script responsibly and only on profiles or repositories that you own or have permission to test.

We do not endorse or encourage any misuse of this code.

---

This script and README serve as an educational example of how automation tools can manipulate online metrics. Understanding how these systems work is important to prevent misuse and ensure fair metrics reporting across platforms.
