import requests

CLOUD_NAME = "dswqmwcwl"  # Replace with your Cloudinary cloud name
UPLOAD_PRESET = "PATIENTS"  # Replace with your upload preset name

def upload_image(image, public_id):
    url = f"https://api.cloudinary.com/v1_1/{CLOUD_NAME}/image/upload"
    files = {'file': image}
    data = {
        'upload_preset': UPLOAD_PRESET,
        'public_id': public_id
    }
    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        return response.json().get('secure_url')
    else:
        return None
