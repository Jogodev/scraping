import requests
from bs4 import BeautifulSoup
import csv
# CODE POUR UN LIVRE
#url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

#url pour une catégorie
url = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# product_page_url = soup.find()
# print(product_page_url)
# title = soup.find('h1')
# print(title)
# image_url = soup.find('img')
# print(image_url)
# tabletd = soup.findAll('td')
# print(tabletd)
#
# with open("books.csv", "w") as book:
#     book.write("product_page_url, universal_ product_code (upc), title, price_including_tax, price_excluding_tax "
#                ",number_available ,product_description, category, review_rating, image_url \n")
#     book.write(str(title) + ' , ' + str(tabletd) + ' , ' + str(image_url


category = soup.findAll('article', class_='product_pod')
print(category)
#[print(str(a) + '\n') for a in categs]
#for li in categs:





