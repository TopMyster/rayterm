import os
import sys
import asyncio
import datetime
import platform
import webbrowser
import python_weather
import random
from openrouter import OpenRouter
from prompt_toolkit import PromptSession
from prompt_toolkit import prompt as pt_prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")

def is_first_run():
    return not os.path.exists(CONFIG_PATH)

def first_run_setup():
    print(
        "\n  ╔══════════════════════════════════════╗\n"
        "  ║   Welcome to Rayterm! Let's set up.  ║\n"
        "  ╚══════════════════════════════════════╝\n"
    )

    print("Set your favorite apps (comma-separated).")
    print("  Default: Spotify, Chrome, Discord")
    fav_input = input("  > ").strip()
    if fav_input:
        fav_list = [app.strip() for app in fav_input.split(",") if app.strip()]
    else:
        fav_list = ["Spotify", "Chrome", "Discord"]

    print("\nChoose a theme color (e.g. Blue, Green, Red, Cyan, Magenta, Yellow).")
    print("  Default: Blue")
    theme_input = input("  > ").strip()
    theme = theme_input if theme_input else "Blue"

    print("\nSet your location for weather (e.g. New York, London, Tokyo).")
    print("  Default: New York")
    loc_input = input("  > ").strip()
    location = loc_input if loc_input else "New York"

    print("\nEnter your OpenRouter API key.")
    print("  Default: sk-or-v1-your-key-here")
    key_input = input("  > ").strip()
    api_key = key_input if key_input else "sk-or-v1-your-key-here"

    with open(CONFIG_PATH, "w") as f:
        f.write(f"favs = {repr(fav_list)}\n")
        f.write(f"THEME = {repr(theme)}\n")
        f.write(f"LOCATION = {repr(location)}\n")
        f.write(f"API_KEY = {repr(api_key)}\n")

    print("\n  Setup complete! Launching Rayterm...\n")

def load_config():
    global favs, THEME, LOCATION, API_KEY
    config = {}
    with open(CONFIG_PATH, "r") as f:
        exec(f.read(), config)
    favs = config.get("favs", ["Spotify", "Chrome", "Discord"])
    THEME = config.get("THEME", "Blue").strip().lower()
    LOCATION = config.get("LOCATION", "New York")
    API_KEY = config.get("API_KEY", "sk-or-v1-your-key-here")

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
    if name.startswith(("http://", "https://", "www.")) or ("." in name and "/" not in name):
        url = name if name.startswith("http") else f"https://{name}"
        webbrowser.open(url)
        return

    if sys.platform == "darwin":
        os.system(f'open -a "{name}"')
    elif sys.platform == "win32":
        os.system(f'start "" "{name}"')
    else:
        os.system(f'xdg-open "{name}"')

def list_apps():
    apps = []
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
    try:
        async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
            result = await client.get(LOCATION)
            print(f"\nWeather for {LOCATION}:")
            print(f"Current Temperature: {result.temperature}°F ({result.description})")
            
            print("\nForecast:")
            for day in result.daily_forecasts:
                print(f"{day.date}: {day.temperature}°F")
            print("")
    except KeyError:
        print(f"\nCouldn't fetch weather for '{LOCATION}'. Try using just the city name (e.g. 'Houston' instead of 'Houston, Texas').")
    except Exception as e:
        print(f"\nWeather error: {e}")

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
    if is_first_run():
        first_run_setup()
    load_config()

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
            main_prompt = HTML(f'<ansi{THEME}><b>◆ rayterm</b></ansi{THEME}> <ansi{THEME}><b>❯</b></ansi{THEME}> ')
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
