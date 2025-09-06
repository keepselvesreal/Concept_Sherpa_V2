import os
from bs4 import BeautifulSoup

# Define the file path
file_path = "/home/nadle/projects/Knowledge_Sherpa/v2/25-08-12/posts/source.html"

# Check if the file exists
if not os.path.exists(file_path):
    print(f"Error: The file '{file_path}' was not found.")
else:
    # Read the HTML content from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the main article content using the new class name.
    # The new class name for the post content appears to be 'post-content'.
    post_content = soup.find('div', class_='post-content')

    if post_content:
        # Extract and print the text, preserving paragraphs with newlines
        post_text = post_content.get_text(separator='\n', strip=True)
        print("--- Extracted Post Content ---")
        print(post_text)
    else:
        print("Could not find the main post content. The HTML structure might have changed.")