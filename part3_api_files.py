##Part 3: FileI/O, API's and Exception Handling
import os
def file_operations_demo():
    filename = "python_notes.txt"
    #Task 1: File Read and write basics
    inital_notes = [
        "Topic 1: Variables store data. Python is dynamically typed.",
        "Topic 2: Lists are ordered and mutable.",
        "Topic 3: Dictionaries store key-value pairs.",
        "Topic 4: Loops automate repetitive tasks.",
        "Topic 5: Exception handling prevents crashes."
    ]
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for note in inital_notes:
                f.write(note + "\n")
        print(f"File written successfully.")

        extra_notes = [
            "Topic 6: Functions promote code reuse",
            "Topic 7: Python is one of the most easiest programming language to learn"
        ]
        with open(filename, "a", encoding="utf-8") as f:
            for note in extra_notes:
                f.write(note + "\n")
        print("Additional notes appended successfully.")
        #Read and Search
        print("\nReading file content:")
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
            #Numbered Output
            for index, line in enumerate(lines, start=1):
                print(f"{index}. {line.strip()}")
            print(f"\nTotal Number of lines: {len(lines)}")
            #Search for Keyword
            keyword = input("\nEnter a keyword to search for:").strip().lower()
            found = False
            print(f"Results for '{keyword}':")
            for line in lines:
                if keyword in line.lower():
                    print(f"- {line.strip()}")
                    found = True
            if not found:
                print("No matches found.")
        else:
            print(f"File '{filename}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    file_operations_demo()

import requests
BASE_URL = "https://dummyjson.com/products"
def fetch_and_process_products():
    try:
        #Step 1: displaying 20 products 
        print("\n--- Step 1: Fetching 20 products ---")
        response = requests.get(f"{BASE_URL}?limit=20")
        response.raise_for_status() #Checking for HTTP errors

        data = response.json()
        products = data.get("products", [])
        #Formatted table as output
        header = f"{'ID':<4} {'Title':<30} {'Category':<15} {'Price':<8} {'Rating':<6}"
        print(header)
        print("-" * len(header))

        for p in products:
            print(f"{p['id']:<4} {p['title'][:30]:<30} {p['category']:<15} ${p['price']:<7} {p['rating']:<6}") 
        #Step 2: Filter products by category
        print("\n--- Step 2: High Rated Products (Rating >= 4.5) Sorted by Price (Descending) ---")
        filtered_products = [p for p in products if p['rating'] >= 4.5]
        #Sorting by price in descending order
        sorted_products = sorted(filtered_products, key=lambda x: x['price'], reverse=True)

        for p in sorted_products:
            print(f"price: ${p['price']}, rating: {p['rating']:<5}, title: {p['title']}") 

        #Step 3: Search by Category
        print("\n--- Step 3: Laptop Category ---")  
        cat_response = requests.get(f"{BASE_URL}/category/laptops")
        cat_data = cat_response.json()

        for laptop in cat_data.get("products", []):
            print(f"laptop: {laptop['title']}, price: ${laptop['price']}, rating: {laptop['rating']}")
        #Step 4: POST request
        print("\n--- Step 4: Adding a custom product(POST) ---")
        new_product = {
            "title": "Custom Laptop",
            "description": "A powerful laptop for testing.",
            "price": 1500,
            "category": "laptops",
            "rating": 4.8
        }

        post_response = requests.post(f"{BASE_URL}/add", json=new_product)
        print(f"Response from Server:")
        print(post_response.json())
    except requests.exceptions.RequestException as e:
        print(f"Network error occured: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
if __name__ == "__main__":
    fetch_and_process_products()

#Guarded Calculator
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
    except TypeError:
        print("Error: Invalid Input Types.")
#Testing
print(f"10/2 = {safe_divide(10, 2)}")
print(f"10/0 = {safe_divide(10, 0)}")
print(f"10/'a' = {safe_divide(10, 'a')}")

#Part B: Guarded File Reader
def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    finally:
        print(f"File operation attempt complete.")

#Testing
print("\n--- Testing File Reader ---")
read_file_safe("python_notes.txt") #Should Succeed
read_file_safe("ghost_file.tst") #Should fail gracefully

#Part C and B
import requests
def lookup_product():
    BASE_URL = "https://dummyjson.com/products"
    while True:
        user_input = input("\nEnter a product ID to lookup (1-100), or 'exit' to quit: ").strip().lower()
        if user_input == "exit":
            print("Exiting product lookup.")
            break
        #Part D: Input Validation
        if not user_input.isdigit():
            print("Invalid input. Please enter a numeric product ID.")
            continue
        product_id = int(user_input)
        if not (1 <= product_id <= 100):
            print("Product ID must be between 1 and 100.")
            continue
        #Part C: API Call
        try:
            #Adding 5 second timeout window
            response = requests.get(f"{BASE_URL}/{product_id}", timeout=5)
            #Check HTTP status codes
            if response.status_code == 404:
                print(f"Product {product_id} not found.")
            elif response.status_code == 200:
                    data = response.json()
                    print(f"Result: {data['title']} - ₹{data['price']}")
            else:
                    print(f"Unexpected response: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("Network error: Unable to connect to the API.")
        except requests.exceptions.Timeout:
            print("Error: The request timed out.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
if __name__ == "__main__":
    lookup_product()

#Task 4: Production error logger
import requests
from datetime import datetime
import os

LOG_FILE = "error_log.txt"

def log_error(function_name, error_type, error):
    """Writes a timestamped error entry to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {function_name} - {error_type}: {error}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
def trigger_errors():
    #Triggering a connection error
    print("Attempting to reach a non-existent URL")
    fake_url = "https://This-does-not-exist-xyz.com/API"
    try:
        response = requests.get(fake_url, timeout=5)
    except requests.exceptions.ConnectionError as e:
        log_error("trigger_errors", "ConnectionError", "No connection could be made")
        print("Logged ConnectionError.")
    except Exception as e:
        log_error("trigger_errors", "UnexpectedError", str(e))
    #Triggering a HTTP 404 error (Manual Check)
    print("Requesting a non existant product ID(99)")
    product_url = "https://dummyjson.com/products/999"
    try:
        response = requests.get(product_url, timeout=5)
        if response.status_code == 200:
            log_error("trigger_errors", "HTTPError", f"{response.status_code} - Not found for product ID 999")
            print(f"Logged: HTTP {response.status_code} Error")
    except Exception as e:
        log_error("trigger_errors", "RequestError", str(e))
def display_logs():
    print("\n--- current contents of error_log.txt ---")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            print(content if content else "Log File is empty.")
    else:
        print("Log File not found.")
if __name__ == "__main__":
    trigger_errors()
    display_logs()