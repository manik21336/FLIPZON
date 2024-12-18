-- CREATE VIEW GlobalProducts AS
-- SELECT id, name, category_name AS category, price, rating
-- FROM AmazonProduct JOIN AmazonCategory ON AmazonProduct.category_id = AmazonCategory.id
-- UNION
-- SELECT id, name, category_name AS category, price, rating
-- FROM FlipkartProduct JOIN FlipkartCategory ON FlipkartProduct.category_id = FlipkartCategory.id;

    -- amazon:
    --     Description of table category:
    --     Column names:
    --     id
    --     main_category
    --     sub_category

    --     Description of table product:
    --     Column names:
    --     id
    --     name
    --     image
    --     link
    --     ratings
    --     no_of_ratings
    --     discount_price
    --     actual_price
    --     category_id
    --     availability
    
    -- flipkart:
    --     Description of table categories:
    --         Column names:
    --         category_id
    --         category_1
    --         category_2
    --         category_3

    --         Description of table products:
    --         Column names:
    --         product_id
    --         category_id
    --         seller_id
    --         title
    --         product_rating
    --         selling_price
    --         mrp
    --         description
    --         highlights
    --         image_links
    --         availability

    --         Description of table sellers:
    --         Column names:
    --         seller_id
    --         seller_name
    --         seller_rating

CREATE VIEW GlobalProducts AS
SELECT id, name, sub_category AS category, discount_price AS price, ratings AS rating, availability, 'amazon' AS source
FROM amazon.product JOIN amazon.category ON amazon.product.category_id = amazon.category.id 
UNION
SELECT product_id AS id, title AS name, category_3 AS sub_category, selling_price AS price, product_rating AS rating, availability, 'flipkart' AS source
FROM flipkart.products JOIN flipkart.categories ON flipkart.products.category_id = flipkart.categories.category_id;