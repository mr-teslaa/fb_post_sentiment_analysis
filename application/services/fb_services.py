import requests

class FacebookAPI:
    def __init__(self):
        self.redirect_uri = "https://127.0.0.1:5000/login_fb" #"https://pulsemngr.com/login_fb" #"https://ar-partners.fr/leads/fb/login.php"
        self.app_id = '452202687413443';
        self.app_secret = '72077871a729f9386c54325f6780bb99';
        self.scope = ("read_insights,pages_show_list,ads_management,ads_read,business_management,"
                        "leads_retrieval,pages_manage_ads,"
                        "pages_read_engagement,pages_read_user_content,pages_manage_engagement")
        self.base_graph_url = "https://graph.facebook.com/v20.0"
        self.base_url = "https://www.facebook.com/v20.0"

        # THIS ACCESS TOKEN WILL BE REPLACED A DYNAMIC USER ACCESS TOKEN LATER
        self.access_token = "EAAGbRqSMvMMBO8gNVZCHewZCtFsx95I3kCSZCtnQGh6nNOaWcJWEAMT8MZApSH75xKRVyV7csZCGwV5D7UxuOqrjQUBSL9BS95txMGN3wZC8zZCd7Cmw8thidSuGBHlZAxB6E48O4UMUBmmxIm7oHvZCZCPBYdEqkKZAI2VGll2R9p4ACVWrytbxOxzh1jV",


    def get_pages(self):
        url = f"{self.base_graph_url}/me/accounts"
        params = {
            "access_token": self.access_token
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('data', [])
        return []
    
    def get_page_access_token(self, page_id):
        url = f"{self.base_graph_url}/{page_id}?fields=access_token"
        params = {
            "access_token": self.access_token
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('access_token', None)
        return None

    def get_posts(self, page_id):
        # First get the Page Access Token
        page_access_token = self.get_page_access_token(page_id)

        # If we couldn't get the Page Access Token, return an empty list
        if not page_access_token:
            return []

        # Now fetch the posts using the Page Access Token
        url = f"{self.base_graph_url}/{page_id}/posts"
        params = {
            "access_token": page_access_token
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('data', [])
        return []
    
    def get_comments(self, post_id, page_access_token):
        url = f"{self.base_graph_url}/{post_id}/comments"
        params = {
            "fields": "message,created_time",
            "access_token": page_access_token
        }
        response = requests.get(url, params=params)
        print('--------- getting comments -----------')
        print('post id: ', post_id)
        print('url: ', url)
        print('page_access_token: ', page_access_token)
        if response.status_code == 200:
            return response.json().get('data', [])
        return []