# This project was for an activity within a codenation course
#? A class to scrape book information from the "Books to Scrape" website.
#? Everything has been overly commented and should be commented properly included the class
#! Written by @Quinny-J

#* Import Flask so we can serve the webpage and a few extras
from flask import Flask, render_template, request
#* Importing my bScraper Class
from b_scraper import bScraper

#* Give Flask our app
app = Flask(__name__)
scraper = bScraper()

#* Handle the index route
@app.route('/', methods=['GET', 'POST'])
def home():
    #? Scrape the categories first
    categories = scraper.scrape_categories()
    
    #? Grab the category from the form payload
    selected_category = request.form.get('category')
    
    #? Grab the checkbox from the form payload
    all_books = request.form.get('all_books')

    #? For filtration
    sort_by = request.form.get('sort_by') 
    min_price = request.form.get('min_price') 
    max_price = request.form.get('max_price')

    #? Set some of our variables here
    books = []
    category_name = None
    estimated_time = None
    show_links = False
    books_count = 0

    #? Checking if a category or all_books checkbox is true
    if selected_category or all_books:
        #? If a category is selected then pass the category to our scrape_books function
        if selected_category:
            books, estimated_time = scraper.scrape_books(selected_category)
            category_name = next((c['name'] for c in categories if c['url'] == selected_category), "Selected Category")
            show_links = False
        #? If all_books checkbox is checked, no category is needed
        elif all_books:
            books, estimated_time = scraper.scrape_books(all_books=True)
            category_name = "All Books"
            show_links = True

        #? Filter by price range if provided
        if min_price and max_price:
            min_price = float(min_price)
            max_price = float(max_price)
            books = [book for book in books if min_price <= float(book['price'].replace('£', '').replace(',', '')) <= max_price]

        #? Sort books based on the selected sort option
        if sort_by == 'title':
            books.sort(key=lambda x: x['title'])
        elif sort_by == 'price_low_high':
            books.sort(key=lambda x: float(x['price'].replace('£', '').replace(',', '')))
        elif sort_by == 'price_high_low':
            books.sort(key=lambda x: float(x['price'].replace('£', '').replace(',', '')), reverse=True)

        #? Keep count of how many books were scraped to return data to the page
        books_count = len(books)
    else:
        #? If no category or checkbox is selected and set the estimated time to "N/A"
        estimated_time = "N/A"

    #? Render the template with the scraped data and other vars
    return render_template('index.html', books=books, categories=categories, category_name=category_name, books_count=books_count, estimated_time=estimated_time, show_links=show_links)

#* Run the Flask app with debugging enabled
if __name__ == '__main__':
    app.run(debug=True)
