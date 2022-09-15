from random import choice
from string import ascii_letters, digits
from http import HTTPStatus
from os.path import exists as file_exists
import requests
from oauthlib.oauth2 import WebApplicationClient

# 1. built auth url to twitch, click authorise
# 2. redirect back this this page with query params
# 3. check that query params are valid
# 4. request auth token from twitch api
# 5. use auth token to make request to resource api


class TwitchApi:
    def __init__(self, client_id, client_secret, redirect_uri, scope,
                 grant_type):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.grant_type = grant_type
        self.state_string = self.generate_state_string()
        self.data = {}
        self.oauth2_client = WebApplicationClient(self.client_id)
        self.auth_link = self.build_auth_link()
        self.token = None
        self.endpoints = {
            "users": {
                "url": "https://api.twitch.tv/helix/users",
                "http_method": "GET",
                "params": ["id", "login"]
            },
            "follows": {
                "url": "https://api.twitch.tv/helix/users/follows",
                "http_method": "GET",
                "params": ["from_id", "to_id"]
            },
            "token": {
                "url": "https://id.twitch.tv/oauth2/token",
                "http_method": "POST",
                "params": ["client_id", "client_secret", "grant_type"]
            }
        }

    def generate_state_string(self):
        chars = ascii_letters + digits
        return "".join([choice(chars) for i in range(24)])

    def build_auth_link(self):
        kwargs = {
            "uri": "https://id.twitch.tv/oauth2/authorize",
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "state": self.state_string
        }
        return self.oauth2_client.prepare_request_uri(**kwargs)

    def twitchAuthResponseIsValid(self, query):
        if "code" in query.keys() and "scope" in query.keys() \
                and "state" in query.keys():
            if query["state"] == self.state_string:
                return True
        return False

    def fetch_auth_token(self, code):
        request_body = self.oauth2_client.prepare_request_body(**{
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        })

        try:
            token_response = requests.post(self.endpoints["token"]["url"],
                                           data=request_body)
            if token_response.status_code == HTTPStatus.OK:
                self.token = token_response.json()
        except Exception as exc:
            raise Exception("Failed to obtain token") from exc

    def token_is_valid(self):
        if self.token is None:
            return False
        if "access_token" in self.token.keys():
            return True

    def fetch_user(self, login):
        if self.token_is_valid() is False:
            raise Exception("Must first obtain auth token")
        payload = {"login": login}
        headers = {
            "Authorization": "Bearer {}".format(self.token["access_token"]),
            "Client-Id": self.client_id
        }
        try:
            res = requests.get(
                self.endpoints["users"]["url"], params=payload,
                headers=headers
            )
            if res.status_code == HTTPStatus.OK:
                self.data["users"] = {login: res.json()["data"][0]}
                return self.data["users"][login]
        except Exception as exc:
            raise Exception("Failed to obtain user(s)") from exc

    def fetch_follows(self, login, limit=100):
        if self.token_is_valid() is False:
            raise Exception("Must first obtain auth token")
        user_id = self.fetch_user(login)["id"]
        payload = {
            "from_id": f"{user_id}",
            "first": f"{limit}"  # return limit max
        }
        headers = {
            "Authorization": "Bearer {}".format(self.token["access_token"]),
            "Client-Id": self.client_id
        }
        try:
            res = requests.get(
                self.endpoints["follows"]["url"], params=payload,
                headers=headers
            )
            if res.status_code == HTTPStatus.OK:
                self.data["users"][login]["follows"] = res.json()["data"]
                return self.data["users"][login]["follows"]
        except Exception as exc:
            raise Exception("Failed to obtain follows") from exc

    def reduce_follows(self, login):
        if self.data["users"][login]["follows"] is None:
            return None
        if len(self.data["users"][login]["follows"]) < 1:
            return None
        follows = []
        for i in self.data["users"][login]["follows"]:
            follows.append(i["to_name"])
        return follows

    def write_ps1_files(self, login):
        TEMPLATE = open("./_twitch.ps1").read()
        follows = self.reduce_follows(login)
        follows.sort()
        for f in follows:
            path = f"./output/{f}.ps1"
            if file_exists(path) is True:
                continue
            with open(path, "x") as file:
                file.write(TEMPLATE)
                file.close()
        return follows
