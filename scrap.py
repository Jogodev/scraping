import requests
import csv
import urllib.request
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin

product_page_url = []
title = []
product_description = []
category = []
review_rating = []
image_url = []
table_book = []

url = "http://books.toscrape.com/index.html"

def click(urls):
    return requests.get(urls)

def paginate(url):
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
            get_all_books(url_next)


def get_all_books(url):
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
            product_description = book_soup.find('div', {'id': 'product_description'}).findNext('p')
        except AttributeError as error:
            product_description = "Ce livre n'a pas de description"
        table_book_upc = book_soup.find('table', class_='table table-striped').findNext('td').text
        table_book_tax_excl = book_soup.find('table', class_='table table-striped').findNext('td').findNext(
            'td').findNext('td').text
        table_book_tax_incl = book_soup.find('table', class_='table table-striped').findNext('td').findNext(
            'td').findNext('td').findNext('td').text
        table_book_stock = book_soup.find('table', class_='table table-striped').findNext('td').findNext('td').findNext(
            'td').findNext('td').findNext('td').findNext('td').text
        rating = (book_soup.find('p', class_='star-rating').findAll('i'))
        review = book_soup.find('table', class_='table table-striped').findNext('td').findNext('td').findNext(
                'td').findNext('td').findNext('td').findNext('td').findNext('td').text
        image_url = book_soup.find('div', class_='item active').find('img')
        image_url_replace = image_url['src'].replace("../../", "")
        image_url_absolute = (("http://books.toscrape.com/") + (image_url_replace))
        im = Image.open(urllib.request.urlopen(image_url_absolute))
        im.save(f"{title_book}_image.png")

        with open(f"{categ}_books.csv", "a", encoding="utf-8") as csv_book:
            writer = csv.writer(csv_book)
            for product_page_url, category, title, product_description, upc, price_including_tax, price_excluding_tax, number_available, rating, review in zip(
                    str(link_book), str(categ), str(title_book), product_description, str(table_book_upc),
                    str(table_book_tax_excl), str(table_book_tax_incl), str(table_book_stock), str(len(rating)),
                    review):
                writer.writerow(
                    [link_book, categ, title_book, product_description, table_book_upc, table_book_tax_excl,
                    table_book_tax_incl, table_book_stock, rating, review])
    paginate(url)

def get_all_categories(url):
    response = requests.get(url)
    category_soup = BeautifulSoup(response.content, 'html.parser')
    categories = category_soup.find('div', class_='side_categories').find('ul').find('ul').findAll('a', href=True)
    for category in categories:
        url_change_category = category['href'].replace("..", "")
        link_category = (("http://books.toscrape.com/") + (url_change_category))
        print(link_category)
        with open(f'{category.text.strip()}_books.csv', "w", encoding='utf-8') as csv_book:
            writer = csv.writer(csv_book)
            header = ['product_page_url', 'category', 'title', 'product_description', 'upc', 'price_including_tax',
                    'price_excluding_tax', 'number_available', 'rating', 'review']

            get_all_books(link_category)

get_all_categories(url)



# array[2]