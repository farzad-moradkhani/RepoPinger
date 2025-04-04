import requests
import time
import socket
from urllib.parse import urlparse
from datetime import timedelta

def country_code_to_emoji(code):
    """Convert a 2-letter country code to emoji flag."""
    return ''.join(chr(ord(char) + 127397) for char in code.upper())

def get_country_flag_from_url(url):
    """Resolve IP and get country flag from API."""
    try:
        host = urlparse(url).hostname
        ip = socket.gethostbyname(host)
        response = requests.get(f"https://ipwho.is/{ip}", timeout=5)
        data = response.json()
        country_code = data.get("country_code")
        if country_code:
            return country_code_to_emoji(country_code)
    except:
        return "🌐"
    return "🌐"

def measure_download_speed(url, test_duration=3):
    """Download for a few seconds and calculate speed in MBps."""
    try:
        response = requests.get(url, stream=True, timeout=10)
        start_time = time.time()
        total_bytes = 0

        for chunk in response.iter_content(1024):
            if chunk:
                total_bytes += len(chunk)
            if time.time() - start_time >= test_duration:
                break

        duration = time.time() - start_time
        if duration == 0:
            return None
        speed_MBps = total_bytes / (duration * 1024 * 1024)
        return speed_MBps
    except:
        return None

def format_seconds_to_hms(seconds):
    """Format seconds as HH:MM:SS."""
    return str(timedelta(seconds=int(seconds)))

def main():
    input_file = "ping_results.txt"
    output_file = "download_speed_results.txt"
    test_path = "/iso/latest/archlinux-x86_64.iso"  # Large file for testing
    test_duration = 3  # Download duration per test

    with open(input_file, "r") as file:
        links = [line.strip().split(" - ")[0] for line in file if line.strip()]

    total_links = len(links)
    results = []
    start_all = time.time()

    for index, link in enumerate(links):
        elapsed = time.time() - start_all
        avg_time = elapsed / (index + 1) if index != 0 else 0
        est_total = avg_time * total_links
        remaining = est_total - elapsed
        percentage = ((index + 1) / total_links) * 100
        eta = format_seconds_to_hms(remaining)

        print(f"\033[93m[{percentage:.2f}% ETA: {eta}] Testing download: {link}\033[0m")
        full_url = link.rstrip("/") + test_path

        speed = measure_download_speed(full_url, test_duration)
        flag = get_country_flag_from_url(link)

        if speed and speed > 0.01:
            print(f"\033[92mSuccess: {flag} {link} - {speed:.2f} MBps\033[0m")
            results.append((link, speed, flag))
        else:
            print(f"\033[91mFailed: {flag} {link}\033[0m")

    results.sort(key=lambda x: -x[1])

    with open(output_file, "w") as file:
        for link, speed, flag in results:
            file.write(f"{flag} {link} - {speed:.2f} MBps\n")

    print(f"\n\033[92mSaved results to {output_file}\033[0m")

if __name__ == "__main__":
    main()
