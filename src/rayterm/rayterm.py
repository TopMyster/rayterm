import os
import sys

favs = ['Spotify', 'Chrome', 'Discord']


def open_fav(index: int):
    if 1 <= index <= len(favs):
        launch_app(favs[index - 1])
    else:
        print('Number is out of range')


def launch_app(name: str):
    if sys.platform == "darwin":
        os.system(f'open -a "{name}"')
    elif os.name == "nt":
        os.system(f'start "" "{name}"')
    else:
        os.system(name)


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

    cmd = prompt.lower()

    if cmd == "all":
        list_apps()
    elif cmd == "x":
        return
    elif cmd == "fav":
        try:
            index = int(input('rayterm/fav (number) > '))
            open_fav(index)
        except ValueError:
            print("Please enter a number.")
    elif cmd == "exit":
        sys.exit(0)
    elif cmd == "help":
        print(
            "Rayterm commands:\n"
            "  help  - show this message\n"
            "  fav   - open one of your favorite apps by number\n"
            "  all   - list installed apps (macOS only)\n"
            "  exit  - quit rayterm\n"
            "  x     - go back / close this session\n"
            "\n"
            "You can also type an app name directly to launch it."
        )
    elif prompt:
        launch_app(prompt)
    else:
        print("Not a known command. Type 'help' for assistance")

    rt()


if __name__ == "__main__":
    rt()

