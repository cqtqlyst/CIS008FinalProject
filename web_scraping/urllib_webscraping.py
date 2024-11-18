import urllib.request
import urllib.error
import random

# URL of the web page you want to download
url = 'https://sfbay.craigslist.org/search/apa#search=1~gallery~0~0'

# Set a User-Agent header to simulate a browser request
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/90.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.64',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:36.0) Gecko/20100101 Firefox/36.0'
]

random_user_agent = random.choice(user_agents)

headers = {
    'User-Agent': random_user_agent
}

# Create a request with the custom headers
req = urllib.request.Request(url, headers=headers)


# Attempting to download the website

try:
    # Download the webpage content
    with urllib.request.urlopen(req) as response:
        # Read the content
        web_content = response.read()

    # Save the content to an HTML file
    with open('webpage.html', 'wb') as file:
        file.write(web_content)

    print('Web page downloaded and saved as "webpage.html"')

except urllib.error.HTTPError as e:
    print(f"HTTP error occurred: {e.code}")
except urllib.error.URLError as e:
    print(f"URL error occurred: {e.reason}")
except Exception as e:
    print(f"An error occurred: {str(e)}")


# does the same thing

# import requests

# url = "https://sfbay.craigslist.org/search/apa#search=1~gallery~0~0"

# response = requests.get(url)
# print(response.text)
