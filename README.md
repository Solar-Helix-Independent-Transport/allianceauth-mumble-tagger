# Mumble Tagger

This is a simple plugin for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth) to append a "Tag" too the end of a display name on mumble depending on a users group association.

## Setup

1. `pip install allianceauth-mumble-tagger`
2. add `'mumbletagger',` to INSTALLED_APPS in your local.py
3. migrate database and restart auth
4. Setup your tags in the admin panel
5. job done.


## Pics 

### Admin Setup Demo

![Imgur](https://i.imgur.com/ivihrLX.png)

### User in Mumble

![Imgur](https://i.imgur.com/QJ6b4ws.png)

## Contribute

All contributions are welcome, but please if you create a PR for functionality or bugfix, do not mix in unrelated formatting changes along with it.
