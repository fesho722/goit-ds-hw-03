import requests
from bs4 import BeautifulSoup
import json
from pymongo import MongoClient

# Задаємо URL бази
base_url = 'http://quotes.toscrape.com'

# Для зберігання даних
quotes = []
authors = {}

# Функція для скрапінгу
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for quote in soup.select('.quote'):
        text = quote.select_one('.text').get_text()
        tags = [tag.get_text() for tag in quote.select('.tags .tag')]
        author_name = quote.select_one('.author').get_text()
        quotes.append({
            "tags": tags,
            "author": author_name,
            "quote": text
        })
        if author_name not in authors:
            author_url = base_url + quote.select_one('.author + a')['href']
            author_response = requests.get(author_url)
            author_soup = BeautifulSoup(author_response.text, 'html.parser')
            authors[author_name] = {
                "fullname": author_soup.select_one('.author-title').get_text(),
                "born_date": author_soup.select_one('.author-born-date').get_text(),
                "born_location": author_soup.select_one('.author-born-location').get_text(),
                "description": author_soup.select_one('.author-description').get_text()
            }

    next_page = soup.select_one('.next a')
    if next_page:
        scrape_page(base_url + '/' + next_page['href'])

# Починаємо скрапінг
scrape_page(base_url)

# Зберігаємо дані у JSON файли
with open('quotes.json', 'w') as f:
    json.dump(quotes, f, indent=4)
with open('authors.json', 'w') as f:
    json.dump(list(authors.values()), f, indent=4)

# Підключаємося до MongoDB
client = MongoClient("mongodb+srv://fesho37:HaHaNorm095@cluster0.yoxuueu.mongodb.net/task2?retryWrites=true&w=majority")
db = client['task2']
authors_collection = db['authors']
quotes_collection = db['quotes']

# Імплементація даних у MongoDB
with open('authors.json') as f:
    authors = json.load(f)
authors_collection.insert_many(authors)

with open('quotes.json') as f:
    quotes = json.load(f)
quotes_collection.insert_many(quotes)

print("Data scraping and importing completed successfully.")
