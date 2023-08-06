# Discord Helper
A simple helper library for discord.py

## Features

`getEmoteFromName(name)`
This gets the unicode emoji that corresponds to the discord emoji, like how `:grinning:` is "😀" in reactions.

`getNameFromEmote(emote)`
The exact opposite of `getEmoteFromName` as this takes in the emoji and gives back the name

`createEmbed(title, text, footer, authour_name, color)`
This returns a embed with the inputs given

`checkURLs(string)`
Returns a bool stating whether there is a url in the string

`getURLs(string)`
Returns a list of all URLs in a string

`getTimeSinceMessage(message)`
Returns DateTime of time since a message was created

`getColoredText(text, color)`
Responds with the formatting corresponding to the color, here are the following colors
- red
- green
- dark-green
- light-green
- orange
- yellow
- dark-yellow
- blue

## Version & Fixes

The code is in version 1.0.0
Please feel free to fork and make suggestions about this library

## How to install

Run setup.py
