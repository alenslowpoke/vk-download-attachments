from datetime import datetime

import requests

# Define variables:
# 1. VK API version
# 2. Access-Token
# 3. Media Type ('photo, audio etc)
# 4. Peer ID
# 5. Download Folder
api_version = '5.78'
access_token = '<access_token>'
media_type = 'photo'
peer_id = '<peer_id>'
attachments_url = 'https://api.vk.com/method/messages.getHistoryAttachments?v=%s&access_token=%s&media_type=%s&peer_id=%s' % (
api_version, access_token, media_type, peer_id)
download_folder = '<download_folder>'


def logging(message):
    print(str(datetime.now()) + ' - ' + message)


def send_request(request_url):
    response = requests.get(request_url)
    return response.status_code, response.json()


def main():
    running = True
    start_from = ''
    while running:
        status, response = send_request(attachments_url + start_from)
        print(response)
        if status == 200:
            data = response['response']
            if 'next_from' in data:
                items = data['items']
                for item in items:
                    photo_url = item['attachment']['photo']['sizes'][6]['url']
                    filename = photo_url.split('/')[-1]
                    r = requests.get(photo_url)
                    if r.status_code == 200:
                        open(download_folder + filename, 'wb').write(r.content)
                        logging('Photo downloaded!')
                    else:
                        logging('Failed to download!')
                start_from = '&start_from=' + data['next_from']
            else:
                running = False
        else:
            logging('Error ' + str(status))
    logging('Download complete!')


if __name__ == "__main__":
    main()
