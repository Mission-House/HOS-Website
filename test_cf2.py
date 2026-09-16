import os, json, urllib.request

CF_API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")
HEADERS = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}

# get zone for mission-house.org
req = urllib.request.Request("https://api.cloudflare.com/client/v4/zones?name=mission-house.org", headers=HEADERS)
with urllib.request.urlopen(req) as response:
    res = json.loads(response.read().decode("utf-8"))
    zone_id = res["result"][0]["id"]

# get records for mission-house.org
req2 = urllib.request.Request(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=CNAME", headers=HEADERS)
with urllib.request.urlopen(req2) as response:
    print(response.read().decode("utf-8"))
