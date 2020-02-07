from spider import SpiderRusFishing
from psql import Postresql

database = Postresql({
    'database': 'rusfishing',
    'user': 'postgres',
    'password': '081099',
    'host': 'localhost',
    'port': '5432'
})


spider = SpiderRusFishing(database=database)
spider.start()


