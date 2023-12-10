from services.choose_random_picture import choose_random_picture
from services.create_api_connection import create_api_connection


service = create_api_connection()

years = choose_random_picture()

print(years)
items = years.get('files', [])

# print("items: ", items)
