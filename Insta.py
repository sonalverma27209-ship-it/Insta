#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Insta.py - Instagram Public Profile OSINT Tool
Created by Shivanshi
Safe, educational tool for public data only
"""

import argparse
import sys
import time
import os
import requests
import re
from getpass import getpass

# ================= GLOBAL VARIABLES =================
PASSWORD = "8252"
PROFILE_PIC_DIR = "profile_pics"
RESULTS_DIR = "results"

# ================= UTILITIES =================
def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")

def animated_loading(steps=None, delay=0.5):
    if steps is None:
        steps = [
            "[+] Initializing Insta.py",
            "[+] Loading modules",
            "[+] Preparing OSINT engine",
            "[+] Ready"
        ]
    for step in steps:
        print(step)
        time.sleep(delay)
    print()

# ================= PASSWORD LOCK =================
def password_lock():
    attempts = 3
    while attempts > 0:
        pin = getpass("Enter Tool Password : ")
        if pin == PASSWORD:
            print("\n[+] Access Granted\n")
            return True
        else:
            attempts -= 1
            print(f"[!] Wrong PIN! {attempts} attempts left")
    print("\n[!] Access Denied")
    sys.exit(1)

# ================= PARROT ASCII =================
def print_parrot():
    print(" _______________ ")
    print(" \033[07m  Insta.py!  \033[27m           # \033[07mC\033[27I")
    print("      \\                    # \033[07mU\033[27n")
    print("       \\   \033[1;31m,__,\033[1;m            # \033[07mP\033[27s")
    print("        \\  \033[1;31m(\033[1;moo\033[1;31m)____\033[1;m         # \033[07mP\033[27t")
    print("           \033[1;31m(__)    )\\ \033[1;m")
    print("           \033[1;31m   ||--|| \033[1;m\033[05m* \033[25m\033[1;m")
    print("                           [ Made by Shivanshi ]\r\n")

# ================= VERSION =================
def version():
    print("\n\033[1;31m[ Insta.py ]  v1.0\033[1;m")
    print(" Created by Shivanshi")
    print(" Public OSINT Tool (Educational Only)\n")

# ================= FETCH PROFILE =================
def fetch_profile(username):
    """Fetch public profile info safely."""
    url = f"https://www.instagram.com/{username}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    data = {
        "Username": username,
        "Full Name": "Not Available",
        "Followers": "Not Available",
        "Following": "Not Available",
        "Posts": "Not Available",
        "Bio": "Not Available",
        "Profile Picture": "Not Downloaded"
    }
    try:
        r = requests.get(url, headers=headers, timeout=6)
        if r.status_code != 200:
            return data
        html = r.text

        # Full Name
        name = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        if name:
            data["Full Name"] = name.group(1).replace(" • Instagram photos and videos", "")

        # Followers / Following / Posts
        desc = re.search(r'<meta property="og:description" content="([^"]+)"', html)
        if desc:
            text = desc.group(1)
            nums = re.findall(r'([\d,.]+)\sFollowers,\s([\d,.]+)\sFollowing,\s([\d,.]+)\sPosts', text)
            if nums:
                data["Followers"], data["Following"], data["Posts"] = nums[0]

        # Bio
        bio = re.search(r'"biography":"(.*?)"', html)
        if bio:
            data["Bio"] = bio.group(1).encode().decode("unicode_escape")

        # Profile Picture
        img = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if img:
            os.makedirs(PROFILE_PIC_DIR, exist_ok=True)
            img_data = requests.get(img.group(1)).content
            img_path = f"{PROFILE_PIC_DIR}/{username}.jpg"
            with open(img_path, "wb") as f:
                f.write(img_data)
            data["Profile Picture"] = img_path

    except Exception as e:
        print(f"[!] Error fetching profile: {e}")

    return data

# ================= SAVE RESULTS =================
def save_results(username, data):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = f"{RESULTS_DIR}/{username}.txt"
    with open(path, "w") as f:
        for k, v in data.items():
            f.write(f"{k} : {v}\n")
    print(f"\n[+] Results saved to {path}")

# ================= INTERACTIVE MENU =================
def interactive(write=False):
    clear_screen()
    print_parrot()
    print("Welcome to Interactive Mode.\n")
    while True:
        username = input("Enter Instagram Username (or 'exit' to quit): ").strip()
        if username.lower() == "exit":
            print("\n[+] Exiting Interactive Mode...")
            break
        if not username:
            print("[!] Invalid username. Try again.\n")
            continue
        print("\n[+] Fetching profile...\n")
        animated_loading(["[+] Connecting...", "[+] Fetching data...", "[+] Analyzing...", "[+] Done"], 0.3)
        data = fetch_profile(username)
        print()
        for k, v in data.items():
            print(f"{k:15}: {v}")
        if write:
            save_results(username, data)
        print("\n-----------------------------------------\n")

# ================= MAIN =================
def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--help", action="store_true", help="Show help")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("-w", "--write", action="store_true", help="Save results to TXT")
    parser.add_argument("-v", "--version", action="store_true", help="Show version info")
    args = parser.parse_args()

    if args.help or len(sys.argv) == 1:
        print_parrot()
        version()
        print("Usage: python3 Insta.py [options]\n")
        print("Options:")
        print(" -h  Show help")
        print(" -i  Interactive mode")
        print(" -w  Save results to TXT")
        print(" -v  Show version\n")
        print("Example:")
        print(" python3 Insta.py -i")
        print(" python3 Insta.py -i -w")
        return

    if args.version:
        version()
        return

    password_lock()
    print_parrot()
    animated_loading(["[+] Starting interactive menu...", "[+] Ready!"], 0.4)

    if args.interactive:
        interactive(write=args.write)
    else:
        print("[!] No interactive mode selected. Use -i for interactive mode.\n")
        print("Example: python3 Insta.py -i -w")

# ================= ENTRY =================
if __name__ == "__main__":
    main()
