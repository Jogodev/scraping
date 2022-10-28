import requests
import csv
import urllib.request
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

product_page_url = []
title = []
product_description = []
category = []
review = []
rating = 0
image_url = []
table_book = []

url = "http://books.toscrape.com/index.html"
def click(urls):
    return requests.get(urls)


def paginate(url, book_writer):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    footer = soup.select_one('li.current')
    try:
        print(footer.text.strip())
    except AttributeError as error:
        print('')
    next_page = soup.select_one('li.next>a')
    if next_page:
        next_url = next_page.get('href')
        url_next = urljoin(url, next_url)
        get_all_books(url_next, book_writer)


def get_all_books(url, book_writer):
    response = requests.get(url)
    book_soup = BeautifulSoup(response.content, 'html.parser')
    link_books = book_soup.find('ol', class_='row').findAll('a')
    for books in link_books[1::2]:
        book_url_change = books['href'].replace('../../../', '')
        link_book = (('http://books.toscrape.com/catalogue/') + (book_url_change))
        book_pages = click(link_book)
        book_soup = BeautifulSoup(book_pages.content, 'html.parser')
        categ = book_soup.find('li', class_='active').findPrevious('a').text
        title_book = book_soup.find('li', class_='active').text
        try:
            product_description = book_soup.find('div', {'id': 'product_description'}).findNext('p').text
        except AttributeError as error:
            product_description = "Ce livre n'a pas de description"
        table_book_upc = book_soup.find('table', class_='table table-striped').findAll('td')
        table_book_tax_excl = book_soup.find('table', class_='table table-striped').findAll('td')
        table_book_tax_incl = book_soup.find('table', class_='table table-striped').findAll('td')
        table_book_stock = book_soup.find('table', class_='table table-striped').findAll('td')
        rating = book_soup.find('p', class_='star-rating')
        note = 0
        if rating == book_soup.find('p', class_='star-rating One'):
            note = 1
        elif rating == book_soup.find('p', class_='star-rating Two'):
            note = 2
        elif rating == book_soup.find('p', class_='star-rating Three'):
            note = 3
        elif rating == book_soup.find('p', class_='star-rating Four'):
            note = 4
        else:
            note = 5
        review = book_soup.find('table', class_='table table-striped').findNext('td').findNext('td').findNext(
            'td').findNext('td').findNext('td').findNext('td').findNext('td')
        image_url = book_soup.find('div', class_='item active').find('img')
        image_url_replace = image_url['src'].replace("../../", "")
        image_url_absolute = (("http://books.toscrape.com/") + (image_url_replace))
        im = Image.open(urllib.request.urlopen(image_url_absolute))
        bad_chars = "/:\"?!*$'&`"
        good_chars = "          "
        trantab = link_book.maketrans(bad_chars, good_chars)
        im.save(f"{categ}/{title_book.translate(trantab)[:50]}_image.png")

        book_writer.writerow(
            [link_book, categ, title_book, product_description, table_book_upc[0].text,
             table_book_tax_excl[2].text, table_book_tax_incl[3].text, table_book_stock[5].text, note,
             review.text])
    paginate(url, book_writer)


def get_all_categories(url):
    response = requests.get(url)
    category_soup = BeautifulSoup(response.content, 'html.parser')
    categories = category_soup.find('div', class_='side_categories').find('ul').find('ul').findAll('a', href=True)
    for category in categories:
        url_change_category = category['href'].replace("..", "")
        link_category = (("http://books.toscrape.com/") + (url_change_category))
        print(link_category)
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, category.text.strip())
        csv_directory = os.path.join(current_directory, "all_csv")
        if not os.path.exists(final_directory):
            os.mkdir(final_directory)
        with open(f'{category.text.strip()}_books.csv', "w", encoding='utf-8', newline='') as csv_book:
            writer = csv.writer(csv_book, delimiter=';')
            headers = ['Product page url', 'Category', 'Title', 'Product description', 'UPC', 'Price including tax',
                       'Price excluding tax', 'Number available', 'Rating', 'Review']
            writer.writerow(headers)
            get_all_books(link_category, writer)


def scrap(url):
    get_all_categories(url)

if __name__ == '__main__':
    scrap(url)
