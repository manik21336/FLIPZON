### **Workflow Summary: E-commerce Product Aggregator**

Below is the step-by-step workflow, starting from the **front end** (user interaction) to the **query execution and result presentation**:

---

#### **1. User Interaction on Front End (Streamlit)**
- **User Options:**
  - The user selects one of two options:
    1. **Pre-defined Query**: Choose from pre-configured queries (e.g., "Find products under 20,000 INR").
    2. **Custom Query**: Provide a free-text query in natural language (e.g., "Show me all laptops under 50,000 INR with ratings above 4.0").
  - Front-end radio buttons and text inputs guide this choice.

---

#### **2. Pre-defined Query Execution**
- If the user selects a **pre-defined query**:
  1. The query (e.g., `SELECT * FROM GlobalProducts WHERE price < 20000`) is retrieved from a dictionary.
  2. The query is executed directly on the **mediated schema** (`GlobalProducts` view).
  3. Results are fetched and displayed in a table format on the Streamlit interface.

---

#### **3. Custom Query Handling via LLM**
- If the user enters a **custom query**:
  1. The query is passed to a Large Language Model (LLM) API (e.g., OpenAI's GPT-4) for **translation into SQL**.
     - Example: *"Show me all laptops under 50,000 INR with ratings above 4.0"* →  
       SQL: `SELECT * FROM GlobalProducts WHERE category = 'Laptop' AND price < 50000 AND rating > 4.0`
  2. The generated SQL query is presented to the user for confirmation.
  3. Once confirmed, the SQL query is executed on the **mediated schema** (`GlobalProducts`).
  4. Results are fetched and displayed in a table format.

---

#### **4. Wrappers for Data Sources**
- Wrappers are responsible for interfacing with individual data sources (Amazon and Flipkart databases):
  - **AmazonWrapper** and **FlipkartWrapper** fetch data from their respective `Product` and `Category` tables using SQL queries.
  - The wrappers allow users to directly explore raw data for debugging or detailed insights.

---

#### **5. Query Execution on Mediated Schema**
- Queries (from pre-defined or LLM-translated) run on the **GlobalProducts view**, which integrates data from both Amazon and Flipkart:
  - Uses **Global-as-View (GAV)** approach:
    - Maps the `Product` and `Category` tables from Amazon and Flipkart databases into a single virtual table.
    - Combines data using `UNION` and joins.

---

#### **6. Data Federation**
- The **mediator** decomposes the global query into sub-queries for individual sources:
  - Example: For a query on `GlobalProducts`, the system might:
    - Query Amazon for products within a price range.
    - Query Flipkart for products matching the same criteria.
- The **execution engine** retrieves results from the wrappers, federates them, and combines them into a unified result set.

---

#### **7. Result Presentation**
- **Final results** (aggregated and formatted) are displayed to the user in a **Streamlit table**.
- For custom queries, results are rewritten into a user-friendly format if necessary (e.g., grouping by category or sorting).

---

### **System Highlights**

| **Stage**         | **Component**                        | **Purpose**                                                                 |
|--------------------|--------------------------------------|-----------------------------------------------------------------------------|
| **1. Front End**   | Streamlit Interface                 | Provides options for query selection and displays results.                 |
| **2. Query Option**| Pre-defined Query / Custom Query     | Allows user to choose pre-configured queries or create custom queries.     |
| **3. Query Handling**| LLM API (for custom queries)       | Translates natural language queries into SQL for complex or unseen queries.|
| **4. Wrappers**    | AmazonWrapper, FlipkartWrapper      | Fetch data from respective sources.                                        |
| **5. Mediator**    | Mediated Schema (`GlobalProducts`)   | Virtual schema integrating data from both sources.                         |
| **6. Federation**  | Query Decomposition and Execution   | Decomposes queries into sub-queries and federates results.                 |
| **7. Results**     | Streamlit Table                     | Displays final aggregated results to the user.                             |

---

### **Example Workflow**

1. **Input**:  
   - User: "Show me all laptops under 50,000 INR with ratings above 4.0."
   - Query Type: Custom Query.

2. **LLM Translation**:  
   SQL: `SELECT * FROM GlobalProducts WHERE category = 'Laptop' AND price < 50000 AND rating > 4.0`.

3. **Mediator Execution**:  
   - Break down the query:
     - Query Amazon: `SELECT * FROM AmazonProduct WHERE price < 50000 AND rating > 4.0`.
     - Query Flipkart: `SELECT * FROM FlipkartProduct WHERE price < 50000 AND rating > 4.0`.
   - Aggregate results.

4. **Output**:  
   A table showing laptops from both Amazon and Flipkart with prices and ratings.
