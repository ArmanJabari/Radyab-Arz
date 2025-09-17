import requests
from bs4 import BeautifulSoup
import time
import os
import platform

URL = "https://alanchand.com/currencies-price"

# 28 Currencies 
currencies = {
    "USD": "usd",   # US Dollar
    "EUR": "eur",   # Euro
    "AED": "aed",   # UAE Dirham
    "TRY": "try",   # Turkish Lira
    "GBP": "gbp",   # British Pound
    "CNY": "cny",   # Chinese Yuan
    "CAD": "cad",   # Canadian Dollar
    "AUD": "aud",   # Australian Dollar
    "RUB": "rub",   # Russian Ruble
    "MYR": "myr",   # Malaysian Ringgit
    "GEL": "gel",   # Georgian Lari
    "AZN": "azn",   # Azerbaijani Manat
    "THB": "thb",   # Thai Baht
    "OMR": "omr",   # Omani Rial
    "INR": "inr",   # Indian Rupee
    "PKR": "pkr",   # Pakistani Rupee
    "SAR": "sar",   # Saudi Riyal
    "AFN": "afn",   # Afghan Afghani
    "SEK": "sek",   # Swedish Krona
    "CHF": "chf",   # Swiss Franc
    "QAR": "qar",   # Qatari Riyal
    "NOK": "nok",   # Norwegian Krone
    "KWD": "kwd",   # Kuwaiti Dinar
    "BHD": "bhd",   # Bahraini Dinar
    "BRL": "brl",   # Brazilian Real
    "ARS": "ars",   # Argentine Peso
    "JPY": "jpy",   # Japanese Yen (100 units)
    "KRW": "krw"    # South Korean Won (100 units)
}

# Persian digits to English digits
persian_to_english = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")

def convert_digits(text):
    return text.translate(persian_to_english)

def format_number(num_str, currency=None):
    try:
        num_str = num_str.replace(",", "")
        num = float(num_str)
        # Special case for ARS: show one decimal place
        if currency == "ars":
            return f"{num:.1f}"
        # For other currencies, use integer with commas
        return f"{int(num):,}"
    except ValueError:
        return num_str

def fetch_prices():
    # Fixed column widths based on longest entries
    max_currency_length = len("USD")  # 3 characters
    max_buy_length = len("Buy = 316,680")  # 13 characters
    max_sell_length = len("Sell = 326,480")  # 14 characters

    # Print table header
    print(f"╔{'═' * (max_currency_length + 2)}╦{'═' * (max_buy_length + 2)}╦{'═' * (max_sell_length + 2)}╗")
    
    try:
        response = requests.get(URL, timeout=10)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        # Collect currency data
        currency_data = []
        for name, symbol in currencies.items():
            row = soup.find("tr", onclick=f"window.location='/currencies-price/{symbol}'")
            if row:
                buy_price = row.find("td", class_="buyPrice").text.strip()
                sell_price = row.find("td", class_="sellPrice").text.strip()
                
                # Convert Persian numbers → English
                buy_price = convert_digits(buy_price)
                sell_price = convert_digits(sell_price)

                # Format with commas or decimals
                buy_price = format_number(buy_price, symbol)
                sell_price = format_number(sell_price, symbol)

                currency_data.append((name, buy_price, sell_price))
            else:
                currency_data.append((name, None, None))

        # Print table rows without separators between them
        for name, buy_price, sell_price in currency_data:
            currency_text = name.ljust(max_currency_length)
            buy_text = f"Buy = {buy_price}" if buy_price else "Not found"
            sell_text = f"Sell = {sell_price}" if sell_price else "Not found"
            padded_buy = buy_text.ljust(max_buy_length)
            padded_sell = sell_text.ljust(max_sell_length)
            
            print(f"║ {currency_text} ║ {padded_buy} ║ {padded_sell} ║")

        # Print table footer
        print(f"╚{'═' * (max_currency_length + 2)}╩{'═' * (max_buy_length + 2)}╩{'═' * (max_sell_length + 2)}╝")

    except Exception as e:
        print(f"Error fetching data: {e}")

# Update every 1 min
while True:
    fetch_prices()
    time.sleep(10)
    os.system('clear' if platform.system() != 'Windows' else 'cls')