import streamlit as st
import mysql.connector
import pandas as pd

# Import LLMQueryHelper
from llm import LLMQueryHelper

# Import wrappers
from amazon_wrapper import AmazonWrapper
from flipkart_wrapper import FlipkartWrapper
from mediator import Mediator

# Translate the upcoming user query into MySQL, provide only the MySQL query, no other word. Use lower with LIKE keyword with '%' in front and back. Use sub_category instead of category. The table schema is: GlobalProducts(id, name, category, sub_category, price, rating, availability, source). Source can be either 'Amazon' or 'Flipkart')

# Pre Defined Queries
PREDEFINED_QUERIES = {
    "1": {
        "description": "Get products below 20000 price",
        "sql": "SELECT * FROM source WHERE price < 20000"
    },
    "2": {
        "description": "Get top-rated products in Electronics category",
        "sql": "SELECT * FROM source WHERE category LIKE '%Electronics%' ORDER BY rating DESC"
    },
    "3": {
        "description": "Get the top highest-rated products",
        "sql": "SELECT * FROM source ORDER BY rating DESC LIMIT 5"
    },
    "4": {
        "description": "get the number of products per category",
        "sql": "SELECT category, COUNT(category) FROM source GROUP BY category"
    }
}


# Use LLM to translate a natural language query into SQL
def translate_query_with_llm(user_query):
    llm =   LLMQueryHelper()
    return llm.translate_query(user_query)

# Query Execution Logic
def execute_query(query, wrapper=None):
    # execute query using mediator
    mediator = Mediator()
    return mediator.execute_query(query)

# Streamlit Application
def main():
    st.set_page_config(layout="wide")
    st.title("E-commerce Product Aggregator")
    st.write("Unified search across Amazon and Flipkart databases.")

    # Wrapper instances
    amazon_wrapper = AmazonWrapper()
    flipkart_wrapper = FlipkartWrapper()

    # Query selection
    st.write("Choose your query type:")
    query_type = st.radio("Query Type", ["Pre-defined Query", "Custom Query (Handled by LLM)"])
    headers = ["ID", "Name", "Category", "Price", "Rating", "Availability", "Source"]

    if query_type == "Pre-defined Query":
        st.write("Select a pre-defined query:")
        query_choice = st.selectbox(
            "Pre-defined Queries", 
            [f"{k}: {v['description']}" for k, v in PREDEFINED_QUERIES.items()],
            placeholder="Select a query",
        )
        query_key = query_choice.split(":")[0]
        query_info = PREDEFINED_QUERIES[query_key]
        st.success(f"Executing Pre-defined Query: {query_info['description']}")

        try:
            results = execute_query(query_info["sql"])
            if len(results[0]) != 7:
                headers = None
            results = pd.DataFrame(results, columns=headers)
            st.table(results)
        except Exception as e:
            st.error(f"Error executing query: {e}")

    elif query_type == "Custom Query (Handled by LLM)":
        user_query = st.text_input("Enter your query:")
        if user_query:
            # LLM integration
            st.write("Translating query to SQL...")
            sql_query = translate_query_with_llm(user_query)
            st.write(f"Translated SQL Query: {sql_query}")
            
            try:
                results = execute_query(sql_query)
                # also display headers
                if len(results[0]) != 7:
                    headers = None
                results = pd.DataFrame(results, columns=headers)
                st.table(results)
            except Exception as e:
                st.error(f"Error executing query: {e}")

    st.write("Explore data directly from wrappers:")
    if st.button("Show Amazon Data"):
        st.table(amazon_wrapper.get_products())

    if st.button("Show Flipkart Data"):
        st.table(flipkart_wrapper.get_products())

if __name__ == "__main__":
    main()
