# API-for-Data-Analytics-Yoox Group
## The Story
In the fashion industry, there are brands that manufacture and retailers that sell. Each brand usually partners with multiple retailers to sell their inventory. So, it may happen that there is a product that is being sold at multiple retailers. 
The retailers need to set the correct price in order to win over the customer and also take care of the fact that they don't lose out on profits. They have to keep a watch on both their own and their competition's pricing strategy. There is a ton of data that every retailer has to gather to make better pricing decisions. They track the brands, availability and prices among other  for each product.
Net-a-porter (NAP) is a famous retailer in Europe. They have identified five competing retailers and have mapped each product in their own inventory with a similar product on their competition's catalogue. This is where you come in. The team at Net-a-porter has a few queries they want answered. They need a flask app that processes and analyses the data and helps them in making day-to-day pricing decisions.

1. NAP products where discount is greater than n%
They want a list of NAP product ids (field name: _id) where the discount% is greater than n%. Discount is calculated as the difference of regular_price and offer_price. Both the values can be found inside the price dictionary

Request-body 
Test 1: POST { "query_type": "discounted_products_list", "filters": [{ "operand1": "discount", "operator": ">", "operand2": 5 }] }

Test 2: POST { "query_type": "discounted_products_list", "filters": [{ "operand1": "brand.name", "operator": "==", "operand2": "balenciaga" }] }
"query_type": "discounted_products_list" returns a list of _id

"filters" this is how NAP will use the Flask app
"operand1" can be ["discount", "brand.name", "competition"]
"operator" can be [">", "<", "=="]
"operand2" is dependent on "operand1"

Response
{ "discounted_products_list": ["","","",""] } list of _id for NAP products



2. Count of NAP products from a particular brand and its average discount
They want the count of NAP products from a particular brand. They would also like to know the average discount they are giving to their customers. Discount to be calculated as before.

Request-body 
Test 1: POST { "query_type": "discounted_products_count|avg_discount", "filters": [{ "operand1": "brand.name", "operator": "==", "operand2": "gucci" }] }

Test 2: POST { "query_type": "discounted_products_count|avg_discount", "filters": [{ "operand1": "discount", "operator": ">", "operand2": 10 }] }
"query_type": "discounted_products_count" returns an integer
"query_type": "avg_discount" returns a float which is the average discount of the products received after applying the filter
Response
{ "discounted_products_count": 11234, "avg_dicount": 0.06 }

3. NAP products where they are selling at a price higher than any of the competition.

They want to know the list of products where they are being undercut by their competition. You can find the expensive products by comparing basket_price of NAP product with its competition. which you can find inside the price dictionary. As mentioned before, there are some NAP products that may have a field called similar_products which consists of the matching product being sold on their competitor's website. The JSON structure of the matching product is similar to the NAP product. You will find the fields name, brand, price etc. inside the _source field inside website_results field. 

Request-body 
Test 1: POST { "query_type": "expensive_list" }

Test 2: POST { "query_type": "expensive_list", 
"filters": [{ "operand1": "brand.name", "operator": "==", "operand2": "balenciaga" }] }
"query_type": "expensive_list" returns list of _id
Response
{ "expensive_list": ["", "", ""] } list of _id for NAP products


4. NAP products where they are selling at a price n% higher than a competitor X.

NAP monitors five competing websites. They have the following website_ids
WEBSITE_ID_HASH["netaporter_gb"] = "5da6d40110309200045874e6" 
WEBSITE_ID_HASH["farfetch_gb"] = "5d0cc7b68a66a100014acdb0" WEBSITE_ID_HASH["mytheresa_gb"] = "5da94e940ffeca000172b12a" WEBSITE_ID_HASH["matchesfashion_gb"] = "5da94ef80ffeca000172b12c" WEBSITE_ID_HASH["ssense_gb"] = "5da94f270ffeca000172b12e" 
WEBSITE_ID_HASH["selfridges_gb"] = "5da94f4e6d97010001f81d72"
NAP products are matched to their competition using a website_id. You can find the website_id as a key inside the website_results dictionary inside each NAP object. The task is to find the products which are being sold at a price 10% greater than their competitor called Farfetch.
Request-body{ "query_type": "competition_discount_diff_list", 
  "filters": [
    { "operand1": "discount_diff", "operator": ">", "operand2": 10 },
    { "operand1": "competition", "operator": "==", "operand2": "5d0cc7b68a66a100014acdb0"}
      ] } 
"query_type": "competition_discount_diff_list" returns list of _id
"discount_diff" calculates the percentage difference between basket_prices of the NAP product and the competing product
"competition" the id corresponding to the competitor, it is the key inside the "website_results" dictionary
Response
{ "competition_discount_diff_list": ["", "", ""] } list of _id for NAP products
