import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# -----------------------------------------------
# URL, Headers, Payload
# -----------------------------------------------
url = "https://stage.b2b.api.zucora.ths.agency/api/v1/b2b/orders?mp_id=1035464&language=en"

headers = {
    "sec-ch-ua-platform": '"Linux"',
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Nzk4ODUxODMsInVzZXJJRCI6ImJkNjJiYjYyLTg3M2MtNGE5Yi05MzE0LTJlZGM1NjBiZjFjMiJ9.tYi0vSvUYcN5ObUnuR4vf2kaCKF_kRJ8SSVZLy0shnM",
    "Referer": "https://stage.zucora.ths.agency/",
    "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json"
}

payload = {
    "checkout_id": "2b3216ea-a11b-4277-a8da-4134184d9cac",
    "mp_id": "1035464",
    "billing_address": {
        "address": "9900 Cavendish Suite 400",
        "city": "St. Laurent",
        "country": "CA",
        "state": "QC",
        "zip": "H4M 2V2"
    },
    "po": "ALCH4316",
    "shipping_cost": 0,
    "payment_method": "Credit Card",
    "bambora_txn_id": "10001499",
    "items": [
        "dd2349fd-8277-455c-bd57-14cf0b6f08a0"
    ],
    "billing_id": "1617083",
    "shipping_id": "1617084"
}

# -----------------------------------------------
# Single request function
# -----------------------------------------------
def send_request(request_num):
    response = requests.post(url, headers=headers, json=payload)
    try:
        return request_num, response.status_code, response.json()
    except Exception:
        return request_num, response.status_code, response.text

# -----------------------------------------------
# Fire ALL 5 requests at the SAME TIME
# -----------------------------------------------
print("🚀 Firing all 5 requests simultaneously...\n")

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(send_request, i): i for i in range(1, 6)}

    for future in as_completed(futures):
        req_num, status, response = future.result()
        print(f"========== Request {req_num} ==========")
        print(f"Status Code : {status}")
        print(f"Response    : {json.dumps(response, indent=2)}\n")