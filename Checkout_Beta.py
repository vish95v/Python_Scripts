import requests
import json

# -----------------------------------------------
# STEP 1: URL (with query params)
# -----------------------------------------------
url = "https://beta.b2b.api.zucora.ths.agency/api/v1/b2b/orders?mp_id=1072513&language=en"

# -----------------------------------------------
# STEP 2: All Headers from cURL
# -----------------------------------------------
headers = {
    "sec-ch-ua-platform": '"Linux"',
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Nzk0NTYxODIsInVzZXJJRCI6IjA1ZmM5NzMyLWMzZGItNGQ5YS04Y2I2LTNiN2U0ODFiNjEzNyJ9.BpIbSVL90Vj82SgGY8E2gKO7NwmVdTYV8CgOu7S_yp4",
    "Referer": "https://beta.zucora.ths.agency/",
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
    "checkout_id": "bb8b3de6-9025-4619-9bb8-65e9bdad0c07",
    "mp_id": "1072513",
    "billing_address": {
        "address": "720 - 1st Avenue N",
        "city": "Saskatoon",
        "country": "CA",
        "state": "SK",
        "zip": "S7K 6R9"
    },
    "po": "ALCH9310",
    "shipping_cost": 0,
    "payment_method": "Credit Card",
    "bambora_txn_id": "10001496",
    "items": [
        "7c5bf9ec-9ba9-44a7-828f-cb8286b710c5"
    ],
    "billing_id": "1677979",
    "shipping_id": "1677979"
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