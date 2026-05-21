import requests
import json

# -----------------------------------------------
# STEP 1: URL (with query params)
# -----------------------------------------------
url = "https://uat.api.b2b.zucora.ths.agency/api/v1/b2b/orders?mp_id=1039575&language=en"

# -----------------------------------------------
# STEP 2: All Headers from cURL
# -----------------------------------------------
headers = {
    "sec-ch-ua-platform": '"Linux"',
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Nzk4ODY3MjIsInVzZXJJRCI6IjljMTI0MDAxLTA4NTEtNDI3OS04YmZhLWEyMjk3MmU1MTU2NSJ9.tbX-PLwrD-e_H6u1LYZQHhcjZZ6yDORWlD9g2PGFB60",
    "Referer": "https://uat.zucora.ths.agency/",
    "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json"
}

# -----------------------------------------------
# STEP 3: Complete Payload from -data
# -----------------------------------------------
payload = {
    "checkout_id": "5cf2e882-bdea-4641-b929-64ee869bd172",
    "mp_id": "1039575",
    "billing_address": {
        "address": "9900 Cavendish Suite 400",
        "city": "St. Laurent",
        "country": "Canada",
        "state": "QC",
        "zip": "H4M 2V2"
    },
    "po": "ALCH2669",
    "shipping_cost": 0,
    "payment_method": "Credit Card",
    "bambora_txn_id": "10001497",
    "items": [
        "3ce5dc41-2e5c-45c6-a03c-a1cf97fb25f8"
    ],
    "billing_id": "1625498",
    "shipping_id": "1626818"
}

# -----------------------------------------------
# STEP 4: Hit API 5 times with same transaction ID
# -----------------------------------------------
for i in range(1, 6):
    response = requests.post(url, headers=headers, json=payload)
    
    print(f"\n========== Request {i} ==========")
    print(f"Status Code : {response.status_code}")
    
    try:
        print(f"Response    : {json.dumps(response.json(), indent=2)}")
    except Exception:
        print(f"Response    : {response.text}")   # fallback if not JSON