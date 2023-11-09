import requests
import json

class life360:
    
    base_url = "https://api-cloudfront.life360.com/v3/"
    token_url = "oauth2/token.json"
    circles_url = "circles.json"
    circle_url = "circles/"
    user_agent = "com.life360.android.safetymapd"
    

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
        except requests.exceptions.JSONDecodeError:
            # Hey carter here, I needed to fix this in case we called too many times on accident.
            # I'm not really sure how to *prevent* the API from returning a blank json so we are going to
            # wait for like 10 minutes because when I was pulling my hair out debugging the only way I was able to
            # test again was to wait 10 minutes or so. My best guess is that this is a cooldown for the user and pass for the API.
            print("You are foolish! I told you not to lower the call time for the life360 api. You are now locked out of the API (not by me <3 ) for calling too quickly.\nThe punishment for this crime is waiting 10 minutes because thats the only way I was able to do it before lol.")
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

   