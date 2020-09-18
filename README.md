# Terminal Spotify


![Terminal Spotify Preview](https://raw.githubusercontent.com/joeysnclr/terminal-spotify/master/screenshot.png)

### Intro

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

`rm -rf ~/.config/terminal-spotify`

`rm -rf ~/.cache/terminal-spotify` (this should be changed)


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


##### Development

- C: clear cache
- D: toggle logging display

### To Do

##### Completed

- playlist menu
- song menu
- Spotify controls (minimum functionality)
- menu navigation controls (minimum functionality)
- snazzy lookin menu bar with some nice scroll effects on too long text
- Linux compatibility
- add some color to menubar
- added logging output
- show song lyrics (Genius API)
- add songs to queue
- add main menu
- organize config/cache files [ XDG ](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)

##### In Progress

- keyboard shortcut config

##### Future

- incorporate update function to Component (keep output function strictly to getting the output)
- response menu item output
- add lyrics caching (permanent)
- menu searching with / (esc to exit search mode)
- continue adding logging, create a toggle shortcut
- document architecture
- change name
- add package to package repos (homebrew, apt, etc...)
- Spotify search
- artist menu
- album menu
- audio visualizer
- help menu
- podcast listening functionality
- change Spotify device
- player view only mode
- minimal ui mode [here](https://i.redd.it/mnerempmqwm51.png)


### Contributing

Feel free to contribute any ideas or code to this project. Anything is welcomed!

If you come across any issues please report them in the issues tab. Thank you!
