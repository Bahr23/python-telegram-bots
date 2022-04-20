from peewee import *

db = SqliteDatabase('database.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = IntegerField(primary_key=True)
    status = CharField()
    name = CharField()
    username = CharField()


class Product(BaseModel):
    id = AutoField()
    name = CharField()
    price = IntegerField()


class Order(BaseModel):
    id = AutoField()
    status = CharField(default='В обработке')
    user = ForeignKeyField(User, backref='orders', on_delete='CASCADE')
    products = CharField()
    address = CharField()
    phone = CharField()


db.create_tables([User, Product, Order])