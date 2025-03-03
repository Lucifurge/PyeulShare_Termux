import requests
import hashlib
import uuid
import random
import string
import time
import threading
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

banner = Panel(
    "[bold yellow]PYEUL SPAMSHARE & TOKEN GENERATOR[/bold yellow]", 
    width=60, 
    title="[bold cyan]Auto Comment Bot[/bold cyan]", 
    border_style="blue",
    expand=False
)
console.print(banner)

def random_string(length):
    characters = string.ascii_lowercase + "0123456789"
    return ''.join(random.choice(characters) for _ in range(length))

def encode_sig(data):
    sorted_data = {k: data[k] for k in sorted(data)}
    data_str = ''.join(f"{key}={value}" for key, value in sorted_data.items())
    return hashlib.md5((data_str + '62f8ce9f74b12f84c123cc23437a4a32').encode()).hexdigest()

def generate_token(email, password):
    device_id = str(uuid.uuid4())
    adid = str(uuid.uuid4())
    random_str = random_string(24)

    form = {
        'adid': adid,
        'email': email,
        'password': password,
        'format': 'json',
        'device_id': device_id,
        'cpl': 'true',
        'family_device_id': device_id,
        'locale': 'en_US',
        'client_country_code': 'US',
        'credentials_type': 'device_based_login_password',
        'generate_session_cookies': '1',
        'generate_analytics_claim': '1',
        'generate_machine_id': '1',
        'source': 'login',
        'machine_id': random_str,
        'api_key': '882a8490361da98702bf97a021ddc14d',
        'access_token': '350685531728%7C62f8ce9f74b12f84c123cc23437a4a32',
    }

    form['sig'] = encode_sig(form)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    url = 'https://b-graph.facebook.com/auth/login'
    try:
        response = requests.post(url, data=form, headers=headers, timeout=10)
        data = response.json()
        if 'access_token' in data:
            return data['access_token']
        else:
            console.print(f"[red]Token generation failed: {data}")
            return None
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Request Error: {e}")
        return None

def share_post(cookie, share_url, share_count):
    url = "https://graph.facebook.com/me/feed"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Authorization": f"Bearer {cookie}"
    }
    data = {
        "link": share_url,
        "privacy": '{"value":"SELF"}',
        "no_story": "true",
        "published": "false"
    }
    for i in range(1, share_count * 2 + 1):
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            response_data = response.json()
            if "id" in response_data:
                console.print(f"[bold cyan]({i}/{share_count * 2})[/bold cyan] [green]Post shared successfully!")
            else:
                console.print(f"[red]({i}/{share_count * 2}) Failed: {response_data}")
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Failed: {e}")
        time.sleep(0.1)

def spam_share_single():
    token = input("Enter your Facebook access token: ").strip()
    if not token:
        console.print("[red]Invalid token!")
        return
    share_url = input("Enter your post link: ").strip()
    try:
        share_count = int(input("Enter Share Count: ").strip())
        share_post(token, share_url, share_count)
    except ValueError:
        console.print("[red]Invalid number format!")

def spam_share_multiple():
    tokens = input("Paste your tokens (comma separated): ").strip().split(',')
    share_url = input("Enter your post link: ").strip()
    try:
        share_count = int(input("Enter Share Count per account: ").strip())
    except ValueError:
        console.print("[red]Invalid number format!")
        return

    threads = []
    for token in tokens:
        thread = threading.Thread(target=share_post, args=(token.strip(), share_url, share_count))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def main_menu():
    while True:
        console.print(Panel("""
[1] Generate Token
[2] Multi-Cookie Spam Share
[3] Single Token Share
[4] Exit
""", width=60, style="bold bright_white"))
        choice = input("Select an option: ").strip()
        if choice == "1":
            email = input("Enter your email: ").strip()
            password = input("Enter your password: ").strip()
            token = generate_token(email, password)
            if token:
                console.print(f"\n[+] Generated Token: {token}\n")
            else:
                console.print("[red]Token generation failed!")
        elif choice == "2":
            spam_share_multiple()
        elif choice == "3":
            spam_share_single()
        elif choice == "4":
            console.print("[red]Exiting... Goodbye!")
            break
        else:
            console.print("[red]Invalid choice!")

if __name__ == '__main__':
    main_menu()
