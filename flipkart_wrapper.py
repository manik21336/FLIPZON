import mysql.connector
import json

class FlipkartWrapper:
    """
            Description of table categories:
            Column names:
            category_id
            category_1
            category_2
            category_3

            Description of table products:
            Column names:
            product_id
            category_id
            seller_id
            title
            product_rating
            selling_price
            mrp
            description
            highlights
            image_links
            availability

            Description of table sellers:
            Column names:
            seller_id
            seller_name
            seller_rating"""
    
    def __init__(self):
        # self.connection = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="root@mohit",
        #     database="flipkart"
        # )

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@mohit",
            database="flipkart"
        )

        # Create a view to join the tables
        query = """
        CREATE OR REPLACE VIEW flipkart
        AS
        SELECT products.product_id, products.title, products.product_rating, products.selling_price, products.description, products.highlights, products.image_links, categories.category_1, categories.category_2, categories.category_3, products.availability
        FROM products
        JOIN categories
        ON products.category_id = categories.category_id
        """
        
        cursor = self.connection.cursor()
        cursor.execute(query)
        cursor.close()

    def get_products(self):
        query = """
        SELECT title, product_rating, selling_price, description, highlights, image_links, category_1, category_2, category_3
        FROM flipkart order by rand() limit 20
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute_query(self, query):
        # load schema_mapping from schema_mappings.json
        with open("SchemaMatching/schema_matched_output.json", "r") as f:
            schema_mapping = json.load(f)

        # print(schema_mapping)

        query = query.lower()

        # replace * with column names
        query = query.replace("*", ", ".join(schema_mapping["flipkart"]["mappings"].keys()))

        # replace source with flipkart
        query = query.replace("source", "flipkart")

        # query is a dictionary containing the query and the values to be selected
        for attr in schema_mapping["flipkart"]["mappings"]:
            query = query.replace(attr, schema_mapping["flipkart"]["mappings"][attr])

        # add LIMIT 20 if not present to limit the number of rows
        if "limit" not in query:
            query += " LIMIT 20"

        

        print(query)
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        # print(cursor.column_names)
        cursor.close()
        return result
    