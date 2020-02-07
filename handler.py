from bs4 import BeautifulSoup


class Handler:
    def __init__(self, pageSource):
        self.pageSource = pageSource

    def textHandle(self):
        soup = BeautifulSoup(self.pageSource, "html.parser")
        self.messages = [str(message) for message in
                         soup.find_all('article',
                                       attrs={'class': 'message message--post js-post js-inlineModContainer'})]
        dates = soup.find_all('div', attrs={'class': 'message-cell message-cell--main'})
        self.result = [{'is_dialog': False, 'date': dates[x].find('time').text} for x in range(len(self.messages))]
        self.__dialogCheck()
        self.__sideHandle()
        self.__imageConvert()
        self.__finalHandle()
        self.__deleteHtml('a')
        self.__deleteHtml('span')

        for index in range(len(self.messages)):
            self.result[index].update({"text": self.messages[index]})
        return self.result

    def __dialogCheck(self):
        for index in range(len(self.messages)):
            sttr = str(self.messages[index])
            indexBlockquote = sttr.find('/blockquote>')
            if indexBlockquote > -1:
                sttr = sttr[indexBlockquote + len('/blockquote>'): sttr.find('</div>', indexBlockquote)]
                self.result[index]['is_dialog'] = True
            else:
                index_wrapper = sttr.find('class=\"bbWrapper\">')
                sttr = sttr[index_wrapper + len('class=\"bbWrapper\">'): sttr.find('</div>', index_wrapper)]
            self.messages[index] = sttr

    def __sideHandle(self):
        for index in range(len(self.messages)):
            sttr = str(self.messages[index])
            index_br = sttr.find('</b>')
            while index_br > -1:
                sttr = sttr[index_br + len('</b>'):]
                index_br = sttr.find('</b>')
            sttr = sttr.replace('<br>', '').replace('<br/>', '')
            self.messages[index] = sttr

    def __imageConvert(self):
        for index in range(len(self.messages)):
            sttr = str(self.messages[index])
            index_img = sttr.find('<img ')
            while index_img > -1:
                imageCode = sttr[index_img: sttr.find('>', index_img) + 1]
                title = imageCode[imageCode.find("alt") + 5:]
                title = title[: title.find("\"")]
                sttr = sttr.replace(imageCode, " " + title + " ")
                index_img = sttr.find('<img ')
            sttr = sttr.replace('</img>', '').replace('</br>', '')
            self.messages[index] = sttr

    def __deleteHtml(self, code):
        for index in range(len(self.messages)):
            sttr = str(self.messages[index])
            index_html = sttr.find('<' + code)
            while index_html > -1:
                htmlCode = sttr[index_html: sttr.find(code + '>', index_html) + 1 + len(code)]
                sttr = sttr.replace(htmlCode, ' ')
                index_html = sttr.find('<' + code)
            self.messages[index] = sttr


    def __finalHandle(self):
        for index in range(len(self.messages)):
            sttr = str(self.messages[index])
            sttr = sttr.replace('....', ' ').replace('...', ' ').replace('..', ' ').replace('\n',' ').replace('\r', ' ')
            self.messages[index] = sttr