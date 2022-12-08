import psycopg2

mydb = psycopg2.connect(
    host="localhost",
    port=2100,
    database="category_service",
    user="thanhpv",
    password="22121992"
    )


