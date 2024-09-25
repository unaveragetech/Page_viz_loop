import subprocess
import sys
import time
import random
import threading
import statistics
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from ping3 import ping

# Function to install required packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check for required packages and install if missing
required_packages = ['selenium', 'ping3']

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"{package} not found. Installing...")
        install(package)

# List of different user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
]

# Function to simulate random user interactions
def simulate_user_interactions(driver):
    try:
        actions = ActionChains(driver)
        # Generate random offsets within the bounds of the window size
        width = driver.execute_script("return window.innerWidth")
        height = driver.execute_script("return window.innerHeight")
        x_offset = random.randint(0, width - 1)
        y_offset = random.randint(0, height - 1)
        
        actions.move_by_offset(x_offset, y_offset).perform()
        time.sleep(random.uniform(0.5, 2.0))
        # Simulate scroll
        driver.execute_script(f"window.scrollTo(0, {random.randint(100, 500)});")
    except Exception as e:
        print(f"Interaction error: {e}")

# Function to handle browser automation and page reload
def auto_reload(url, limit, initial_views, thread_num, lock, stats):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    
    # Set random user agent for each thread
    user_agent = random.choice(user_agents)
    chrome_options.add_argument(f"user-agent={user_agent}")
    
    # Set random screen size for each thread (to simulate different devices)
    screen_width = random.randint(1024, 1920)
    screen_height = random.randint(768, 1080)
    chrome_options.add_argument(f"--window-size={screen_width},{screen_height}")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    # Simulate ping
    ping_time = ping('github.com')
    if ping_time is not None:
        print(f"Thread-{thread_num}: Ping time to GitHub: {ping_time * 1000:.2f} ms")
    else:
        print(f"Thread-{thread_num}: Ping request failed. Host may be unreachable.")
        ping_time = 0  # Assign a default value in case of failure
    
    load_times = []
    
    print(f"Thread-{thread_num}: Opened URL: {url} with User-Agent: {user_agent}, Screen Size: {screen_width}x{screen_height}")

    for i in range(limit):
        start_time = time.time()
        simulate_user_interactions(driver)  # Simulate interactions like scroll, mouse move
        driver.refresh()  # Reload page
        load_time = time.time() - start_time
        load_times.append(load_time)
        
        print(f"Thread-{thread_num}: Page reloaded {i + 1}/{limit} (Load time: {load_time:.2f} sec)")
        
        time.sleep(random.uniform(5, 15))  # Randomized delay
    
    driver.quit()
    
    # Lock to ensure thread safety when accessing shared data
    with lock:
        if ping_time > 0:  # Only append if the ping was successful
            stats['ping_times'].append(ping_time)
        stats['load_times'].extend(load_times)
        stats['total_reloads'] += limit

# Function to handle multi-threaded execution
def multi_thread_reload(url, limit, initial_views, threads_count):
    lock = threading.Lock()  # Lock for thread safety
    stats = {
        'ping_times': [],
        'load_times': [],
        'total_reloads': 0
    }
    
    threads = []
    reloads_per_thread = limit // threads_count

    for i in range(threads_count):
        t = threading.Thread(target=auto_reload, args=(url, reloads_per_thread, initial_views, i + 1, lock, stats))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    final_views = initial_views + stats['total_reloads']
    
    # Return stats summary
    avg_ping = statistics.mean(stats['ping_times']) if stats['ping_times'] else 0
    avg_load_time = statistics.mean(stats['load_times']) if stats['load_times'] else 0
    print(f"\nApproximate gain in views: {stats['total_reloads']} (from {initial_views} to {final_views})")
    print(f"Average ping time: {avg_ping:.2f} ms")
    print(f"Average page load time: {avg_load_time:.2f} sec")
    print(f"Total reloads: {stats['total_reloads']}")

# Main script logic
if __name__ == "__main__":
    default_url = "https://github.com/unaveragetech"
    
    # Ask for the GitHub profile URL or use default
    url = input(f"Enter the GitHub profile URL to visit (default: {default_url}): ") or default_url
    
    # Ask for the number of times to reload the page
    while True:
        try:
            user_limit = int(input("Enter the number of times to reload the page: "))
            if user_limit > 0:
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Ask for the current number of views
    while True:
        try:
            initial_views = int(input("Enter the current number of profile views: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Ask for the number of threads to use
    while True:
        try:
            threads_count = int(input("Enter the number of threads to use (recommended: 4): "))
            if threads_count > 0:
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Start multi-threaded page reloading with stats collection
    multi_thread_reload(url, user_limit, initial_views, threads_count)
