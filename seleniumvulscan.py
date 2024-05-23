import requests
from bs4 import BeautifulSoup
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url = input("Enter target URL (i.e. 'https://example.com'): ")
driver.get(url)

# Give the page some time to load
time.sleep(5)

# Get the page source after JavaScript has been executed
html_content = driver.page_source

def extract_form_details(form):
    action = form.get_attribute('action')
    method = form.get_attribute('method') or 'get'
    inputs = form.find_elements(By.TAG_NAME, 'input')
    
    form_details = {
        'action': action,
        'method': method.lower(),
        'inputs': []
    }

    for input_tag in inputs:
        input_type = input_tag.get_attribute('type') or 'text'
        input_name = input_tag.get_attribute('name')
        form_details['inputs'].append({'type': input_type, 'name': input_name})

    return form_details

def submit_form(form_details, url, payload):
    target_url = urllib.parse.urljoin(url, form_details['action'])
    data = {input_tag['name']: payload for input_tag in form_details['inputs'] if input_tag['type'] in ['text', 'password']}
    
    if form_details['method'] == 'post':
        response = requests.post(target_url, data=data)
    else:
        response = requests.get(target_url, params=data)
        
    return response

def detect_xss(form_details, url):
    payload = "<script>alert('UH OH')</script>"
    response = submit_form(form_details, url, payload)
    
    
    if payload in response.text:
        print(f"Possible XSS vulnerability detected in form: {form_details}")
    else:
        print(f"No XSS vulnerability detected in form: {form_details}")

# Parse the HTML content using BeautifulSoup with lxml
soup = BeautifulSoup(html_content, 'lxml')     
forms = soup.find_all('form')

print("Forms Found:")
print(forms)  # Debugging: Print forms found

for form in forms:
    # Using XPath to uniquely identify forms
    form_xpath = f'//form[@action="{form.get("action")}"]'
    selenium_form = driver.find_element(By.XPATH, form_xpath)
    form_details = extract_form_details(selenium_form)
    detect_xss(form_details, url)

# Close the Selenium WebDriver
driver.quit()
