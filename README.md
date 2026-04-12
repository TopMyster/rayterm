# Rayterm 
#### Raycast for the terminal



https://github.com/user-attachments/assets/4d5fd884-e656-47e2-9e1b-5abd7f80470f



## Installation/Configuration

First, clone the repository
```
git clone https://github.com/TopMyster/rayterm/tree/main
```

Edit the configurations in config.py Ex:
```
# Config

#Favorite Apps
favs = [
    'Spotify', 
    'Chrome', 
    'Discord'
    ]

#Openrouter API Key
API_KEY = 'sk-or-v1-...' # Your API KEY
```

To install, while in project location run:

```bash
pip3 install -e .
```

Once installation is complete, use the rayterm with:

```bash
rt
```

## Commands
Enter the index of your favorite apps to open them quickly
```
fav
```

Shows all apps on your computer (MacOS Only)
```
apps
```

Ask AI anything
```
ai
```

Search the web
```
/b
```

Shows list of commands
```
help
```
Exits rayterm
```
q
```





