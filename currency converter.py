import requests

BASE_URL = 'https://api.exchangerate-api.com/v4/latest/'

def fetch_exchange_rates(base_currency):
    url = f'{BASE_URL}{base_currency}'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}")
    data = response.json()
    return data['rates']

def convert_currency(amount, from_currency, to_currency):
    rates = fetch_exchange_rates(from_currency)
    
    if to_currency not in rates:
        raise ValueError(f"Conversion rate from {from_currency} to {to_currency} not available.")
    
    conversion_rate = rates[to_currency]
    return amount * conversion_rate

def main():
    print("Welcome to the Currency Converter ")
    from_currency = input("Enter the currency you are converting from (e.g., USD, EUR): ").upper()
    to_currency = input("Enter the currency you are converting to (e.g., INR, USD): ").upper()
    amount = float(input(f"Enter the amount in {from_currency}: "))

    try:
        converted_amount = convert_currency(amount, from_currency, to_currency)
        print(f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
