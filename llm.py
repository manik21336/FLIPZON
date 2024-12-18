import google.generativeai as genai

class LLMQueryHelper:
    def __init__(self):
        genai.configure(api_key="AIzaSyCawLVKrFTlvvRMRFDY_oics7QW_hf5Q7I")

        model = genai.GenerativeModel("gemini-1.5-flash")
        self.chat = model.start_chat(
            history=[
                {"role": "user", "parts": "Translate the upcoming user query into MySQL, provide only the MySQL query, no other word. Use lower with LIKE keyword with '%' in front and back for better results. The table schema is: source(id, name, category, price, rating, availability). use FROM source, or FROM amazon or FROM flipkart only if query asks for. Limit all queries to 20 rows. Don't use * in aggregate functions"},
            ]
        )

    def translate_query(self, user_query):
        prompt = f"Translate the following user query into SQL:\n\n'{user_query}'"
        response = self.chat.send_message(prompt)
        sql_query = response.text.strip()    
        # remove "```sql " from response
        sql_query = sql_query[7:]
        return sql_query
