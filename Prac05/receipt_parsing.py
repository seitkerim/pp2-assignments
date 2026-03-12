import re
import json

# читаем файл
with open(r"C:\Users\alisher\pp2\pp2-assignments\Prac05\raw.txt", "r", encoding="utf-8") as f:
    text = f.read()


# Extract prices

price_pattern = r"\d[\d\s]*,\d{2}"
prices = re.findall(price_pattern, text)



# Extract product names
# (between item number and quantity line)

product_pattern = r"\d+\.\n(.+?)\n\d"
products = re.findall(product_pattern, text)



# Extract total amount

total_pattern = r"ИТОГО:\s*([\d\s]+,\d{2})"
total = re.search(total_pattern, text)
total_amount = total.group(1) if total else None



# Extract date and time

datetime_pattern = r"Время:\s*(\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2})"
datetime_match = re.search(datetime_pattern, text)
datetime = datetime_match.group(1) if datetime_match else None



# Extract payment method
payment_pattern = r"(Банковская карта|Наличные)"
payment = re.search(payment_pattern, text)
payment_method = payment.group(1) if payment else None



# Structured output

data = {
    "products": products,
    "prices": prices,
    "total_amount": total_amount,
    "datetime": datetime,
    "payment_method": payment_method
}

print(json.dumps(data, ensure_ascii=False, indent=4))