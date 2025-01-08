import requests
from requests.auth import HTTPDigestAuth
from dotenv import load_dotenv
import os

def get_public_ip():
    response = requests.get("https://api.ipify.org")
    return response.text

def add_ip_to_atlas():
    atlas_group_id = "67732ef17724126e525745e0"
    load_dotenv()

    atlas_api_key_public = "jwheqkpk"
    atlas_api_key_private = os.getenv("ATLAS_API_KEY_PRIVATE")
    
    ip = get_public_ip()
    resp = requests.post(
        "https://cloud.mongodb.com/api/atlas/v1.0/groups/{atlas_group_id}/accessList".format(atlas_group_id=atlas_group_id),
        auth=HTTPDigestAuth(atlas_api_key_public, atlas_api_key_private),
        json=[{'ipAddress': ip, 'comment': 'From PythonAnywhere'}]  # the comment is optional
    )
    if resp.status_code in (200, 201):
        print("MongoDB Atlas accessList request successful", flush=True)
    else:
        print(
            "MongoDB Atlas accessList request problem: status code was {status_code}, content was {content}".format(
                status_code=resp.status_code, content=resp.content
            ),
            flush=True
        )
