import mysql.connector
import json

class AmazonWrapper:
    """
        Description of table category:
        Column names:
        id
        main_category
        sub_category

        Description of table product:
        Column names:
        id
        name
        image
        link
        ratings
        no_of_ratings
        discount_price
        actual_price
        category_id
        availability
    """
    
    def __init__(self):
        # self.connection = mysql.connector.connect(
        #     host="192.168.48.243",
        #     user="root",
        #     password="root@manik",
        #     database="amazon"
        # )

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@mohit",
            database="amazon"
        )

        # Create a view to join the tables
        query = """
        CREATE OR REPLACE VIEW amazon
        AS
        SELECT product.id, product.name, product.ratings, product.no_of_ratings, product.discount_price, product.actual_price, product.availability, category.main_category, category.sub_category
        FROM product
        JOIN category
        ON product.category_id = category.id
        """
        
        cursor = self.connection.cursor()
        cursor.execute(query)
        cursor.close()

    def get_products(self):
        query = """
        SELECT name, ratings, no_of_ratings, discount_price, actual_price, availability, main_category, sub_category
        FROM amazon order by rand() limit 20
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        # print(cursor.column_names)
        cursor.close()
        return result

    def execute_query(self, query):
        # load schema_mapping from schema_mappings.json
        with open("SchemaMatching/schema_matched_output.json", "r") as f:
            schema_mapping = json.load(f)

        # print(schema_mapping)

        query = query.lower()

        # replace * with column names
        query = query.replace("*", ", ".join(schema_mapping["amazon"]["mappings"].keys()))
        
        # replace source with amazon
        query = query.replace("source", "amazon")

        # query is a dictionary containing the query and the values to be selected
        for attr in schema_mapping["amazon"]["mappings"]:
            query = query.replace(attr, schema_mapping["amazon"]["mappings"][attr])

        # add LIMIT 20 if not present to limit the number of rows
        if "limit" not in query:
            query += " LIMIT 20"

        print(query)
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    