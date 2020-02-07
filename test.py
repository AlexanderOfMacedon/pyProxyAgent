from scraper import Scraper
from spider import SpiderRusFishing
from psql import Postresql

database = Postresql({
    'database': 'rusfishing',
    'user': 'postgres',
    'password': '081099',
    'host': 'localhost',
    'port': '5432'
})

# database.createTable('texts', {'main_place': 'TEXT', 'mini_place': 'TEXT', 'text': 'TEXT', 'date': 'varchar(12)',
#                                'is_dialog': 'BOOL'})
# print(database.columns('texts'))
# database.deleteTable('texts')
# print(database.select('texts'))
print(len(database.select('texts')))
# spider = SpiderRusFishing(database=database)
# spider.start()


