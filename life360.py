import requests
import json

class life360:
    
    base_url = "https://api-cloudfront.life360.com/"
    token_url = "v3/oauth2/token"
    circles_url = "v4/circles"
    circle_url = "circles/"
    user_agent = "com.life360.android.safetymapd/KOKO/23.49.0 android/13"


    def __init__(self, authorization_token=None, username=None, password=None):
        self.authorization_token = authorization_token
        self.username = username
        self.password = password

    def make_request(self, url, params=None, method='GET', authheader=None):
        headers = {'Accept': 'application/json', "user-agent": self.user_agent}
        if authheader:
            headers.update({'Authorization': authheader, 'cache-control': "no-cache",})
        
        if method == 'GET':
            try:
                r = requests.get(url, headers=headers, timeout=30)
            except requests.exceptions.Timeout:
                print("Timed out")
                self.make_request(self, url, params=None, method='GET', authheader=None)
            
        elif method == 'POST':
            try:
                r = requests.post(url, data=params, headers=headers, timeout=30)
            except requests.exceptions.Timeout:
                print("Timed out")
                self.make_request(self, url, params=None, method='GET', authheader=None)
        try:
            
            return r.json()
        except requests.exceptions.JSONDecodeError as E:
            print(f"There has been an issue connecting to life360's servers! | {E}")
            from time import sleep
            sleep(600)


    def authenticate(self):
        

        url = self.base_url + self.token_url
        params = {
            "grant_type":"password",
            "username":self.username,
            "password":self.password,
        }

        r = self.make_request(url=url, params=params, method='POST', authheader="Basic " + self.authorization_token)
        try:
            self.access_token = r['access_token']
            return True
        except:
            return False

    def get_circles(self):
        url = self.base_url + self.circles_url
        authheader="bearer " + self.access_token
        r = self.make_request(url=url, method='GET', authheader=authheader)
        return r['circles']

    def get_circle(self, circle_id):
        url = self.base_url + self.circle_url + circle_id
        authheader="bearer " + self.access_token
        r = self.make_request(url=url, method='GET', authheader=authheader)
        return r

    def get_circle_members(self, circle_id):
        authheader="bearer " + self.access_token
        r = self.make_request(url = f"https://api-cloudfront.life360.com/v4/circles/{circle_id}/members".format(circle_id=circle_id), method="GET", authheader=authheader)["members"]
        return r

    def get_circle_places(self, circle_id):
        authheader="bearer " + self.access_token
        r = self.make_request(url = f"https://api-cloudfront.life360.com/v4/circles/{circle_id}/places".format(circle_id=circle_id), method="GET", authheader=authheader)["places"]
        return r

    def update_user(self, circle_id, member_id):
        authheader="bearer " + self.access_token
        request = self.make_request(url = f"https://api-cloudfront.life360.com/v3/circles/{circle_id}/members/{member_id}/request".format(circle_id=circle_id,member_id=member_id), method="POST", params={"type": "location"}, authheader=authheader)
        requestID = request["requestId"]
        r = self.make_request(url = f"https://api-cloudfront.life360.com/v3/circles/members/request/{requestID}".format(requestID=requestID), method="GET", params={"type": "location"}, authheader=authheader)
        return r