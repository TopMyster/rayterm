import os
import sys
import asyncio
import datetime
import platform
import webbrowser
import python_weather
import random
from .config import *
from openrouter import OpenRouter
from prompt_toolkit import PromptSession
from prompt_toolkit import prompt as pt_prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion

chat_history = [
    {"role": "system", "content": "You are a helpful assistant for people using Rayterm you can help them navigate through it too . 'Commands:\n"
        "  /l   - lists all apps\n"
        "  /f   - open a favorite app by typing the number.\n"
        "  /b   - searches using browser\n"
        "  /ai  - ask AI a question\n"
        "  /calc - a simple calculator\n"
        "  clock - shows current date and time\n"
        "  weather - show current weather forecast\n"
        "  sys - shows your computers basic information\n"
        "  help - shows list of commands\n"
        "  dice - rolls a dice\n"
        "  rick - Try and find out what it does ;)\n"
        "  q    - quit rayterm get out of a / mode ex. getting out of /l mode\n"}
]

class AppCommandSuggest(AutoSuggest):
    def __init__(self, options):
        self.options = options
    def get_suggestion(self, buffer, document):
        text = document.text_before_cursor.strip()
        if not text: return None
        for opt in self.options:
            if opt.lower().startswith(text.lower()):
                return Suggestion(opt[len(text):])
        return None

def open_fav(index_str: str):
    if index_str != "q":
        try:
            index = int(index_str)
            launch_app(favs[index - 1])
        except IndexError:
            print('Number is out of range')
        except ValueError:
            print('Invalid input. Please enter in a number.')
    else:
        quit_rt()
    
def launch_app(name: str):
    #Opening a url in a browser
    if name.startswith(("http://", "https://", "www.")) or ("." in name and "/" not in name):
        url = name if name.startswith("http") else f"https://{name}"
        webbrowser.open(url)
        return

    #Opening an app with macOS
    if sys.platform == "darwin":
        os.system(f'open -a "{name}"')
    #Opening an app with Windows 
    elif sys.platform == "win32":
        os.system(f'start "" "{name}"')
    #Opening an app with Linux
    else:
        os.system(f'xdg-open "{name}"')

def list_apps():
    apps = []
    #Listing apps with macOS
    if sys.platform == "darwin":
        apps = [f for f in sorted(os.listdir("/Applications")) if f.endswith(".app")]
    elif sys.platform == "win32":
        paths = [
            os.path.join(os.environ.get('ProgramData', 'C:\\ProgramData'), 'Microsoft\\Windows\\Start Menu\\Programs'),
            os.path.join(os.environ.get('AppData', ''), 'Microsoft\\Windows\\Start Menu\\Programs')
        ]
        for p in paths:
            if os.path.exists(p):
                apps.extend([f for f in os.listdir(p) if f.endswith('.lnk')])
    else: 
        apps_path = f'{os.environ.get("HOME")}/.local/share/applications'
        if os.path.exists(apps_path):
            apps = [f for f in os.listdir(apps_path) if f.endswith('.desktop')]
    
    if apps:
        print("\n".join(sorted(apps)))
    else:
        print("No apps found on this platform.")

def ask_ai(txt):
    if txt == "q":
        quit_rt()
    else:
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
    if query == "q":
        quit_rt()
    else:
        launch_app(f"https://www.google.com/search?q={query}")

def calc(expression):
    if expression == "q":
        quit_rt()
    else:
        print(eval(expression))

async def weather():
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        result = await client.get(LOCATION)
        print(f"\nWeather for {LOCATION}:")
        print(f"Current Temperature: {result.temperature}°F ({result.description})")
        
        print("\nForecast:")
        for day in result.daily_forecasts:
            print(f"{day.date}: {day.temperature}°F")
        print("")

def sys_info():
    print(f"\nPlatform: {platform.system()}")
    print(f"Version: {platform.platform()}")
    print(f"Python Version: {platform.python_version()}")
    print(f"Architecture: {platform.machine()}\n")
    

def clock():
    print(datetime.datetime.now().strftime("%H:%M %p"))
    print(datetime.date.today().strftime("%m-%d-%Y"))

def roll_dice():
    print(random.randint(1, 6))

def rick_roll():
    launch_app("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

def help_rt():
    print(
        'Commands:\n'
        '  /l   - lists all apps\n'
        '  /f   - open a favorite app by number\n'
        '  /b   - searches browser\n'
        '  /ai  - ask AI a question\n'
        '  /calc - a simple calculator\n'
        '  clock - shows current date and time\n'
        '  weather - show current weather\n'
        '  dice - rolls a dice\n'
        '  sys - shows system information\n'
        '  help - shows list of commands\n'
        '  q    - quit rayterm\n'
        '  rick - Try and find out what it does ;)\n'
    )

def quit_rt():
    print("\nNow switching galaxies - Goodbye!")
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
    
    apps = []
    if sys.platform == 'darwin':
        apps = [f.replace('.app', '') for f in os.listdir('/Applications') if f.endswith('.app')]
    elif sys.platform == 'win32':
        paths = [
            os.path.join(os.environ.get('ProgramData', 'C:\\ProgramData'), 'Microsoft\\Windows\\Start Menu\\Programs'),
            os.path.join(os.environ.get('AppData', ''), 'Microsoft\\Windows\\Start Menu\\Programs')
        ]
        for p in paths:
            if os.path.exists(p):
                apps.extend([f.replace('.lnk', '') for f in os.listdir(p) if f.endswith('.lnk')])
    else: 
        apps_path = '/usr/share/applications'
        if os.path.exists(apps_path):
            apps = [f.replace('.desktop', '') for f in os.listdir(apps_path) if f.endswith('.desktop')]

    commands_list = ['/l', '/f', '/b', '/ai', '/calc', 'weather', 'clock', 'help', 'q', 'dice', 'rick']
    all_options = commands_list + apps
    completer = FuzzyCompleter(WordCompleter(all_options))
    session = PromptSession(
        completer=completer,
        auto_suggest=AppCommandSuggest(all_options),
        complete_while_typing=False
    )

    while True:
        try:
            main_prompt = HTML('<ansiblue><b>◆ rayterm</b></ansiblue> <ansiblue><b>❯</b></ansiblue> ')
            prompt_str = session.prompt(main_prompt).strip()
            cmd = prompt_str.strip()
            
            commands = {
                '/l': list_apps,
                '/f': lambda: open_fav(pt_prompt(HTML('<ansiblue><b>◆ rayterm</b></ansiblue><ansicyan><b>/fav</b></ansicyan> <ansiblue><b>❯</b></ansiblue> '))),
                '/b': lambda: search_browser(pt_prompt(HTML('<ansiblue><b>◆ rayterm</b></ansiblue><ansiyellow><b>/browser</b></ansiyellow> <ansiblue><b>❯</b></ansiblue> '))),
                '/ai': lambda: ask_ai(pt_prompt(HTML('<ansiblue><b>◆ rayterm</b></ansiblue><ansimagenta><b>/ai</b></ansimagenta> <ansiblue><b>❯</b></ansiblue> '))),
                '/calc': lambda: calc(pt_prompt(HTML('<ansiblue><b>◆ rayterm</b></ansiblue><ansired><b>/calc</b></ansired> <ansiblue><b>❯</b></ansiblue> '))),
                'weather': lambda: asyncio.run(weather()),
                'clock': clock,
                'sys': sys_info,
                'help': help_rt,
                'q': quit_rt,
                'dice': roll_dice,
                'rick': rick_roll
            }

            if cmd in commands:
                commands[cmd]()
            elif cmd:
                launch_app(cmd)
            else:
                print("Not a known command. Type 'help' for assistance.")
        except KeyboardInterrupt:
            print("\nNow switching galaxies - Goodbye!")