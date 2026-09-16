import os, json, urllib.request

CF_API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")
HEADERS = {"Authorization": f"Bearer {CF_API_TOKEN}", "Content-Type": "application/json"}

# 1. Get zone ID for houseofstrauss.org
req = urllib.request.Request("https://api.cloudflare.com/client/v4/zones?name=houseofstrauss.org", headers=HEADERS)
with urllib.request.urlopen(req) as response:
    res = json.loads(response.read().decode("utf-8"))
    zone_id = res["result"][0]["id"]

# 2. Get existing CNAMEs
req2 = urllib.request.Request(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=CNAME", headers=HEADERS)
with urllib.request.urlopen(req2) as response:
    existing = json.loads(response.read().decode("utf-8"))["result"]

for record in existing:
    if record["name"] in ["houseofstrauss.org", "www.houseofstrauss.org"]:
        req_del = urllib.request.Request(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record['id']}", 
                                         headers=HEADERS, method="DELETE")
        with urllib.request.urlopen(req_del) as response:
            print(f"Deleted {record['name']}")

