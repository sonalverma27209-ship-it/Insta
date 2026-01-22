#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import time
import os
import requests
from getpass import getpass

# ================= PASSWORD LOCK =================
PASSWORD = "8252"

def password_lock():
    pin = getpass("Enter Tool Password : ")
    if pin != PASSWORD:
        print("\n[!] Access Denied")
        sys.exit(1)

# ================= PARROT ASCII =================
def print_parrot():
    print(" _______________ ")
    print(" \033[07m  Insta.py!  \033[27m           # \033[07mC\033[27mommon")
    print("      \\                    # \033[07mU\033[27mser")
    print("       \\   \033[1;31m,__,\033[1;m            # \033[07mP\033[27massword")
    print("        \\  \033[1;31m(\033[1;moo\033[1;31m)____\033[1;m         # \033[07mP\033[27mrofile")
    print("           \033[1;31m(__)    )\\ \033[1;m")
    print("           \033[1;31m   ||--|| \033[1;m\033[05m* \033[25m\033[1;m")
    print("                           [ Made by Shivanshi ]\r\n")

def version():
    __version__ = "1.0"
    print("\r\n \033[1;31m[ Insta.py ]  " + __version__ + "\033[1;m\r\n")
    print(" * Created by Shivanshi")
    print(" * Educational & OSINT Purpose Only")
    print(" * Read README.md for usage\r\n")

# ================= LOADING =================
def animated_loading():
    steps = [
        "[+] Initializing Insta.py",
        "[+] Loading modules",
        "[+] Preparing OSINT engine",
        "[+] Ready"
    ]
    for step in steps:
        print(step)
        time.sleep(0.5)
    print()

# ================= FEATURE FUNCTIONS =================
def check_username(username):
    url = f"https://www.instagram.com/{username}/"
    try:
        r = requests.get(url, timeout=5)
        return r.status_code == 200
    except:
        return False

def download_profile_pic(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code != 200 or 'og:image' not in r.text:
            return "Not Available"
        start = r.text.find('property="og:image" content="') + 34
        end = r.text.find('"', start)
        img_url = r.text[start:end]
        os.makedirs("profile_pics", exist_ok=True)
        img_data = requests.get(img_url).content
        path = f"profile_pics/{username}.jpg"
        with open(path, "wb") as f:
            f.write(img_data)
        return path
    except:
        return "Not Available"

def fetch_public_info(username):
    exists = check_username(username)
    data = {
        "Username": username,
        "Exists": "Yes" if exists else "No",
        "Profile Picture": "Not Downloaded"
    }
    if exists:
        pic = download_profile_pic(username)
        data["Profile Picture"] = pic
    return data

def save_to_file(username, data):
    os.makedirs("results", exist_ok=True)
    path = f"results/{username}.txt"
    with open(path, "w") as f:
        for k, v in data.items():
            f.write(f"{k} : {v}\n")
    print(f"\n[+] Results saved to {path}")

# ================= INTERACTIVE MODE =================
def interactive_mode(write=False):
    print("[+] Interactive Mode Enabled\n")
    username = input("Enter Instagram Username : ").strip()
    if not username:
        print("\nFailed to fetch data")
        print("Reason: Username invalid / empty")
        return
    print("\n[+] Checking username")
    time.sleep(1)
    data = fetch_public_info(username)
    print()
    for k, v in data.items():
        print(f"{k:18}: {v}")
    if write:
        save_to_file(username, data)

# ================= ARGPARSE =================
def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-i", "--interactive", action="store_true")
    parser.add_argument("-w", "--write", action="store_true")
    parser.add_argument("-v", "--version", action="store_true")

    args = parser.parse_args()

    if args.help or len(sys.argv) == 1:
        print_parrot()
        version()
        print("Usage:")
        print("  python3 Insta.py [options]\n")
        print("Options:")
        print("  -h, --help            Show this help")
        print("  -i, --interactive     Interactive mode")
        print("  -w, --write           Save results to TXT file")
        print("  -v, --version         Show version info\n")
        print("Examples:")
        print("  python3 Insta.py -i")
        print("  python3 Insta.py -i -w")
        return

    if args.version:
        version()
        return

    password_lock()
    print_parrot()
    animated_loading()

    if args.interactive:
        interactive_mode(write=args.write)
    else:
        print("Failed to fetch data")
        print("Reason: No mode selected (use -i)")

# ================= ENTRY =================
if __name__ == "__main__":
    main()
