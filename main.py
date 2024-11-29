import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import sqlite3

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def connect_db():
    conn = sqlite3.connect('database.db')  
    return conn
def fetch_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price,category FROM products")  # SQL query
    rows = cursor.fetchall()
    conn.close()

    # Convert rows into a list of dictionaries
    products = [
        {'id': row[0], 'name': row[1], 'price': row[2],'category': row[3]}
        for row in rows
    ]
    return products
def fetch_product_by_id(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, price, category FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
    except Exception as e:
        row = None
    conn.close()
    if row:
        return {'id': row[0], 'name': row[1], 'price': row[2], 'category': row[3]}
    return None

#main page layout
def main_page_layout():
    products = fetch_products()  # Fetch products from the database

    # Extract unique categories
    categories = list(set(product['category'] for product in products))

    # Build the main page layout with categories only
    return html.Div([
        html.H1("Welcome to Our Store"),
        html.Div([
            html.H2("Categories"),
            html.Ul([
                html.Li(dcc.Link(category, href=f"/products/{category}"))
                for category in categories
            ])
        ]),
        dcc.Link("View All Products", href="/products", style={"margin-top": "20px", "display": "block"})
    ])

# Product list page layout for a specific catalog
def product_list_by_category_layout(category):
    products = fetch_products()
    filtered_products = [p for p in products if p['category'] == category]

    if not filtered_products:
        return html.Div([
            html.H1(f"No products found in {category}."),
            dcc.Link("Back to categories", href="/", style={"margin-top": "20px", "display": "block"})
        ])

    return html.Div([
        html.H1(f"Products in {category}"),
        html.Ul([
            html.Li(dcc.Link(f"{product['name']} - ${product['price']:.2f}", href=f"/product/{product['id']}"))
            for product in filtered_products
        ]),
        dcc.Link("Back to categories", href="/", style={"margin-top": "20px", "display": "block"})
    ])



#all product list
def product_list_page_layout():
    products = fetch_products()  # Fetch products from the database
    return html.Div([
        html.H1("All Products"),
        html.Ul([
            html.Li(dcc.Link(f"{product['name']} - ${product['price']:.2f}", href=f"/product/{product['id']}"))
            for product in products
        ]),
        dcc.Link("Back to Main Page", href="/", style={"margin-top": "20px", "display": "block"})
    ])

# Product detail page layout with link back to correct catalog
def product_detail_layout(product_id):
    product = fetch_product_by_id(product_id)  # Fetch product data by ID
    if not product:
        return html.Div(["Product not found.", dcc.Link("Go back to catalog", href='/')])

    return html.Div([
        html.H1(f"Details for {product['name']}"),
        html.P(f"Category: {product['category']}"),
        html.P(f"Price: ${product['price']:.2f}"),
        dcc.Link("Back to catalog", href="/", style={"margin-top": "20px", "display": "block"})
    ])


# Define the app layout with dynamic routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback to handle navigation
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':  # Main page
        return main_page_layout()

    elif pathname.startswith('/products/'):  # Product list by category
        category = pathname.split('/')[-1].replace('%20', ' ')  # Decode spaces
        return product_list_by_category_layout(category)

    elif pathname == '/products':  # Full product list page
        return product_list_page_layout()

    elif pathname.startswith('/product/'):  # Product detail page
        try:
            product_id_str = pathname.split('/')[-1]
            if not product_id_str.isdigit():
                return html.Div(["Invalid Product ID", dcc.Link("Go back to catalog", href='/')])
            
            product_id = int(product_id_str)
            return product_detail_layout(product_id)
        except Exception as e:
            return html.Div(["Invalid Product ID", dcc.Link("Go back to catalog", href='/')])

if __name__ == '__main__':
    app.run_server(debug=True)