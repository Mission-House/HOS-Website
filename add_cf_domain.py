import os, json, urllib.request

CF_API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")
ACCOUNT_ID = "a1f4779ae4bb143e54d61f934e63fb6f"
HEADERS = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}
PROJECT_NAME = "houseofstrauss-site"

def add_domain(domain):
    payload = {"name": domain}
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/domains"
    req = urllib.request.Request(url, headers=HEADERS, method="POST", data=json.dumps(payload).encode("utf-8"))
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Added {domain}: ", json.loads(response.read().decode("utf-8"))["success"])
    except urllib.error.HTTPError as e:
        print(f"Failed {domain}: ", e.read().decode("utf-8"))

add_domain("houseofstrauss.org")
add_domain("www.houseofstrauss.org")

