# Вариант при доступном бесплатном base.

# r = requests.get(f"http://api.exchangeratesapi.io/latest?base={base_key}&symbols={quote_key}")
# resp = json.loads(r.content)
# new_price = resp['rates'][quote_key] * amount
# new_price = round(new_price, 3)
# message =  f"Цена {amount} {base} в {quote} : {new_price}"
# return message