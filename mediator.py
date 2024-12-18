# Write code for the mediator class

import flipkart_wrapper
import amazon_wrapper

class Mediator:
    def __init__(self):
        self.flipkart_wrapper = flipkart_wrapper.FlipkartWrapper()
        self.amazon_wrapper = amazon_wrapper.AmazonWrapper()

    def execute_query(self, query):
        result_flipkart = []
        result_amazon = []
        if "flipkart" in query:
            result_flipkart = self.flipkart_wrapper.execute_query(query)
        if "amazon" in query:
            result_amazon = self.amazon_wrapper.execute_query(query)

        if "flipkart" not in query and "amazon" not in query:
            result_flipkart = self.flipkart_wrapper.execute_query(query)
            result_amazon = self.amazon_wrapper.execute_query(query)

        # add source name to tuples
        for i in range(len(result_flipkart)):
            row = list(result_flipkart[i])
            row.append('Flipkart')
            result_flipkart[i] = tuple(row)

        for i in range(len(result_amazon)):
            row = list(result_amazon[i])
            row.append('Amazon')
            result_amazon[i] = tuple(row)

        # merge
        return result_flipkart + result_amazon
    