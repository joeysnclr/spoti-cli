# Spotify Terminal Application

![Spoti-CLI Preview](https://raw.githubusercontent.com/joeysnclr/spoti-cli/master/screenshot.png)

### Intro

Spotify Terminal Application is a terminal client for Spotify. Designed with efficiency in mind, it uses quick keybindings for navigating and controlling your music.


Supports Mac & Linux

### Requirements

- Python3 and pip
- Spotify Premium
- [Spotify Developer Application](https://developer.spotify.com/dashboard/login)
    - client-id and client-secret are retrieved from your Spotify Developer Application

### Install & Usage

Clone repository
`git clone https://github.com/joeysnclr/spoti-cli.git`

Change directory to repo
`cd spoti-cli`

Install requirements
`pip3 install -r requirements.txt`

Add `http://127.0.0.1:5000/auth` as a Redirect URI for your Spotify developer Application

Run application & Input your **client-id** and **client-secret**
`python3 spoticli/__main__.py`

Press `?` for help.
