import requests
import os

def download_file(url, download_dir):
    local_filename = os.path.join(download_dir, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f'Downloaded: {local_filename}')
