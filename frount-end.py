import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Sample product data categorized by catalog
catalogs = {
    'Electronics': [
        {'id': 1, 'name': 'Laptop', 'description': '', 'price': 000, 'details': ''},
        {'id': 2, 'name': 'Smartphone', 'description': '', 'price': 000, 'details': ''}
    ],
    'Accessories': [
        {'id': 3, 'name': 'Headphones', 'description': '', 'price': 000, 'details': ''},
        {'id': 4, 'name': 'Smartwatch', 'description': '', 'price': 000, 'details': ''}
    ]
}

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Main page layout showing catalogs
def main_page_layout():
    return html.Div([
        html.H1("Product Catalogs"),
        html.Div([
            html.H3("Available Catalogs:"),
            html.Ul([
                html.Li(dcc.Link(catalog, href=f'/catalog/{catalog}'))
                for catalog in catalogs.keys()
            ])
        ])
    ])

# Product list page layout for a specific catalog
def product_list_page_layout(catalog_name):
    if catalog_name not in catalogs:
        return html.Div([
            html.H1(f"Catalog '{catalog_name}' not found."),
            dcc.Link("Back to Main Page", href='/')
        ])

    return html.Div([
        html.H1(f"Products in {catalog_name}"),
        html.Ul([
            html.Li([
                dcc.Link(f"{product['name']} - ${product['price']:.2f}", href=f"/product/{catalog_name}/{product['id']}")
            ]) for product in catalogs[catalog_name]
        ]),
        dcc.Link("Back to Main Page", href='/')
    ])

# Product detail page layout with link back to correct catalog
def product_detail_layout(catalog_name, product_id):
    # Find the product in the specified catalog
    product = next((p for p in catalogs[catalog_name] if p['id'] == product_id), None)

    if product is None:
        return html.Div([
            html.H1("Product not found"),
            dcc.Link("Go back to catalog", href=f"/catalog/{catalog_name}")
        ])
    
    return html.Div([
        html.H1(f"Details for {product['name']}"),
        html.P(f"Description: {product['description']}"),
        html.P(f"Price: ${product['price']:.2f}"),
        html.P(f"Details: {product['details']}"),
        dcc.Link(f"Back to {catalog_name} catalog", href=f'/catalog/{catalog_name}'),
        dcc.Link("Back to main page", href='/', style={"display": "block", "margin-top": "10px"}),
    ])

# Define the app layout with dynamic routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback to control page navigation
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    # Main page
    if pathname == '/':
        return main_page_layout()

    # Catalog product list page (e.g., /catalog/Electronics)
    elif pathname.startswith('/catalog/'):
        catalog_name = pathname.split('/')[-1]
        return product_list_page_layout(catalog_name)

    # Product detail pages (e.g., /product/Electronics/1)
    elif pathname.startswith('/product/'):
        try:
            catalog_name = pathname.split('/')[2]
            product_id = int(pathname.split('/')[-1])
            return product_detail_layout(catalog_name, product_id)
        except (ValueError, IndexError):
            return html.Div("Invalid Product ID or Catalog")

    # Fallback for unknown pages
    return html.Div([
        html.H1("404 - Page not found"),
        dcc.Link("Go back to main page", href="/")
    ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
