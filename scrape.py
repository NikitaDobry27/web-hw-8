import requests
from bs4 import BeautifulSoup
import json

base_url = 'https://quotes.toscrape.com'
url = base_url
quotes_list = []
authors_list = []

while url:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    for quote in soup.findAll('div', class_='quote'):
        quote_dict = {}
        author_dict = {}

        text = quote.find('span', class_='text').text
        author_name = quote.find('small', class_='author').text
        author_url = quote.find('a')['href']
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]

        quote_dict['tags'] = tags
        quote_dict['author'] = author_name
        quote_dict['quote'] = text

        quotes_list.append(quote_dict)

        author_response = requests.get(base_url + author_url)
        author_soup = BeautifulSoup(author_response.text, 'lxml')

        author_born_date = author_soup.find('span', class_='author-born-date')
        author_born_location = author_soup.find('span', class_='author-born-location')
        author_description = author_soup.find('div', class_='author-description')

        if author_born_date:
            author_born_date = author_born_date.text
        if author_born_location:
            author_born_location = author_born_location.text
        if author_description:
            author_description = author_description.text.strip()

        author_dict['fullname'] = author_name
        author_dict['born_date'] = author_born_date
        author_dict['born_location'] = author_born_location
        author_dict['description'] = author_description

        authors_list.append(author_dict)

    next_link = soup.find('li', class_='next')
    url = base_url + next_link.find('a')['href'] if next_link else None

with open('quotes.json', 'w') as f:
    json.dump(quotes_list, f, indent=1)

with open('authors.json', 'w') as f:
    json.dump(authors_list, f, indent=1)
