import os
from dotenv import load_dotenv
from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE, EmailField, BooleanField

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
connect(host=mongo_uri)


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}



class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=50))
    quote = StringField(required=True)
    meta = {
        "collection": "quotes",
        "indexes": [
            "tags",
            {"fields": ["author"]}
        ]
    }

    def to_json(self):
        data = self.to_mongo().to_dict()
        data["author"] = self.author.fullname if self.author else None
        return json_util.dumps(data, ensure_ascii=False )



