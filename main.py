import requests
import os

                    # Constants
API_KEY = 'YOUR_STEAM_API_KEY'  # Replace with your Steam API Key
WORKSHOP_ITEM_ID = input()  # Input item's ID
DOWNLOAD_DIRECTORY = './steam_workshop_items' # Replace with your actuall download directory

                    # Function to get the workshop item details
def get_workshop_item_details(item_id):
    url = f'https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/'
    params = {
        'key': API_KEY,
        'itemcount': 1,
        'publishedfileids[0]': item_id
    }
    response = requests.post(url, json=params)
    return response.json()

                    # Function to download file from URL
def download_file(url, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f'Downloaded: {filename}')
    else:
        print(f'Failed to retrieve the file from {url}')

                    # Main function
def main():
                    # Get workshop item details
    item_details = get_workshop_item_details(WORKSHOP_ITEM_ID)

    if item_details.get('response') and len(item_details['response']['publishedfiledetails']) > 0:
        details = item_details['response']['publishedfiledetails'][0]
        download_url = details['file_url']
        item_filename = details['filename']  # Get the filename from the response

                    # Download the file
        download_file(download_url, DOWNLOAD_DIRECTORY, item_filename)
    else:
        print('Failed to retrieve item details.')

if __name__ == "__main__":
    main()
