# Game-Score
A simple Discord bot to keep track of scores for board games

# Installation
* Requires [Python 3.8+](https://www.python.org/)
* Requires [Discord.py](https://discordpy.readthedocs.io/en/stable/)

To install Discord.py:
 ```console
 python3 -m pip install discord.py
 ```
 This Bot also requires your discord bot token. Place that token in token.token
 
 # Running
 
 To run this bot after you have installed all the dependancies, run: 
 ```console
 python score.py
 ```
 # Usage
  
 The current commands that this uses are
 ```
 !ping
 ```
 This is just to test if the bot is running.
 ```
 !score {game_name} {(player_name) (player_score)}*
 ```
 ###### Note, that the player_name and score section is repeated for all the players in the game
 Once you have followed the instructions given by the discord bot, it saves that in the file ```allGames.csv```
 
 ```
 !file
 ```
 This returns the file that contains all scores. This file can then be used in a program like [Google Sheets](https://docs.google.com/spreadsheets) to turn it into a spreadsheet

```
!last {game_name}
```
This Returns the date of the last time the given game was played
