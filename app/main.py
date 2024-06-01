import uvicorn
from fastapi import FastAPI

title = 'My first App'

app = FastAPI(title=title)

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]


@app.get('/product/{product_id}')
def read_users(product_id: int):
    for product in sample_products:
        if product['product_id'] == product_id:
            return product
    return {"message": "Product not found"}


@app.get('/products/search')
def find_products(keyword: str, category: str = None, limit: int = 10):
    products_result = []
    for product in sample_products:
        if category is None or product['category'] == category:
            if keyword.lower() in product['name'].lower():
                products_result.append(product)
    return products_result[:limit]


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True, workers=3)
