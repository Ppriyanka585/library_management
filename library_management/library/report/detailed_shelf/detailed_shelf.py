import frappe

def execute(filters=None):
    """
    Method generates shelf details.
    Args:
        filters(Frappe dict): contains selected shelf for details.
    Returns:
        columns: article columns.
        data: list of shelves with articles.
    """
    shelf = filters.get("shelf")
    
    if not shelf:
        return [], []
    
    # Gets all data from Row doctype
    rows = frappe.get_all(
        "Row",
        fields=["name", "row"], 
        filters={"shelf_name": shelf},
        order_by="row asc"
    )

    # Initialize dictionary to hold articles for each row
    row_articles = {row["name"]: [] for row in rows}

    # Fetch articles for the given shelf
    articles = frappe.get_all(
        "Article",
        fields=["article_name", "row_no", "shelf_names"]
    )

    # Organize articles under respective rows
    for article in articles:
        shelf_names = article["shelf_names"].split(",") if isinstance(article["shelf_names"], str) else article["shelf_names"]

        if shelf in shelf_names:
            row_no = article["row_no"]
            if row_no in row_articles:
                row_articles[row_no].append(article["article_name"])

    # Determine the maximum number of articles in any row
    max_articles_per_row = max(len(articles) for articles in row_articles.values())

    # Define columns dynamically based on the maximum articles in any row
    columns = [
        {
            "fieldname": f"article_{i+1}", 
            "label": f"Article {i+1}",
            "fieldtype": "Data",
            "width": 200
        }
        for i in range(max_articles_per_row)
    ]

    # Prepare data for the report
    data = []

    for row in rows:
        row_data = {}
        articles = row_articles[row["name"]]
        for i in range(max_articles_per_row):
            if i < len(articles):
                row_data[f"article_{i+1}"] = articles[i]
            else:
                row_data[f"article_{i+1}"] = "" 
        data.append(row_data)

    return columns, data
