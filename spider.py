from random import randint
from time import sleep
import requests

from scraper import Scraper
from handler import Handler


# сначала выгружает все, заводит переменную числоНеобрабатанных, парсит пока эта переменная не ноль. все в start().

class SpiderRusFishing(Scraper):
    def __init__(self, database, handler=None, agentsTableName='agents', timeout=5):
        super().__init__(database=database, agentsTableName=agentsTableName)
        self.baseUrl = 'https://www.rusfishing.ru'
        self.handler = handler
        self.timeout = timeout

    def start(self):
        self.urls = [url for url in self.database.select('forumUrls') if url['handled'] == 'no']
        self.iterator = 0
        while self.iterator < len(self.urls):
            print('осталось:', len(self.urls) - self.iterator)
            sleep(10)
            self.getProxiesAgents()
            self.proxiesAgents.append({'proxy': None, 'agent': None})
            self._getTexts()

    def _getTexts(self):
        proxyIterator = 0
        while proxyIterator < len(self.proxiesAgents):
            internalIterator = 0
            user = self.proxiesAgents[proxyIterator]
            try:
                while internalIterator < 30:
                    if proxyIterator == len(self.proxiesAgents) - 1:
                        sleep(randint(3,5))
                    url = self.urls[self.iterator]
                    pageSource = str(requests.get(url['url'], proxies={"http": user['proxy'], "https": user['proxy']},
                                     headers={'User-Agent': user['agent']}, timeout=self.timeout).content.decode(
                            'utf-8'))
                    handler = Handler(pageSource=pageSource)
                    texts = handler.textHandle()
                    for index in range(len(texts)):
                        texts[index].update({'main_place': url['main_place'], 'mini_place': url['mini_place']})
                    self.database.insert(table_name='texts', insert_data=texts)
                    new_url = url
                    new_url['handled'] = 'yes'
                    self.database.update(table_name='forumUrls', insert_data=new_url)
                    self.iterator += 1
                    internalIterator += 1
                proxyIterator += 1
            except Exception as e:
                proxyIterator += 1


