# discord-bot
A friendly bot that talks to you on Discord and listens to your commands

#### Functionalities-
1. The bot replies to a "Hi" with a "Hey"
2. The bot will search for the user provided query on Google and return top 5 links for the same.
For example, if you want the bot to search for "real madrid", issue the command - 

`!google real madrid`

3. The bot will maintain a cache of the user's search history.
4. If we query for a word in the search history, the bot will return the previosuly searched terms which match the word
Usage -

`!recent madrid` # This will return "real madrid" as it was searched earlier and was stored in the user's history

#### Pre-requisites-
`redis-server and redis-cli`
`supervisord` (To ensure that the process running the bot is highly available)


#### Usage-

`python bot.py`