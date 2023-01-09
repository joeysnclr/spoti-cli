# Spotify Terminal Application

![Spoti-CLI Preview](https://github.com/joeysnclr/spoti-cli/blob/dev/screenshot.png?raw=true)

### Intro

Spotify Terminal Application is a terminal client for Spotify. Designed with efficiency in mind, it uses quick keybindings for navigating and controlling your music.

### Requirements

- python3 & pip or from source
- Spotify Premium
- Spotify Developer Application
- client-id and client-secret are retrieved from your Spotify Developer Application

### Install & Usage

##### Pip

`pip3 install spoti-cli`

`spoticli`

###### Source

`git clone https://github.com/joeysnclr/spoti-cli.git`
`cd spoti-cli`
`pip3 install -r requirements.txt`
`python3 spoticli/__main__.py`


### Shortcuts 
`(~/.config/spoti-cli/shortcuts.json)`

##### Navigation

- h: back to previous menu
- j: down 1 menu item
- k: up 1 menu item
- l: select menu item
- enter: select menu item
- n: next page
- N: previous page
- g: go to first item on page
- G: go to last item on page

##### Music Player

- space: play/pause
- H: previous song
- L: next song
- s: toggle shuffle
- r: toggle repeat
- i: show lyrics

##### Development/Utils

- ?: help menu
- C: clear cache
- D: toggle logging display

