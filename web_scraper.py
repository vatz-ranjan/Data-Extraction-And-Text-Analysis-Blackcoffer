from bs4 import BeautifulSoup
import requests


class WebScrapper:

    def __init__(self):
        self.__url = None
        self.__fileLoc = None
        self.__document = None

    def __scraping(self):
        print("Scanning {}".format(self.__url))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
        webpage = requests.get(self.__url, headers=headers)
        soup = BeautifulSoup(webpage.content, 'html.parser')
        try:
            title = soup.find('h1', attrs={'class': 'entry-title'}).text.replace(' – Blackcoffer Insights', '')
        except:
            title = ''

        try:
            paragraphs = soup.find('div', attrs={'class': 'td-post-content'})
        except:
            paragraphs = None

        self.__document = title
        if paragraphs is not None:
            for paragraph in paragraphs.findAll(['p', 'h3', 'li']):
                text = paragraph.text
                if len(text) < 1: continue
                self.__document = self.__document + "\n" + text

    def __save_text_file(self):
        try:
            file = open(self.__fileLoc, "w")
            file.write(self.__document)
        except:
            file = open(self.__fileLoc, "wb")
            file.write(self.__document.encode('utf-8', 'ignore'))

        file.close()

    def scrape(self, cur_entry_info):
        self.__url = cur_entry_info['URL']
        self.__fileLoc = cur_entry_info['File Loc']
        self.__scraping()
        self.__save_text_file()



