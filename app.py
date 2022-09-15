import os
from flask import Flask, request, render_template
from dotenv import load_dotenv
from twitch_api import TwitchApi

load_dotenv()
app = Flask(__name__, template_folder="templates")
LOGIN = "anarchicuk"

twitch = TwitchApi(**{
    "client_id": os.environ["CLIENT_ID"],
    "client_secret": os.environ["CLIENT_SECRET"],
    "redirect_uri": os.environ["REDIRECT_URL"],
    "scope": ["user:read:follows"],
    "grant_type": "client_credentials"
})


@app.route("/", methods=["GET"])
def index():
    auth_url = twitch.auth_link
    return render_template("index.jinja2", auth_url=auth_url)


@app.route("/auth", methods=["GET"])
def auth():
    if twitch.token_is_valid() is True:
        return twitch.token
    if twitch.twitchAuthResponseIsValid(request.args):
        twitch.fetch_auth_token(request.args["code"])
        return twitch.token
    return "Error: Twitch oauth2 response invalid"


@app.route("/user", methods=["GET"])
def user():
    if twitch.token_is_valid() is True:
        return twitch.fetch_user(LOGIN)
    return "no auth token in memory"


@app.route("/follows", methods=["GET"])
def follows():
    if twitch.token_is_valid() is True:
        res = twitch.fetch_follows(LOGIN)
        if res:
            return res
        return "error contacting api, login: {}".format(LOGIN)
    return "no auth token in memory"


@app.route("/write", methods=["GET"])
def write():
    if twitch.token_is_valid() is True:
        return twitch.write_ps1_files(LOGIN)
    return "no auth token in memory"
