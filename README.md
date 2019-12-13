# Stream music announcer

**This project is abandoned in favor of [song-announcer2](https://github.com/paskausks/song-announcer2)!**

An animated HTML widget for displaying the currently playing song targeted towards streamers, like yours truly.
Shows song title, artist name, album name and album art, provided by the Spotify Web API.

![Stream song announcer](https://thumbs.gfycat.com/GrotesqueFairKodiakbear-size_restricted.gif "Stream song announcer")

[Higher resolution](https://gfycat.com/GrotesqueFairKodiakbear)

Started as a single HTML file way back, but was forced to grow a bit bigger recently due to the mandatory authentication for applications which want to search the Spotify library.


## Requirements
* Python 2.7+
* A standalone program which writes the currently playing song performer and title to a text file. I personally recommend [SMG music display](https://martijnbrekelmans.com/SMG/), since it supports a wide variety of services, like, YouTube, Spotify, SoundCloud etc. The only downside is that it's not freeware.
* A streaming program which supports displaying HTML content with CSS animations, like [OBS Studio](https://obsproject.com/).

##  Setup
1) Make sure Python 2 is installed. If you're on GNU/Linux, it almost definitely was bundled with your distribution.
2) Go to https://developer.spotify.com, login with your Spotify account (or register if you don't have one, it's free), go to _My Apps_, and proceed to the beta version of the site, by clicking _Check It Out_. Once there, create an application with whatever name and description you like. Note the Client ID and the Client Secret (by clicking _Show Client Secret_).
3) Open *config.ini.example* and replace __YourApplicationClientIdHere__ with the Client ID of your application and the __YourApplicationClientSecretHere__ with the Client Secret of the application you created. Also, remember to set _songfile_ in the bottom of the example file to the path to the text file which contains the currently playing song as well. For SMG it might be _C:\SMG\current_song.txt_ , while, for instance, the Streamlabs Chatbot hides it in _C:\Users\yourUserName\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Twitch\Files\CurrentlyPlaying.txt_. Save the edited file as __config.ini__.
4) Make sure the program responsible for updating your current song text file is running. Open a terminal window, navigate to the folder where you downloaded the announcer files and just type `app.py` (or `python2 app.py` if you're on Linux) and press Enter. If everything was done correctly, you'll see the server start up. Now we're rolling.
5) Launch your streaming program. I'll use OBS Studio as an example. Right-click in the _Sources_ section of your scene and go to _Add > BrowserSource_. Give it a name, like "Song announcer" and press OK. In the _URL_ field enter __http://localhost:15987/__. For the _Width_, I recommend it to put it to the full horizontal resolution of your scene, for example __1920__, if you have a full HD monitor, and __200__ for the _Height_. You can leave the rest at their default values, and press OK. If everything was done correctly, your currently playing song should already be shown, as will the ones after it (if you have music playing currently, that is). You can position it anywhere you want, but I recommend selecting the source and pressing ctrl+D, which will center it in the scene. We're all done.

## Something to do when bored
* Make it run on Python 3
* Rewrite that ancient, ugly front-end
* Add more customisation options, controlled via GUI, to make setup easier.
* Since, Windows doesn't come installed with python, create a redistributable package
