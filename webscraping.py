import urllib.request
import urllib.error

# URL of the web page you want to download
url = 'https://sfbay.craigslist.org/search/apa#search=1~gallery~0~0'

# Set a User-Agent header to simulate a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
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

