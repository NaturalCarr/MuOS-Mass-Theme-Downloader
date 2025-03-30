#!/usr/bin/env python3
import os
import time
import json
import urllib.request
import urllib.error
from datetime import datetime
import sys

# Config
REPO = "MustardOS/theme"
LATEST_RELEASE_API = f"https://api.github.com/repos/{REPO}/releases/latest"
OUTPUT_DIR = "muxthm_downloads"
RETRY_DELAY = 180  # seconds
LOG_FILE = "muxthm_download_errors.log"

# ANSI control
COLOR_GREEN = "\033[92m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"
CLEAR_LINE = "\033[K"
CURSOR_HIDE = "\033[?25l"
CURSOR_SHOW = "\033[?25h"

os.makedirs(OUTPUT_DIR, exist_ok=True)
downloaded = set(os.listdir(OUTPUT_DIR))
saved_lines = []


def log_error(name, error_message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] {name} - {error_message}\n")


def fetch_latest_release():
    print("Fetching latest release info...")
    req = urllib.request.Request(LATEST_RELEASE_API, headers={"User-Agent": "Python"})
    try:
        with urllib.request.urlopen(req) as response:
            release_data = json.load(response)
            # Print the current release URL with color formatting
            print(f"{COLOR_GREEN}Current Release:{COLOR_RESET} {release_data.get('html_url', 'Unknown')}")
            # Print the download directory with updated label and color formatting
            print(f"{COLOR_GREEN}Download Directory:{COLOR_RESET} {os.path.abspath(OUTPUT_DIR)}")
            return release_data
    except urllib.error.URLError as e:
        print(f"Error fetching release info: {e}")
        return None


def retry_countdown(seconds):
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(f"\rRetrying in {remaining} seconds...{CLEAR_LINE}")
        sys.stdout.flush()
        time.sleep(1)
    print("\rRetrying now..." + CLEAR_LINE)


def format_size(size_bytes):
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {units[i]}"


def refresh_status_block(download_name, downloaded_bytes, size_expected, completed_files, total_files, completed_bytes, total_bytes):
    if download_name:  # Always show the file name in "Downloading"
        progress = f"[{format_size(downloaded_bytes)}/{format_size(size_expected)}]" if size_expected > 0 else ""
        downloading_line = f"{COLOR_GREEN}Downloading:{COLOR_RESET} {download_name} {progress}"
    else:  # Clear the "Downloading" field when no file is being downloaded
        downloading_line = f"{COLOR_GREEN}Downloading:{COLOR_RESET} "

    completed_line = f"{COLOR_GREEN}Completed:{COLOR_RESET} {completed_files}/{total_files} files, {format_size(completed_bytes)}/{format_size(total_bytes)}"

    # Move the cursor up to overwrite the status block
    sys.stdout.write("\033[2F")  # Move up 2 lines to overwrite the status block
    sys.stdout.write(CLEAR_LINE + downloading_line + "\n")
    sys.stdout.write(CLEAR_LINE + completed_line + "\n")
    sys.stdout.flush()


def download_file(name, url, size_expected, completed_files, total_files, completed_bytes, total_bytes):
    last_shown_kb = 0  # Track progress in 100 KB increments
    refresh_status_block(name, 0, size_expected, completed_files, total_files, completed_bytes, total_bytes)  # Show the file name immediately
    while True:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Python"})
            with urllib.request.urlopen(req) as response:
                downloaded_bytes = 0
                chunk_size = 8192
                with open(os.path.join(OUTPUT_DIR, name), "wb") as f:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded_bytes += len(chunk)
                        if downloaded_bytes // (100 * 1024) > last_shown_kb:  # Update every 100 KB
                            last_shown_kb = downloaded_bytes // (100 * 1024)
                            refresh_status_block(name, downloaded_bytes, size_expected, completed_files, total_files, completed_bytes, total_bytes)
                # Update the "Completed" field after the file is completed
                refresh_status_block("", 0, 0, completed_files + 1, total_files, completed_bytes + size_expected, total_bytes)
                return downloaded_bytes
        except Exception as e:
            log_error(name, str(e))
            print(f"\nError downloading {name}: {e}")
            retry_countdown(RETRY_DELAY)
            refresh_status_block(name, 0, size_expected, completed_files, total_files, completed_bytes, total_bytes)


def main():
    # Clear any residual output and ensure the cursor starts fresh
    sys.stdout.write("\033c")  # Clear the screen
    sys.stdout.flush()

    print(CURSOR_HIDE)  # Ensure cursor is hidden at the start
    try:
        data = fetch_latest_release()
        if not data:
            print(CURSOR_SHOW)  # Show cursor before exiting
            return

        all_assets = [
            (a["name"], a["browser_download_url"], a["size"])
            for a in data.get("assets", [])
            if a["name"].endswith(".muxthm")
        ]

        pending_assets = [
            (name, url, size) for (name, url, size) in all_assets if name not in downloaded
        ]

        total_files = len(pending_assets)
        total_bytes = sum(size for (_, _, size) in pending_assets)

        # Ensure this output happens after the command prompt
        print(f"Found {total_files} .muxthm files to download.")
        print()  # Reserve line

        completed_files = 0
        completed_bytes = 0

        for name, url, size in pending_assets:
            downloaded_bytes = download_file(
                name, url, size,
                completed_files, total_files,
                completed_bytes, total_bytes
            )
            completed_files += 1
            completed_bytes += size

        # Move the cursor to the bottom of the output after all downloads
        sys.stdout.write("\033[0J")  # Clear everything below the cursor
        print("All .muxthm downloads from latest release complete.")
        print()  # Add an extra line to ensure the command prompt appears below
    finally:
        print(CURSOR_SHOW)  # Ensure cursor is shown even if an error occurs

if __name__ == "__main__":
    # Ensure all output happens after the command prompt
    main()
