import string
import os
import requests
from bs4 import BeautifulSoup

MSG_INVALID_MOVIE_PAGE = 'Invalid movie page!'
WORD_TITLE = 'title'
MSG_CONTENT_SAVED = 'Content saved.'
MSG_THE_URL_RETURNED = 'The URL returned %d'
FILE = 'source.html'
MODE_WRITE_IN_BYTES = 'wb'
MODE_WRITE = 'w'
URL_HOST = 'https://www.nature.com'
SELECTOR_SPAN = 'span', {"class": "c-meta__type"}
SELECTOR_LI = 'li', {"class": "app-article-list-row__item"}
SELECTOR_LINK = 'a', {"class": "c-card__link u-link-inherit"}
TEXT_NEWS = 'News'
DIR_PAGE = 'Page_%d'

SELECTOR_ARTICLE_BODY = 'div', {"class": "c-article-body main-content"}


def url_page(page):
    return '%s/nature/articles?sort=PubDate&year=2020&page=%d' % (URL_HOST, page)


def url_article(link):
    return "%s%s" % (URL_HOST, link)


def parse_file_name(title):
    for char in string.punctuation:
        title = title.replace(char, '')
    for char in string.whitespace:
        title = title.replace(char, '_')

    return "%s.txt" % title


def parse_body(body):
    for char in string.whitespace:
        body.replace(char, '')
    return body
    # return " ".join(body.split())


def main():
    try:
        pages_nr = int(input())
        article_type = str(input())
        cwd_path = os.getcwd()
        for page_nr in range(1, pages_nr+1):
            dir_page = DIR_PAGE % page_nr
            os.mkdir(cwd_path + '/' + dir_page)
            os.chdir(cwd_path + '/' + dir_page)

            # assert WORD_TITLE in url, MSG_INVALID_MOVIE_PAGE
            url = url_page(page_nr)
            print(url)
            response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            assert response.status_code == 200, MSG_THE_URL_RETURNED % response.status_code
            soup = BeautifulSoup(response.content, 'html.parser')
            links = [
                el.find_parents(SELECTOR_LI[0], SELECTOR_LI[1])[0].find(SELECTOR_LINK[0], SELECTOR_LINK[1])
                for el in
                soup.find_all(SELECTOR_SPAN[0], SELECTOR_SPAN[1])
                if el.text == article_type
            ]

            for link in links:
                file = open(parse_file_name(link.text), MODE_WRITE)
                soup = BeautifulSoup(requests.get(url_article(link.attrs['href'])).content, 'html.parser')
                file.write(parse_body(soup.find(SELECTOR_ARTICLE_BODY[0], SELECTOR_ARTICLE_BODY[1]).text))
                file.close()

        # movie_title = soup.find('h1').text
        # movie_description = soup.find('span', {'data-testid': 'plot-l'}).text
        # print(MSG_CONTENT_SAVED)
    except AssertionError as msg:
        print(msg)


if __name__ == '__main__':
    main()

