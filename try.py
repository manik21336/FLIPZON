# write  simple code to test the mediator class

import mediator

m = mediator.Mediator()
result = m.execute_query("SELECT * FROM source WHERE price < 20000 limit 2")
# print("Distinct Categories from Source:")
for row in result:
    print(row)