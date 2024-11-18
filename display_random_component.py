import random
from bs4 import BeautifulSoup
import webbrowser

# Load the HTML content from the saved HTML file
with open('webpage_with_imagesv2.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the <ol> tag, which contains the <div> elements
ol_tag = soup.find('ol')

# print(ol_tag.prettify())

first_level_divs = [div for div in ol_tag.find_all('div', recursive=False)]

# for div in first_level_divs:
#     print(div.prettify())
# print(first_level_divs[0].prettify())

def has_valid_image(div):
    # Find all <img> tags within this <div>
    img_tags = div.find_all('img')

    if (img_tags):
        for img in img_tags:
            # Check if the src attribute is a valid URL (does not contain 'data:image/png;base64')
            src = img.get('src', '')
            if src and not src.startswith('data:image'):
                return True  # Return True if there's a valid external image
        
    return False  # Return False if no valid image is found

valid_divs = [div for div in first_level_divs if has_valid_image(div)]

# Randomly select one of the divs
selected_div = random.choice(valid_divs)

# Create a new HTML page that contains only the selected <div>
new_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Random Component</title>
</head>
<body>
    {selected_div.prettify()}  <!-- Display the selected div -->
</body>
</html>
"""

# Save the new HTML page to a temporary file
with open('random_component.html', 'w', encoding='utf-8') as file:
    file.write(new_html)

# Open the new HTML file in the default web browser
webbrowser.open('random_component.html')

print("Random component generated.")
