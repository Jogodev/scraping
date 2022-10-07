import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

product_page_url = []
title = []
product_description = []
category = []
review_rating = []
image_url = []
table_book = []

# url = "http://books.toscrape.com/catalogue/category/books/christian-fiction_34/index.html"
# url = "http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"
# url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
url = "http://books.toscrape.com/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


def click(urls):
    return requests.get(urls)


# def paginate(page_soup):
#     next_button = page_soup.find('li', class_='next').find('a', href=True)
#     if next_button:
#         url_change = url.replace('index.html', str(next_button['href']))
#         next_page = click(url_change)
#         return next_page
#     else:
#         print("Non")
# paginate()

def get_all_books():
    link_books = soup.find('ol', class_='row').findAll('a', href=True)
    for books in link_books:
        link_book = (('http://books.toscrape.com/') + (books['href']))
        book_pages = click(link_book)
        book_soup = BeautifulSoup(book_pages.content, 'html.parser')
        categ = book_soup.find('li', class_='active').findPrevious('a')
        title_book = book_soup.find('li', class_='active')
        product_description = book_soup.find('div', {'id': 'product_description'}).findNext('p')
        table_book_upc = book_soup.find('table', class_='table table-striped').findNext('td')
        table_book_tax_excl = book_soup.find('table', class_='table table-striped').findNext('td').findNext('td').findNext('td')
        table_book_tax_incl = book_soup.find('table', class_='table table-striped').findNext('td').findNext('td').findNext('td').findNext('td')
        table_book_stock = book_soup.find('table', class_='table table-striped').findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').findNext('td')
        rating = (book_soup.find('p', class_='star-rating').findAll('i'))
        review = book_soup.find('table', class_='table table-striped').findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').findNext('td').findNext('td')
        header = ['product_page_url', 'category', 'title', 'product_description', 'upc', 'price_including_tax', 'price_excluding_tax', 'number_available', 'rating', 'review']
        with open("books.csv", "w") as bookfile:
            writer = csv.writer(bookfile, delimiter=",")
            writer.writerow(header)

            for urls, categ, title_book, product_description, table_book_upc, table_book_tax_excl, table_book_tax_incl, table_book_stock, rating, review in zip(link_book, categ, title_book, product_description, table_book_upc, table_book_tax_excl, table_book_tax_incl, table_book_stock, str(len(rating)), review):
                writer.writerow([link_book, categ, title_book, product_description, table_book_upc, table_book_tax_excl, table_book_tax_incl, table_book_stock, rating, review])









        # with open("books.csv", "a") as bookfile:
        #     bookfile.write(
        #         "product_page_url ; category ; title ; product_description ; universal_ product_code (upc) ; price_including_tax ; "
        #         "price_excluding_tax ; number_available  ; rating ; review \n")
        #     bookfile.write(str(link_book) + ' ; ' + str(categ) + ' ; ' + str(title_book) + ' ; ' + str(
        #         product_description) + ' ; ' + str(table_book_upc) + ' ; ' + str(table_book_tax_excl) + ' ; ' + str(
        #         table_book_tax_incl) + ' ; ' + str(table_book_stock) + ' ; ' + str(len(rating)) + ' ; ' + str(review))





get_all_books()

# def get_all_categories():
#     categories = soup.find('div', class_='side_categories').find('ul').find('ul').findAll('a', href=True)
#     for category in categories:
#         url_change_category = category['href'].replace("..", "")
#         link_category = (('http://books.toscrape.com/') + (url_change_category))
#         category_result = click(link_category)
#         category_soup = BeautifulSoup(category_result.content, 'html.parser')
# get_all_categories()


