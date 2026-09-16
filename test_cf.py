import os, json, urllib.request

CF_API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")
HEADERS = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}

req = urllib.request.Request("https://api.cloudflare.com/client/v4/zones?name=houseofstrauss.org", headers=HEADERS)
with urllib.request.urlopen(req) as response:
    print(response.read().decode("utf-8"))
