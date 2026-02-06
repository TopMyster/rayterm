import os
import sys
favs = ['Spotify', 'Chrome', 'Discord'] #Configure your favorite apps

def open_fav(index: int):
    try:
        launch_app(favs[index-1])
    except:
        print('Number is out of range')
    
def launch_app(name: str):
    if sys.platform == "darwin":
        os.system(f'open -a "{name}"')
    elif os.name == "nt":
        os.system(f'start "" "{name}"')
    else:
        os.system(f'xdg-open "{name}"')

def list_apps():
    if sys.platform == "darwin":
        apps = [f for f in sorted(os.listdir("/Applications")) if f.endswith(".app")]
        print("\n".join(apps))
    else:
        print("Listing all apps is only supported on macOS in this rayterm.")

def rt():
    prompt = input(
        "    ╔═══╗           ╔╗                \n"
        "    ║╔═╗║          ╔╝╚╗               \n"
        "    ║╚═╝║╔══╗ ╔╗ ╔╗╚╗╔╝╔══╗╔═╗╔╗╔╗    \n"
        "    ║╔╗╔╝╚ ╗║ ║║ ║║ ║║ ║╔╗║║╔╝║╚╝║    \n"
        "    ║║║╚╗║╚╝╚╗║╚═╝║ ║╚╗║║═╣║║ ║║║║    \n"
        "    ╚╝╚═╝╚═══╝╚═╗╔╝ ╚═╝╚══╝╚╝ ╚╩╩╝    \n"
        "              ╔═╝║                    \n"
        "              ╚══╝                    \n\n"
        "rayterm > "
    ).strip()

    if prompt.lower() == "all":
        list_apps()
    elif prompt.lower() == "fav":
        open_fav(int(input('rayterm/fav > ')))
    elif prompt:
        launch_app(prompt)
    else:
        print("Not a known command.")

if __name__ == "__main__":
    rt()

