import json
import logging
from sqlalchemy import create_engine, MetaData, Table, inspect
from rapidfuzz import fuzz
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

GLOBAL_SCHEMA = {
    'product_id': {'type': 'string'},
    'name': {'type': 'string'},
    'price': {'type': 'float'},
    'rating': {'type': 'float'},
    'category': {'type': 'string'},
    'availability': {'type': 'string'}
}

SYNONYMS = {
    'product_id': ['asin', 'sku', 'item_id', 'id', 'prod_id'],
    'price': ['cost', 'amount', 'value', 'selling_cost', 'discounted_price', 'product_price'],
    'name': ['title', 'product_name'],
    'rating': ['review_score', 'avg_rating', 'stars', 'rating_score', 'product_rate', 'product_rating'],
    'category': ['type', 'class', 'group', 'sub_category', 'category_3'],
    'availability': ['stock', 'in_stock', 'availability', 'available']
}

def clean_column_name(name):
    return re.sub(r'\W+', '', name).lower()

def find_best_match(global_attr, source_columns):
    best_match = None
    highest_score = 0
    possible_matches = [global_attr] + SYNONYMS.get(global_attr, [])
    for col in source_columns:
        for candidate in possible_matches:
            score = fuzz.token_set_ratio(candidate, col)
            if score > highest_score:
                highest_score = score
                best_match = col
    return best_match if highest_score >= 70 else None

def process_source(source_config):
    try:
        logging.info(f"Processing source: {source_config['name']}")
        engine = create_engine(source_config['connection_string'])
        inspector = inspect(engine)

        # Get all tables and views from the database
        all_objects = inspector.get_table_names() + inspector.get_view_names()

        object_name = source_config.get('table') or source_config.get('view')
        if object_name not in all_objects:
            logging.error(f"'{object_name}' not found in source '{source_config['name']}'.")
            return None

        metadata = MetaData()
        main_object = Table(object_name, metadata, autoload_with=engine)
        source_columns = {clean_column_name(col.name): col.name for col in main_object.columns}
        mappings = {}

        for global_attr in GLOBAL_SCHEMA.keys():
            match = find_best_match(global_attr, source_columns.keys())
            if match:
                mappings[global_attr] = source_columns[match]
            else:
                logging.warning(f"No match found for '{global_attr}' in source '{source_config['name']}'.")

        logging.info(f"Mappings for source '{source_config['name']}': {mappings}")
        return {
            "name": source_config['name'],
            "connection_string": source_config['connection_string'],
            "object": object_name,
            "mappings": mappings,
            "type": "view" if object_name in inspector.get_view_names() else "table"
        }

    except Exception as e:
        logging.error(f"Error processing source '{source_config['name']}': {e}")
        return None

def generate_schema_mappings(schema_mappings):
    output = {}
    for source in schema_mappings['data_sources']:
        source_output = process_source(source)
        if source_output:
            output[source['name'].lower()] = source_output
    return output

if __name__ == "__main__":
    with open('schema_mappings.json', 'r') as f:
        schema_mappings = json.load(f)

    result = generate_schema_mappings(schema_mappings)

    with open('schema_matched_output.json', 'w') as f:
        json.dump(result, f, indent=2)

    logging.info("Schema matching completed. Output saved to 'schema_matched_output.json'.")
