import frappe

def execute(filters=None):
    """
        method generates shelf details
        Args:
            filters(Frappe dict): contains selected shelf for details
        Returns:
            columns: serial number and articles
            data: list of shelves with articles
    """
    shelf = filters.get("shelf")
        
    if not shelf:
        return [], []
    
    # gets all data from Row doctype 
    rows = frappe.get_all(
        "Row",
        fields=["name", "row"], 
        filters={"shelf_name": shelf},
        order_by="row asc")

    columns = [
        {
            "fieldname": "row_number", 
            "label": "Row Number", "fieldtype": "Int", "width": 100},
    ]
    
    max_articles_per_row = 0
    row_articles = {row["name"]: [] for row in rows}

    articles = frappe.get_all(
        "Article",
        fields=["article_name", "row_no", "shelf_names"])

    for article in articles:
        shelf_names = article["shelf_names"].split(",") if isinstance(article["shelf_names"], str) else article["shelf_names"]

        if shelf in shelf_names:
            row_no = article["row_no"]
            if row_no in row_articles:
                row_articles[row_no].append(article["article_name"])

    max_articles_per_row = max(len(articles) for articles in row_articles.values())

    columns += [
        {"fieldname": f"article_{i+1}", "label": f"Article {i+1}", "fieldtype": "Data", "width": 200}
        for i in range(max_articles_per_row)
    ]

    data = []

    for row in rows:
        row_data = {
            "row_number": row["row"]
        }
        articles = row_articles[row["name"]]
        for i in range(max_articles_per_row):
            if i < len(articles):
                row_data[f"article_{i+1}"] = articles[i]
            else:
                row_data[f"article_{i+1}"] = ""  
        data.append(row_data)

    return columns, data
