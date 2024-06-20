import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
from urllib.request import Request, urlopen

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = Request(
    url=input("Enter URL: (e.g. https://google.com)  \n"),
    headers={'User-Agent': 'Mozilla/5.0'}
)
html = urllib.request.urlopen(req, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

# Retrieve all of the anchor tags
tags = soup('a')
links = [tag.get('href', None) for tag in tags if tag.get('href', None)]

if links:
    # Create a dynamic filename using the current timestamp
    filename = "pahttpge-links.txt"
    
    # Write the links to the file
    with open(filename, "w") as file:
        for link in links:
            file.write(link + "\n")
    
    print(f"Links saved to {filename}")
else:
    print('No links found')
