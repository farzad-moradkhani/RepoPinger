import requests
import time

def measure_download_speed(url, test_duration=3):  # Download for 3 seconds
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

        speed_MBps = total_bytes / (duration * 1024 * 1024)  # bytes to MBps
        return speed_MBps
    except Exception:
        return None

def main():
    input_file = "ping_results.txt"
    output_file = "download_speed_results.txt"
    test_path = "/iso/latest/archlinux-x86_64.iso"  # Large file for speed test
    test_duration = 3  # in seconds

    with open(input_file, "r") as file:
        links = [line.strip().split(" - ")[0] for line in file if line.strip()]

    results = []

    for index, link in enumerate(links):
        print(f"\033[93m[{index+1}/{len(links)}] Testing download: {link}\033[0m")
        full_url = link.rstrip("/") + test_path

        speed = measure_download_speed(full_url, test_duration)
        if speed and speed > 0.01:
            print(f"\033[92mSuccess: {link} - {speed:.2f} MBps\033[0m")
            results.append((link, speed))
        else:
            print(f"\033[91mFailed: {link}\033[0m")

    results.sort(key=lambda x: -x[1])  # Sort by fastest

    with open(output_file, "w") as file:
        for link, speed in results:
            file.write(f"{link} - {speed:.2f} MBps\n")

    print(f"\n\033[92mSaved results to {output_file}\033[0m")

if __name__ == "__main__":
    main()
