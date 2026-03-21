import os
import sys
import webbrowser
from .config import *
from openrouter import OpenRouter

chat_history = []

def open_fav(index: int):
    try:
        launch_app(favs[index - 1])
    except IndexError:
        print('Number is out of range')
    
def launch_app(name: str):
    if name.startswith(("http://", "https://", "www.")) or ("." in name and "/" not in name):
        url = name if name.startswith("http") else f"https://{name}"
        webbrowser.open(url)
        return

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
        print("Listing all apps is only supported on macOS rayterm.")

def ask_ai(txt):
    chat_history.append({"role": "user", "content": txt})
    with OpenRouter(
        api_key=API_KEY
    ) as client:
        response = client.chat.send(
            model="openai/gpt-oss-20b",
            messages=chat_history,
            temperature=0.7
        )

        print('...\n')

        ai_msg = response.choices[0].message
        print(f"AI: {ai_msg.content}")
        chat_history.append({"role": "assistant", "content": ai_msg.content})

def search_browser(query):
    launch_app(f"https://www.google.com/search?q={query}")


def help_rt():
    print(
        'Commands:\n'
        '  /a   - lists all apps (only available on macOS)\n'
        '  /f   - open a favorite app by number\n'
        '  /b   - searches browser\n'
        '  ai   - ask AI something\n'
        '  help - show list of commands\n'
        '  q    - quit rayterm\n'
    )

def quit_rt():
    print("\n Exiting rayterm. Goodbye!")
    sys.exit(0)

def rt():
    print(
        "    ╔═══╗           ╔╗                \n"
        "    ║╔═╗║          ╔╝╚╗               \n"
        "    ║╚═╝║╔══╗ ╔╗ ╔╗╚╗╔╝╔══╗╔═╗╔╗╔╗    \n"
        "    ║╔╗╔╝╚ ╗║ ║║ ║║ ║║ ║╔╗║║╔╝║╚╝║    \n"
        "    ║║║╚╗║╚╝╚╗║╚═╝║ ║╚╗║║═╣║║ ║║║║    \n"
        "    ╚╝╚═╝╚═══╝╚═╗╔╝ ╚═╝╚══╝╚╝ ╚╩╩╝    \n"
        "              ╔═╝║                    \n"
        "              ╚══╝                    \n\n"
    )
    while True:
        try:
            prompt = input(
                "rayterm > "
            ).strip()

            cmd = prompt.strip()
            
            commands = {
                '/a': list_apps,
                '/f': lambda: open_fav(int(input('rayterm/fav > '))),
                '/b': lambda: search_browser(input('rayterm/browser > ')),
                'ai': lambda: ask_ai(input('rayterm/ai > ')),
                'help': help_rt,
                'q': quit_rt
            }

            if cmd in commands:
                commands[cmd]()
            elif cmd:
                launch_app(cmd)
            else:
                print("Not a known command. Type 'help' for assistance.")
        except KeyboardInterrupt:
            print("\n Exiting rayterm. Goodbye!")