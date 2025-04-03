import subprocess
import sys
import time

def test_repo_availability(url, timeout=0.2):
    try:
        start_time = time.time()
        result = subprocess.run(
            ["curl", "-I", "--max-time", str(timeout), url],  # Limit the total time for the request
            capture_output=True,
            text=True,
            check=True
        )
        end_time = time.time()
        if "200 OK" in result.stdout:
            ping_time = end_time - start_time  # Time taken for the request
            return ping_time
    except subprocess.CalledProcessError:
        return None

    return None

def main():
    timeout = 1.0  # Set your desired timeout in seconds (e.g., 1.0s)
    
    with open("RepoPinger/links.txt", "r") as file:
        links = [line.strip() for line in file if line.strip()]
    
    results = []
    total_links = len(links)
    successful_pings = 0
    
    for index, link in enumerate(links):
        remaining_percent = ((index + 1) / total_links) * 100
        # Print testing status with yellow color
        print(f"\033[93m[{remaining_percent:.2f}%] Testing: {link}\033[0m")
        
        ping_time = test_repo_availability(link, timeout)
        
        if ping_time is not None:
            print(f"\033[92mSuccess: {link} - {ping_time:.2f} seconds\033[0m")  # Green for success
            results.append((link, ping_time))
            successful_pings += 1
        else:
            print(f"\033[91mFailed: {link}\033[0m")  # Red for failure
    
    # Sort the results based on ping time
    results.sort(key=lambda x: x[1])

    with open("RepoPinger/ping_results.txt", "w") as file:
        for link, ping_time in results:
            file.write(f"{link} - {ping_time:.2f} seconds\n")
    
    print(f"\nResults saved to ping_results.txt")
    print(f"\033[92mTotal successful pings: {successful_pings}\033[0m")  # Green for successful pings

if __name__ == "__main__":
    main()
