import requests
import json
# base_key = input()
# sym_key = input()

TOKEN_MONEY = '53b5449d39e69c8a9664d197c542369a'

TOKEN_SEC = 'b24d3153a1e7469291ced0e84df849fa'

# r = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key={TOKEN_MONEY}&base={base_key}&symbols={sym_key}")

r = requests.get(f'https://openexchangerates.org/api/latest.json?app_id={TOKEN_SEC}')

resp = json.loads(r.content)

print(resp)
