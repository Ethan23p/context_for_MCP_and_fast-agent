# download_docs_llms.py
# This script downloads the LLMs.txt and llms-full.txt files from the Model Context Protocol (MCP) and fast-agent.ai websites.
import requests
from datetime import datetime
import os
from urllib.parse import urlparse # Though not directly used for naming, good for URL parsing

# --- Configuration ---
# Define a dictionary where keys are the URLs and values are the desired output filenames
# Make sure to include the .txt extension in your desired filenames
urls_to_filenames = {
    "https://fast-agent.ai/llms.txt": "fast_agent_full_documentation_llms.txt",
    "https://modelcontextprotocol.io/llms-full.txt": "ModelContextProtocol_full_documentation_llms.txt",
    # Add more URLs and their desired filenames here
    # "https://example.com/another_doc.txt": "example_another_doc.txt",
}

# Directory to save the files.
# Using os.path.abspath ensures this path is absolute and not relative to some changing CWD.
# You can change 'downloaded_docs' to a full path like 'C:\MyDocs\DownloadedAI' if preferred.
output_directory_name = "downloaded_docs"
script_dir = os.path.dirname(os.path.abspath(__file__)) # Get directory of the current script
output_directory = os.path.join(script_dir, output_directory_name)
# --- End Configuration ---

# Get the current date for the "last fetched" note
current_date = datetime.now().strftime("%Y-%m-%d")

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

print(f"Starting document download and processing.")
print(f"Output directory will be: {output_directory}") # CONFIRM THE PATH
print(f"Current fetch date: {current_date}")
print("-" * 40)

for url, desired_filename in urls_to_filenames.items():
    try:
        print(f"Processing URL: {url}")

        # Construct the full path for the output file
        output_filepath = os.path.join(output_directory, desired_filename)

        # Skip download if file already exists with this name and current date? (Optional)
        # if os.path.exists(output_filepath):
        #     print(f"  File already exists: {output_filepath}. Skipping download.")
        #     print("-" * 40)
        #     continue

        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # Get the 'Last-Modified' header if available
        last_modified = response.headers.get('Last-Modified')
        site_update_info = f"Site Last-Modified: {last_modified}\n" if last_modified else "Site Last-Modified: Not available\n"

        # Prepare the content with the prepended note and site update info
        prepended_note = f"info last fetched on: {current_date}\n"
        full_content = prepended_note + site_update_info + response.text

        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)

        print(f"  Successfully downloaded and saved as: {output_filepath}") # CONFIRM SAVED PATH
        if last_modified:
            print(f"  Site last updated (Last-Modified header): {last_modified}")
        else:
            print("  Site Last-Modified header not found.")
        print("-" * 40)

    except requests.exceptions.RequestException as e:
        print(f"  Error downloading {url}: {e}")
        print("-" * 40)
    except Exception as e:
        print(f"  An unexpected error occurred for {url}: {e}")
        print("-" * 40)

print("Document download and processing complete.")