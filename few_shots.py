few_shots = [
    {'Question': "How many t-shirts do we have left for Nike in XS size and white color?",
     'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
     'SQLResult': "Result of the SQL query",
     'Answer': "12 Tshirts"},
    
    {'Question': "What is the total number of t-shirts available in Blue color?",
     'SQLQuery': "SELECT SUM(stock_quantity) FROM t_shirts WHERE color = 'Blue'",
     'SQLResult': "Result of the SQL query",
     'Answer': "868 Tshirts"},

    {'Question': "How much is the total price of the inventory for all S-size t-shirts?",
     'SQLQuery': "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S'",
     'SQLResult': "Result of the SQL query",
     'Answer': "$22906"},

    {'Question': "If we have to sell all the Levi's T-shirts today with discounts applied, how much revenue will our store generate (post discounts)?",
     'SQLQuery': """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue 
                    from (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts 
                    where brand = 'Levi' group by t_shirt_id) a 
                    left join discounts on a.t_shirt_id = discounts.t_shirt_id""",
     'SQLResult': "Result of the SQL query",
     'Answer': "$33017.15"},

    {'Question': "If we have to sell all the Levi's T-shirts today, how much revenue will our store generate without discounts?",
     'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
     'SQLResult': "Result of the SQL query",
     'Answer': "$35918"},

    {'Question': "How many white color Levi's shirts do I have?",
     'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White'",
     'SQLResult': "Result of the SQL query",
     'Answer': "325 Tshirts"},

    {'Question': "How much sales amount will be generated if we sell all large size Nike t-shirts today after discounts?",
     'SQLQuery': """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue 
                    from (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts 
                    where brand = 'Nike' and size='L' group by t_shirt_id) a 
                    left join discounts on a.t_shirt_id = discounts.t_shirt_id""",
     'SQLResult': "Result of the SQL query",
     'Answer': "$855.0"},

    {'Question': "How many red color t-shirts are there for Adidas in stock?",
     'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Adidas' AND color = 'Red'",
     'SQLResult': "Result of the SQL query",
     'Answer': "294 Tshirts"},

    {'Question': "What is the total value of all XS-sized Van Huesen t-shirts in stock?",
     'SQLQuery': "SELECT sum(price * stock_quantity) FROM t_shirts WHERE brand = 'Van Huesen' AND size = 'XS'",
     'SQLResult': "Result of the SQL query",
     'Answer': "$8769"},

    {'Question': "How many total t-shirts do we have in stock across all brands and sizes?",
     'SQLQuery': "SELECT sum(stock_quantity) FROM t_shirts",
     'SQLResult': "Result of the SQL query",
     'Answer': "3489 Tshirts"},

    {'Question': "What is the average price of all t-shirts in stock for Adidas?",
     'SQLQuery': "SELECT AVG(price) FROM t_shirts WHERE brand = 'Adidas'",
     'SQLResult': "Result of the SQL query",
     'Answer': "$31.00"},

    {'Question': "How much discount will be applied to Van Huesen t-shirts in M size?",
     'SQLQuery': """SELECT COALESCE(discounts.pct_discount, 0) as discount_pct 
                    FROM t_shirts 
                    LEFT JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id 
                    WHERE brand = 'Van Huesen' AND size = 'M'""",
     'SQLResult': "Result of the SQL query",
     'Answer': "35%"},

    {'Question': "How much revenue will we generate if we sell all t-shirts today at full price?",
     'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts",
     'SQLResult': "Result of the SQL query",
     'Answer': "$111808"},

    {'Question': "How many total t-shirts in XL size are left in stock across all brands?",
     'SQLQuery': "SELECT SUM(stock_quantity) FROM t_shirts WHERE size = 'XL'",
     'SQLResult': "Result of the SQL query",
     'Answer': "441 Tshirts"},

    {'Question': "What is the total inventory value of Van Huesen t-shirts in L size?",
     'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Van Huesen' AND size = 'L'",
     'SQLResult': "Result of the SQL query",
     'Answer': "$8210"}
]


mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.In final Answer you should not give the sql query user need a final answer it may be a number or what user asks.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves "today". 

Use the following format:

Question: Question here
SQLQuery: Query to run with no pre-amble
SQLResult: Result of the SQLQuery
Answer: Final answer here which is result of sql query

No pre-amble.
"""