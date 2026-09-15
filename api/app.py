from flask import Flask, request
import os
import psycopg

app = Flask(__name__)

@app.get("/")
def home():
    return {"service": "api", "status": "running"}
    
@app.get("/db-check")
def db_check():
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    cur = conn.cursor()

    cur.execute("SELECT 1;")

    result = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "database": "connected",
        "result": result[0]
    }

@app.get("/products")
def get_products():
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, price FROM products ORDER BY id;"
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    products = []

    for row in rows:
        products.append({
            "id": row[0],
            "name": row[1],
            "price": row[2]
        })

    return {"products": products}  
@app.post("/products")
def create_product():
    data = request.get_json()

    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    cur = conn.cursor()

    cur.execute(
        "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id;",
        (data["name"], data["price"])
    )

    new_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return {
        "id": new_id,
        "name": data["name"],
        "price": data["price"]
    }    
@app.patch("/products/<int:product_id>")
def update_product(product_id):
    data = request.get_json()

    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    cur = conn.cursor()

    cur.execute(
        "UPDATE products SET price = %s WHERE id = %s RETURNING id, name, price;",
        (data["price"], product_id)
    )

    row = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    if row is None:
        return {"error": "product not found"}, 404

    return {
        "id": row[0],
        "name": row[1],
        "price": row[2]
    }    
@app.delete("/products/<int:product_id>")
def delete_product(product_id):
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM products WHERE id = %s RETURNING id, name, price;",
        (product_id,)
    )

    row = cur.fetchone()

    conn.commit()

    cur.close()
    conn.close()

    if row is None:
        return {"error": "product not found"}, 404

    return {
        "deleted": {
            "id": row[0],
            "name": row[1],
            "price": row[2]
        }
    }    

app.run(host="0.0.0.0", port=5000)