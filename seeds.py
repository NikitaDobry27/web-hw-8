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
    Quotes.objects().delete()
    quotes = read_quotes('quotes.json')
    for quote in quotes:
        Quotes(
            tags=quote.get('tags'),
            author=Authors.objects.get(fullname=quote.get('author')),
            quote=quote.get('quote'),
        ).save()


if __name__ == "__main__":
    seed_authors()
    seed_quotes()
    disconnect()
