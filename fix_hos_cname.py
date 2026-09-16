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

target_content = "houseofstrauss-site.pages.dev"

def upsert_cname(name):
    matched = [r for r in existing if r["name"] == name]
    payload = {
        "type": "CNAME",
        "name": name,
        "content": target_content,
        "ttl": 1,
        "proxied": True
    }
    
    if matched:
        rec_id = matched[0]["id"]
        req = urllib.request.Request(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{rec_id}", 
                                     headers=HEADERS, method="PUT", data=json.dumps(payload).encode("utf-8"))
    else:
        req = urllib.request.Request(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records", 
                                     headers=HEADERS, method="POST", data=json.dumps(payload).encode("utf-8"))
        
    with urllib.request.urlopen(req) as response:
        print(f"Updated {name} to {target_content}")

upsert_cname("houseofstrauss.org")
upsert_cname("www.houseofstrauss.org")

