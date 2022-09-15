# Twitch API play

Fetches list of followed twitch streamers from [Twitch API](https://dev.twitch.tv/docs/api/). Writes PowerShell scripts to disk which when run, opens the respective live stream natively via [Streamlink](https://streamlink.github.io/).

## Dependencies

1. Windows
2. PowerShell
3. Python 3
4. Streamlink
5. a decent video player

## Instructions

Run in PowerShell.

1. copy file **.env_template** to **.env**
2. populate **.env** with your [twitch api app credentials](https://dev.twitch.tv/console)
3. `python -m venv venv`
4. `./venv/Scripts/Activate.ps1`
5. `python -m pip install -r requirements.txt`
6. `python -m flask --app app run --port=80`
7. http://localhost