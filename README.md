# Terminal Spotify

### Intro

![Terminal Spotify Preview](https://raw.githubusercontent.com/joeysnclr/terminal-spotify/master/playlists_screenshot.png)

Terminal Spotify (subject to name change) is a TUI (terminal user interface)
client for Spotify. Designed with efficiency in mind, Terminal Spotify uses Vim
based keybindings for navigating and controlling the application.

### Requirements

- python3 & pip
- Spotify Premium
- Spotify Developer Application

### Installation From Source

clone the repository to any directory ($DIR)

`git clone https://github.com/joeysnclr/terminal-spotify.git $DIR`


add directory to path (in .bashrc or .zshrc)

`export PATH=$PATH:$DIR`


make `clify` file executable

`chmod +x $DIR/clify`


cd into $DIR and install requirements

`cd $DIR`

`pip3 install -r requirements.txt`



### Uninstall Source and Config/Cache Files

`rm -rf $DIR`
`rm ~./terminal-spotify.json`
`rm ~./terminal-spotify-cache.json` (this should be changed)

### Shortcuts

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
- /: enter search input (esc to leave search mode)


##### Music Player

- space: play/pause
- H: previous song
- L: next song
- s: toggle shuffle
- r: toggle repeat


##### Lyrics

- i: fetch lyrics from Genius


##### Development

- C: clear cache

### Known Bugs

- delay when exiting search mode

### Features/To Do

##### To Do List

- move cache file
- document architecture
- change name
- add package to package repos (homebrew, apt, etc...)


##### Completed features

- playlist menu
- song menu
- Spotify controls (minimum functionality)
- menu navigation controls (minimum functionality)
- snazzy lookin menu bar with some nice scroll effects on too long text
- menu searching with / (esc to exit search mode)
- Linux compatibility
- show song lyrics (Genius API)
- add some color to menubar

##### In Progress Features

- None currently

##### Future Features

- Spotify search
- artist menu
- album menu
- audio visualizer


### Contributing

Feel free to contribute any ideas or code to this project. Anything is welcomed!

If you come across any issues please report them in the issues tab. Thank you!
