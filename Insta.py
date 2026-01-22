#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Shivanshi Insta.py - All-in-One Public Instagram OSINT & Downloader
Standalone version: No args, menu-driven
"""

import instaloader
import os
import sys
import time
from colorama import Fore, Style, init
from getpass import getpass

init(autoreset=True)

# ================= CONFIG =================
PASSWORD = "8252"
L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    save_metadata=False
)
PROFILE_DIR = "profile_pics"

# ================= UTILITIES =================
def clear():
    os.system("clear" if os.name != "nt" else "cls")

def loading():
    clear()
    print("Initializing SHIVANSHI Tool\n")
    for i in range(1, 21):
        bar = "[" + "#" * i + " " * (20 - i) + "]"
        print(f"\rLoading {bar}", end="")
        time.sleep(0.08)
    time.sleep(0.5)

def banner():
    print(Fore.GREEN + r"""
███████╗██╗  ██╗██╗██╗   ██╗ █████╗ ███╗   ██╗███████╗██╗  ██╗██╗
██╔════╝██║  ██║██║██║   ██║██╔══██╗████╗  ██║██╔════╝██║  ██║██║
███████╗███████║██║██║   ██║███████║██╔██╗ ██║███████╗███████║██║
╚════██║██╔══██║██║╚██╗ ██╔╝██╔══██║██║╚██╗██║╚════██║██╔══██║██║
███████║██║  ██║██║ ╚████╔╝ ██║  ██║██║ ╚████║███████║██║  ██║██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝

        SHIVANSHI INSTAGRAM OSINT TOOL
              Made by SHIVANSHI
""" + Style.RESET_ALL)

def password_lock():
    clear()
    banner()
    for _ in range(3):
        pwd = getpass("Enter password: ").strip()
        if pwd == PASSWORD:
            print("\nAccess granted")
            time.sleep(1)
            return
        else:
            print("Wrong password\n")
    print("Too many attempts")
    sys.exit()

# ================= CORE FUNCTIONS =================
def save_to_txt(username, data):
    filename = f"{username}_info.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    print(f"\n[+] Saved to {filename}")

def download_profile_pic(profile):
    os.makedirs(PROFILE_DIR, exist_ok=True)
    L.download_profilepic(profile)
    print(f"[+] Profile picture saved to {PROFILE_DIR}/{profile.username}.jpg")

def check_username(username):
    try:
        instaloader.Profile.from_username(L.context, username)
        print(f"\n[!] Username '{username}' is NOT available")
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"\n[+] Username '{username}' is AVAILABLE")
    except Exception:
        print("\n[!] Unable to check username (rate limited)")

def get_info(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)

        email = getattr(profile, "business_email", None)
        if not email:
            email = "Not Available"

        info = (
            f"\nUsername        : {profile.username}\n"
            f"Full Name       : {profile.full_name}\n"
            f"Bio             : {profile.biography}\n"
            f"Followers       : {profile.followers}\n"
            f"Following       : {profile.followees}\n"
            f"Posts           : {profile.mediacount}\n"
            f"Verified        : {profile.is_verified}\n"
            f"Private Account : {profile.is_private}\n"
            f"External URL    : {profile.external_url}\n"
            f"Public Email    : {email}\n"
        )

        print(info)

        if input("Save results to TXT? (y/n): ").lower() == "y":
            save_to_txt(username, info)

        if input("Download profile picture? (y/n): ").lower() == "y":
            download_profile_pic(profile)

    except instaloader.exceptions.ProfileNotExistsException:
        print("\n[!] Failed to fetch data")
        print("Reason: Username does not exist")

    except instaloader.exceptions.PrivateProfileNotFollowedException:
        print("\n[!] Failed to fetch data")
        print("Reason: Account is private")

    except Exception as e:
        print("\n[!] Failed to fetch data")
        print("Reason: Username invalid / private / rate limited")
        print(e)

# ================= MENU =================
def menu():
    while True:
        clear()
        banner()
        print("[1] Get Instagram Public Info")
        print("[2] Check Username Availability")
        print("[3] Exit\n")

        choice = input("Select option: ").strip()

        if choice == "1":
            username = input("\nEnter Instagram username: ").strip()
            clear()
            banner()
            get_info(username)
            input("\nPress Enter to continue...")

        elif choice == "2":
            username = input("\nEnter username to check: ").strip()
            check_username(username)
            input("\nPress Enter to continue...")

        elif choice == "3":
            print("Exiting")
            sys.exit()

        else:
            print("[!] Invalid option")
            time.sleep(1)

# ================= MAIN =================
if __name__ == "__main__":
    loading()
    password_lock()
    menu()
