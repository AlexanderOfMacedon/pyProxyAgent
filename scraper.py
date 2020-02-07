import requests
from lxml.html import fromstring
from random import randint


class Scraper:
    def __init__(self, database=None, agentsTableName='agents'):
        self.database = database
        self.agentsTableName = agentsTableName

    def __getProxies(self):
        url = 'https://free-proxy-list.net'
        response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'})
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr'):
            if i.xpath('.//td[7][contains(text(),"yes")]') and i.xpath('.//td[4][contains(text(),"Russian Federation")]'):
                # Grabbing IP and corresponding PORT
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
        self.proxies = list(proxies)[:5]

    def __getAgentsOnline(self, proxy):
        url = 'https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/1'
        response = requests.get(url, proxies={'http': proxy, 'https': proxy}, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/76.0.3809.100 Safari/537.36'}, timeout=10)
        parser = fromstring(response.text)
        userAgents = set()
        for i in parser.xpath('//tbody/tr'):
            user_agent = i.xpath('.//td[1]/a')[0].text
            userAgents.add(user_agent)
        self.agents = list(userAgents)

    def __getAgentsDB(self):
        self.agents = [agent['agent'] for agent in self.database.select(table_name=self.agentsTableName)]

    def getProxiesAgents(self):
        self.__getProxies()
        self.__getAgentsDB()
        proxiesAgents = []
        for proxy in self.proxies:
            indexAgent = randint(0, len(self.agents) - 1)
            proxiesAgents.append({'proxy': proxy, 'agent': self.agents[indexAgent]})
        self.proxiesAgents = proxiesAgents
