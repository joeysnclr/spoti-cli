# Spoti-CLI


![Spoti-CLI Preview](https://raw.githubusercontent.com/joeysnclr/terminal-spotify/master/screenshot.png)

### Intro

Spoti-CLI (subject to name change) is a command line TUI (terminal user interface)
client for Spotify. Designed with efficiency in mind, Terminal Spotify uses Vim
based keybindings for navigating and controlling the application.

### Requirements

- python3 & pip
- Spotify Premium
- Spotify Developer Application

### Install & Usage

`pip3 install spoti-cli`

`spoticli`

### Shortcuts

##### Navigation

- h: back to previous menu (not implemented)
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

### To Do

##### Necesarry

- add package to package repos (homebrew, apt, etc...)

##### Useful Functionality

- responsive lines
- add setting; reset cache on startup
- menu searching with / (esc to exit search mode)
- artist menu
- album menu
- podcast listening functionality

##### Nice To Have

- add lyrics caching (permanent)
- Spotify search
- audio visualizer
- change Spotify device
- player view only mode
- minimal ui mode [here](https://i.redd.it/mnerempmqwm51.png)
- centered lyrics/help menu

### Known Bugs

- linux, can't play song in context


### Contributing

Feel free to contribute any ideas or code to this project. Anything is welcomed!

If you come across any issues please report them in the issues tab. Thank you!
