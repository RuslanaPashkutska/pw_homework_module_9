import os
from dotenv import load_dotenv
import json
from mongoengine import connect
from models import Author, Quote

from mongoengine.errors import NotUniqueError


load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
connect(host=mongo_uri)


if __name__ == "__main__":
    with open("authors.json", encoding="utf-8") as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author(
                    fullname=el.get("fullname"),
                    born_date=el.get("born_date"),
                    born_location=el.get("born_location"),
                    description=el.get("description")
                )
                author.save()
            except NotUniqueError:
                print(f"Author exist {el.get('fullname')}")


    with open("quotes.json", encoding="utf-8") as fd:
        data = json.load(fd)
        for el in data:
            author = Author.objects(fullname=el.get("author")).first()
            if author:
                quote = Quote(
                    quote=el.get("quote"),
                    tags=[tag for tag in el.get("tags") if len(tag) <= 15],
                    author=author
                )
                quote.save()
            else:
                print(f"Author not found: {el.get('author')}")
