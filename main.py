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
    cursor.execute("SELECT id, name, price,category, img FROM products")  # SQL query
    rows = cursor.fetchall()
    conn.close()

    # Convert rows into a list of dictionaries
    products = [
        {'id': row[0], 'name': row[1], 'price': row[2],'category': row[3],'img': row[4]}
        for row in rows
    ]
    return products
def fetch_product_by_id(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, price, category, img FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
    except Exception as e:
        row = None
    conn.close()
    if row:
        return {'id': row[0], 'name': row[1], 'price': row[2], 'category': row[3],'img': row[4]}
    return None

#main page layout
def main_page_layout():
    products = fetch_products()
    categories = list(set(product['category'] for product in products))
    
    category_cards = [
        dbc.Card(
            dbc.CardBody([
                html.H5(category, className="card-title"),
                dbc.Button("Explore", href=f"/products/{category}", color="primary", className="mt-3")
            ]),
            style={"margin-bottom": "20px", "text-align": "center"}
        ) for category in categories
    ]
    
    return html.Div([
        html.H1("Welcome to Our Store!", style={"text-align": "center", "margin-bottom": "40px"}),
        dbc.Container([
            dbc.Row([
                dbc.Col(card, width=4) for card in category_cards  # Responsive grid
            ], className="gy-4")  # Adds spacing between rows
        ]),
        dbc.Row([
            dbc.Col(dbc.Button("View All Products", href="/products", color="secondary", className="mt-4"), width={"size": 2, "offset": 5})
        ])
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
    product_cards = [
        dbc.Card(
            dbc.CardBody([
                html.H5(product['name'], className="card-title"),
                html.Img(src=product['img'], className="card-img-top", style={"border-radius": "15px"}),  # Dynamic image
                html.P(f"Price: ${product['price']:.2f}", className="card-text"),
                dbc.Button("View Details", href=f"/product/{product['id']}", color="info", className="mt-2")
            ]),
            style={"margin-bottom": "20px", "text-align": "center"}
        ) for product in filtered_products
    ]

    return html.Div([
        html.H1(f"Products in {category}", style={"text-align": "center", "margin-bottom": "30px"}),
        dbc.Container([
            dbc.Row([
                dbc.Col(card, width=4) for card in product_cards
            ], className="gy-4")
        ]),
        dbc.Button("Back to Categories", href="/", color="warning", className="mt-4", style={"margin-left": "20px"})
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
        return html.Div([
            html.H1("Product Not Found", style={"text-align": "center", "margin-bottom": "20px"}),
            dbc.Button("Back to Categories", href="/", color="danger", className="mt-4")
        ])


    return html.Div([
        html.H1(product['name'], style={"text-align": "center", "margin-bottom": "30px"}),
        dbc.Container([
            dbc.Row([
                dbc.Col(html.Img(src=product['img'], style={"border-radius": "15px", "width": "100%"}), width=6),  # Dynamic image
                dbc.Col([
                    html.H4(f"Category: {product['category']}", className="mb-3"),
                    html.H4(f"Price: ${product['price']:.2f}", className="mb-4"),
                    dbc.Button("Back to Categories", href="/", color="primary", className="me-2"),
                    dbc.Button("View All Products", href="/products", color="secondary")
                ], width=6)
            ])
        ])
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