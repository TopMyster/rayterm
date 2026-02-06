import os
import sys

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
    elif prompt:
        launch_app(prompt)
    else:
        print("Not a known command.")

if __name__ == "__main__":
    rt()

