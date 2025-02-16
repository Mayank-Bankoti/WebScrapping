import requests
import queue

# Create a queue for proxies
q = queue.Queue()
valid_proxies = []

# Read proxy list from file and add to queue
with open("proxy_list.txt", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)

# Function to check proxy validity
def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get(
                "http://ipinfo.io/json",  # Checking the IP
                proxies={"http": f"http://{proxy}", "https": f"https://{proxy}"},
                timeout=5  # Set timeout to avoid slow proxies
            )
            if res.status_code == 200:
                valid_proxies.append(proxy)
                print(f"Proxy {proxy} is valid!")
        except requests.exceptions.RequestException:
            print(f"Proxy {proxy} is not working.")

# Run the proxy checker
check_proxies()

# Save valid proxies
with open("valid_proxies.txt", "w") as f:
    f.write("\n".join(valid_proxies))
