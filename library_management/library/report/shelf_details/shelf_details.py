# Copyright (c) 2024, priyanka and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    shelves = frappe.get_all('Shelf', fields=['name', 'shelf_name'])
    
    columns = [{
        'label': shelf.name, 
        'fieldname': shelf.name, 
        'fieldtype': 'Link',
        'options':'Article'
        } for shelf in shelves]
    
    shelf_books = {shelf.name: [] for shelf in shelves}
    
    articles = frappe.get_all('Article', fields=['article_name', 'shelf_names'])
                            
    for article in articles:
        if article.shelf_names in shelf_books:
            shelf_books[article.shelf_names].append(article.article_name)
    
    max_books = max(len(books) for books in shelf_books.values())
    
    data = []
    
    for i in range(max_books):
        row = {}
        for shelf in shelves:
            if i < len(shelf_books[shelf.name]):
                row[shelf.name] = shelf_books[shelf.name][i]
            else:
                row[shelf.name] = ''
        data.append(row)
    
    return columns, data
