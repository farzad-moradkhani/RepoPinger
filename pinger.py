import subprocess
import time
from urllib.parse import urlparse
import socket

def ping_host(url, timeout=0.3, max_wait=2.0):
    """Ping the host and return the response time in ms, skip if it takes too long."""
    try:
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        if not host:
            return None
        
        # Resolve DNS with timeout
        try:
            socket.setdefaulttimeout(timeout)
            socket.gethostbyname(host)
        except Exception:
            print(f"\033[91mSkipping: {host} (DNS failed)\033[0m")
            return None

        # Run the ping command with a strict Python-level timeout
        start_time = time.time()
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(int(timeout * 1000)), host],
            capture_output=True,
            text=True,
            timeout=max_wait  # Python kills it after this
        )
        elapsed_time = time.time() - start_time

        for line in result.stdout.split("\n"):
            if "time=" in line:
                time_ms = line.split("time=")[1].split(" ")[0]
                return float(time_ms)

    except subprocess.TimeoutExpired:
        print(f"\033[91mSkipping: {host} (Ping timeout)\033[0m")
    except Exception:
        pass

    return None

def main():
    timeout = 0.3  # Ping-level timeout in seconds
    max_wait = 1.0  # Maximum full subprocess duration

    with open("links.txt", "r") as file:
        links = [line.strip() for line in file if line.strip()]

    results = []
    total_links = len(links)
    successful_pings = 0

    for index, link in enumerate(links):
        remaining_percent = ((index + 1) / total_links) * 100
        print(f"\033[93m[{remaining_percent:.2f}%] Testing: {link}\033[0m")

        ping_time = ping_host(link, timeout, max_wait)

        if ping_time is not None:
            print(f"\033[92mSuccess: {link} - {ping_time:.2f} ms\033[0m")
            results.append((link, ping_time))
            successful_pings += 1
        else:
            print(f"\033[91mFailed: {link}\033[0m")

    # Sort results
    results.sort(key=lambda x: x[1])

    with open("ping_results.txt", "w") as file:
        for link, ping_time in results:
            file.write(f"{link}\n")

    print(f"\nResults saved to ping_results.txt")
    print(f"\033[92mTotal successful pings: {successful_pings}\033[0m")

if __name__ == "__main__":
    main()
