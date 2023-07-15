import json

import connect
from mongoengine import disconnect
from models import Authors, Quotes
from typing import List, Dict


def read_authors(authors: str) -> List[Dict]:
    with open(authors, 'r', encoding='utf-8') as fd:
        result = json.load(fd)
    return result


def read_quotes(quotes: str) -> List[Dict]:
    with open(quotes, 'r', encoding='utf-8') as fd:
        result = json.load(fd)
    return result


def seed_authors():
    Authors.objects().delete()
    authors = read_authors('authors.json')
    for author in authors:
        Authors(
            fullname=author.get('fullname'),
            born_date=author.get('born_date'),
            born_location=author.get('born_location'),
            description=author.get('description')
        ).save()


def seed_quotes():
    with open('quotes.json', 'r') as f:
        quotes_json = json.load(f)

    for quote in quotes_json:
        author_name = quote.get('author')
        # print(author_name)
        try:
            author = Authors.objects(fullname=author_name).first()
        except Authors.DoesNotExist:
            print(f"Author not found for fullname: {author_name}, skipping quote.")
            continue

        try:
            quote_obj = Quotes(
                quote=quote.get('quote'),
                author=author,
                tags=quote.get('tags')
            )
            quote_obj.save()
        except Authors.MultipleObjectsReturned:
            print(f"Multiple authors found for fullname: {quote.get('author')}")





if __name__ == "__main__":
    # seed_authors()
    seed_quotes()
    disconnect()
