import requests
import json

def read_creds(filename):
    with open(filename) as f:
        credentials = json.load(f)
    return credentials

def get_user_profile(access_token):
    url = 'https://api.linkedin.com/v2/userinfo'
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    else:
        print("Error:", response.text)
        return None

def share_post(access_token, text_content):
    url = 'https://api.linkedin.com/v2/ugcPosts'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    payload = {
    "author": "urn:li:person:"+ user_sub,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": text_content
            },
            "shareMediaCategory": "ARTICLE",
            "media": [
                {
                    "status": "READY",
                    "description": {
                        "text": "Official LinkedIn Blog - Your source for insights and information about LinkedIn."
                    },
                    "originalUrl": "https://blog.linkedin.com/",
                    "title": {
                        "text": "Official LinkedIn Blog"
                    }
                }
            ]
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.ok:
        return response.json()
    else:
        print("Error:", response.text)
        return None


if __name__ == '__main__':

    credentials = r"C:\Users\CAGRII\Desktop\Yapay-Zeka-Projesi\LinkedinAPI\credentials.json"
    creds = read_creds(credentials)
    access_token = creds['access_token']
    
    # Kullanıcı profili alınması
    user_profile = get_user_profile(access_token)
    user_sub= user_profile.get('sub', '')
    if user_profile:
        print("User Profile:", user_profile)
    
    # Örnek bir post paylaşımı
    text_content="CAGRII POST TRY3"
    share_result = share_post(access_token, text_content)
    if share_result:
        print("Post Shared:", share_result)
