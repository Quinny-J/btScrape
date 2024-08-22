# This project was for an activity within a codenation course
#? A class to scrape book information from the "Books to Scrape" website.
#? Everything has been overly commented and should be commented properly included the class
#! Written by @Quinny-J

import requests
from bs4 import BeautifulSoup
import time

class bScraper:
    """
    A class to scrape book information from the "Books to Scrape" website.
    Written by @Quinny-J
    """

    def __init__(self):
        """
        Initializes the bScraper with the base URL for the website.
        """
        #! Warning: Base URL is hardcoded. Changes to the website's URL structure might require updates here.
        self.base_url = "https://books.toscrape.com/"

    def scrape_books(self, category_url=None, all_books=False):
        """
        Scrapes book information from either all pages or a specific category.

        :param category_url: URL for the category to scrape (if not scraping all books).
        :param all_books: Boolean to determine if all books from all pages should be scraped.
        :return: A list of books and the time taken to scrape.
        """
        books = []
        start_time = time.time()

        if all_books:
            page = 1
            while True:
                #? Information: Scraping all books across multiple pages.
                #! Warning: Pagination URL assumes the format "page-{page}.html"
                url = f"{self.base_url}catalogue/page-{page}.html"
                response = requests.get(url)
                if response.status_code != 200:
                    #! Warning: Non-200 status code indicates an issue, possibly with URL or connectivity.
                    break

                soup = BeautifulSoup(response.text, 'html.parser')
                page_books = self.extract_books_from_soup(soup)
                if not page_books:
                    #! Warning: Empty page indicates end of available books.
                    break
                books.extend(page_books)
                page += 1
        else:
            page = 1
            while True:
                #? Information: Scraping books from a specific category.
                #! Warning: Category URL handling assumes "index.html" for the first page and "page-{page}.html" for subsequent pages.
                url = category_url if page == 1 else category_url.replace("index.html", f"page-{page}.html")
                response = requests.get(url)
                if response.status_code != 200:
                    #! Warning: Non-200 status code indicates an issue with the URL or page.
                    break

                soup = BeautifulSoup(response.text, 'html.parser')
                page_books = self.extract_books_from_soup(soup)
                if not page_books:
                    #! Warning: Empty page indicates the end of the category.
                    break
                books.extend(page_books)
                page += 1

        end_time = time.time()
        estimated_time = round(end_time - start_time, 2)
        return books, estimated_time

    def extract_books_from_soup(self, soup):
        """
        Extracts book details from the BeautifulSoup object.

        :param soup: BeautifulSoup object containing the HTML of the page.
        :return: A list of books with details like title, price, stock, rating, image, and link.
        """
        books = []
        for book in soup.select('.product_pod'):
            #? Information: Extracting book details from HTML.
            #! Warning: Extracted data depends on HTML structure, which might change.
            title = book.h3.a['title']
            price = book.select_one('.price_color').text
            cleaned_price = price.replace('Â', '')  # Remove Â character if present
            stock = book.select_one('.availability').text.strip()
            rating = book.p['class'][1].lower()
            image = self.base_url + book.img['src'].replace('../../', '')
            link = self.base_url + "catalogue/" + book.h3.a['href'].replace('../../', '')
            books.append({
                'title': title,
                'price': cleaned_price,
                'stock': stock,
                'rating': rating,
                'image': image,
                'link': link
            })

        return books

    def scrape_categories(self):
        """
        Scrapes the list of book categories from the main page.

        :return: A list of dictionaries, each containing a category's name and URL.
        """
        #? Information: Fetching categories from the main page.
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        categories = []

        for category in soup.select('.nav-list li ul li a'):
            category_name = category.text.strip()
            category_url = self.base_url + category['href']
            categories.append({'name': category_name, 'url': category_url})

        return categories