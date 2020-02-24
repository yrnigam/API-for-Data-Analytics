

#Get JSON data from Google Drive public link
'''import gdown
url = 'https://drive.google.com/a/greendeck.co/uc?id=19r_vn0vuvHpE-rJpFHvXHlMvxa8UOeom&export=download'
output = 'netaporter_gb.json'
gdown.download(url, output, quiet=False)'''


#Ignoring warnings
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

"""#**Importing JSON file into notebook**"""

import pandas as pd
data=pd.read_json("https://****-datasets-2.s3.amazonaws.com/netaporter_gb_similar.json",lines=True,orient='columns')

"""##Creating percentage discount,Brand name,Competiton,Product_id column in dataframe"""

data['discount %']=0
data['brand_name']=0
data['competition']=0
data['p_id']=0
for i in range(0,len(data)):
  regular_price=data['price'][i]['regular_price'].get('value')
  offer_price=data['price'][i]['offer_price'].get('value')
  data['discount %'][i]=((regular_price-offer_price)/regular_price)*100
  data['brand_name'][i]=data['brand'][i].get("name")
  data['competition'][i]=data['website_id'][i].get('$oid')
  data['p_id'][i]=data["_id"][i].get('$oid')

#Filtering out values as per condition
def giveIdEq(d):
  filtered_df = data[data['discount %'] == d] 
  return(filtered_df["_id"])

def giveIdGrater(d):
  filtered_df = data[data['discount %'] > d] 
  return(filtered_df["_id"])

def giveIdSmaller(d):
  filtered_df = data[data['discount %'] < d] 
  return(filtered_df["_id"])

def giveIdByName(d):
  filtered_df = data[data['brand_name'] == d] 
  return(filtered_df["_id"])

def giveIdByCompetition(d):
  filtered_df = data[data['competition'] == d] 
  return(filtered_df["_id"])

#Importing necessary packages to run flask app
from flask import Flask,request,redirect,jsonify,make_response

"""#Task 1 to Task 4"""

app = Flask(__name__)
@app.route("/")
def home():
    return "<h1> Yashraj Nigam</h1>"

                                                                                            #TASK 1
@app.route("/json",methods=["POST"])
def json():
  
  if request.is_json:
    response={}
    req=request.get_json()
    query_type= req.get("query_type")
    if query_type== "discounted_products_list":                                          #Checking the conditions getting from request
      filters= req.get("filters")
      operand1=filters[0].get("operand1")
      operator=filters[0].get("operator")
      operand2=filters[0].get("operand2")
      if operand1== "discount":
        if operator=="==":
          result=list(giveIdEq(operand2))
        elif operator==">":
          result=list(giveIdGrater(operand2))
        elif operator=="<":
          result=list(giveIdSmaller(operand2))
      elif operand1== "brand.name":
        result=list(giveIdByName(operand2))
      elif operand1== "competition":
        result=list(giveIdByCompetition(operand2))
      response = {
            "discounted_products_list": result                                             #Creating response consisting final result of Task 1
            }
                                                                                             #TASK 2
    elif query_type== "discounted_products_count|avg_discount":
      filters= req.get("filters")
      operand2=filters[0].get("operand2")
      filtered_data=data[data['brand_name'] == operand2]
      product_count=int(filtered_data["_id"].count())                                       #Calcualting Product count
      avg_discount=filtered_data["discount %"].mean()                                       #Calcualting Average Discount
      response = {
            "discounted_products_count":product_count,
            "avg_discount":avg_discount                                                      #Creating response consisting final result of Task 2
            }
                                                                                             #TASK 3
    elif query_type=="expensive_list":
      expensive=[]
      for i in range(0,len(data)):                                                            #Getting Competition Basket Price from Similar_product Column
        competition_basket=((((data["similar_products"][0].get("website_results")).get("5d0cc7b68a66a100014acdb0")).get("meta")).get("max_price")).get("basket")
        net_basket=data['price'][0]['regular_price'].get('value')                             #Getting NAP Basket Price from Similar_product Column
        if competition_basket<net_basket:
          expensive.append(data["_id"][i].get("$oid"))
      response = {
            "expensive_list": expensive                                                       #Creating response consisting final result of Task 3
            }
                                                                                              #TASK 4
    elif query_type=="competition_discount_diff_list":
      filters= req.get("filters")
      operand1=filters[0].get("operand1")
      operand2=filters[0].get("operand2")
      operand11=filters[1].get("operand1")
      operand12=filters[1].get("operand2")
      discount_list=[]
      for i in range(0,len(data)):
        if operand1== "discount_diff" and operand11 == "competition" and type(data['similar_products'][i])==dict:
          competition_basket=((((data["similar_products"][i].get("website_results")).get(operand12)).get("meta")).get("max_price")).get("basket")
          net_basket=data['price'][i]['regular_price'].get('value')
          if competition_basket<(int(operand2)/100)*net_basket:
            discount_list.append(data["_id"][i].get("$oid"))
        
      response = {
            "competition_discount_diff_list": discount_list                                       #Creating response consisting final result of Task 4
            }

    else:
      response = {
            "query_type":"WRONG QUERY TYPE"                                                       #Creating response when wrong Query is received
            }
      
    
                                                                                                  #Return JSON Response
    res= make_response(jsonify(response),200)                                                    
    return res

  else:
    res= make_response(jsonify({"message": "No JSON received"}),400)                              ##Creating response when no JSON data is received
    return res

#Run the app
app.run()

