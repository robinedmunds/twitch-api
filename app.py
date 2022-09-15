import os
from flask import Flask, request
from dotenv import load_dotenv
from twitch_api import TwitchApi

load_dotenv()
app = Flask(__name__)

twitch = TwitchApi(**{
    "client_id": os.environ["CLIENT_ID"],
    "client_secret": os.environ["CLIENT_SECRET"],
    "redirect_uri": os.environ["REDIRECT_URL"],
    "scope": ["user:read:follows"],
    "grant_type": "client_credentials"
})


@app.route("/", methods=["GET"])
def index():
    if twitch.token:
        return twitch.token
    if twitch.twitchAuthResponseIsValid(request.args):
        twitch.fetch_auth_token(request.args["code"])
        return twitch.token
    auth_url = twitch.auth_link
    return f"<a href={auth_url}>twitch auth link</a>"


@app.route("/user", methods=["GET"])
def user():
    login = "anarchicuk"
    if twitch.token:
        return twitch.fetch_user(login)
    return "no auth token in memory"


@app.route("/followed", methods=["GET"])
def followed():
    login = "anarchicuk"
    if twitch.token:
        res = twitch.fetch_followed(login)
        if res:
            return res
        return "error contacting api, login: {}".format(login)
    return "no auth token in memory"