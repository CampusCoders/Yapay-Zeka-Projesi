import requests
import json
from LinkedinAPI.linkedin_token_utils import credentials, read_creds
import re

import re

def format_linkedin_content(html_content):
    # HTML etiketlerini LinkedIn'in desteklediği biçimlendirme ile değiştir
    html_content = html_content.replace('<h2>', '**').replace('</h2>', '**\n')
    html_content = html_content.replace('<h3>', '**').replace('</h3>', '**\n')
    html_content = html_content.replace('<h4>', '**').replace('</h4>', '**\n')
    html_content = html_content.replace('<p>', '').replace('</p>', '\n')
    html_content = html_content.replace('<strong>', '**').replace('</strong>', '**')
    html_content = html_content.replace('<b>', '**').replace('</b>', '**')
    html_content = html_content.replace('<i>', '_').replace('</i>', '_')
    html_content = html_content.replace('<em>', '_').replace('</em>', '_')
    html_content = html_content.replace('<ul>', '').replace('</ul>', '')
    html_content = html_content.replace('<li>', '- ').replace('</li>', '\n')
    
    # Diğer HTML etiketlerini düz metin olarak temizle
    clean_text = re.sub('<[^<]+?>', '', html_content)
    
    # Birden fazla boşluğu ve satır sonlarını tek bir boşluk/satır sonu ile değiştir
    clean_text = re.sub('\n\s*\n', '\n\n', clean_text)
    clean_text = re.sub(' +', ' ', clean_text).strip()
    
    return clean_text

def get_user_profile(access_token):
    url = 'https://api.linkedin.com/v2/userinfo'
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    else:
        print("Error:", response.text)
        return None

def share_post(access_token, text_content, user_sub):
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
