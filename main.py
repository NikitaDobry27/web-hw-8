import connect

from prettytable import PrettyTable
from models import Authors, Quotes


def search_by_tag(tags: str = None):
    if tags:
        quotes = Quotes.objects(tags__in=tags)
    else:
        quotes = Quotes.objects.all()
    return quotes


def search_quotes_by_author(author_name: str):
    author = Authors.objects(fullname=author_name).first()

    if not author:
        return None

    quotes = Quotes.objects(author=author)
    return quotes


def text_parser(text: str):
    mod = text.strip().split(':')
    command = mod[0]

    if command == 'name':
        data = ':'.join(mod[1:]).strip()
    else:
        data = ':'.join(mod[1:]).strip().split(',')
    return command, data


COMMANDS = {
    'tag': search_by_tag,
    'tags': search_by_tag,
    'name': search_quotes_by_author
}


def main():
    while True:
        user_input = input('Type your request >>>')

        if user_input.strip().lower() == 'exit':
            break

        command, data = text_parser(user_input)

        if command not in COMMANDS:
            print("Unknown command")
            continue

        result = COMMANDS[command](data)

        if result is None or not result:
            print(f"No result found for {data}")
            continue

        table = PrettyTable(["ID", "Quote", "Author", "Tags"])
        for quote in result:
            quote_dict = quote.to_mongo().to_dict()
            author = Authors.objects(id=quote_dict["author"]).first()
            table.add_row([quote_dict["_id"], quote_dict["quote"], author.fullname, ", ".join(quote_dict["tags"])])

        print(table)


if __name__ == '__main__':
    main()
