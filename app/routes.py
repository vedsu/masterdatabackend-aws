# Routing

from flask import request, jsonify
from app import app
from app import mongo
from app.model_login import Login
from app.model_webinar import Webinar
from app.model_speaker import Speaker
from app.model_order import Order
from app.model_category import Category
from app.model_website import Website
from app.model_newsletter import Newsletter

import string
import random
from bson import Binary
import re
import io
import base64
from PIL import Image
import os
from datetime import datetime
from app import s3_client
import pandas as pd
from io import StringIO

@app.route('/health', methods= ['GET'])
def home():
    
        return {"success":"True",
                "message":"AWS Running"}
    
@app.route('/', methods =['POST'])
def master_login():
    if request.method == 'POST':
        login_email = request.json.get("Email")
        login_password = request.json.get("Password")

        response_login = Login.authenticate(login_email, login_password)
        return response_login
    

@app.route('/coupon_panel', methods= ['GET'])
def view_coupon():
    coupon_list = Order.view_coupon()
    if request.method =='GET':
       
        return jsonify(coupon_list),200
      
@app.route('/coupon_panel/<c_id>', methods= ['GET','PUT','POST','DELETE'])
def update_coupon_panel(c_id):    
    
    if request.method  =='POST':
        coupon_status = request.json.get("status")
        response = Order.update_coupon(c_id, coupon_status)
        return response
        
       


@app.route('/coupon_panel/create_coupon', methods= ['POST'])
def create_coupon():
    coupon_list = Order.view_coupon()
    id = str(len(list(coupon_list)))
    N = 3
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    c_id = res+"_"+id
    if request.method == "POST":
        coupon = request.json.get("coupon")
        type = request.json.get("type")
        amount = request.json.get("amount")
        status = "Active"
        coupon_data = {
            "id":c_id, 
            "coupon":coupon,
            "type":type,
            "amount":amount,
            "status":status
        }
        response = Order.new_coupon(coupon_data)
        return response


@app.route('/webinar_panel', methods = ['GET'])
def webinar_panel():
    
    webinar_list = Webinar.view_webinar()
    speaker_list = Speaker.view_speaker()
    website_list = Website.view_website()
    # industry_list = Category.industry()
        
    if request.method == 'GET':
       
        return jsonify(webinar_list, speaker_list, website_list),200
    
def process_url(topic):

    # Convert the sentence to lowercase
    sentence = topic.lower()
    
    # Remove special characters using regex
    sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence)
    
    # Replace spaces between words with dashes
    sentence = sentence.replace(' ', '-')
    
    return sentence


    

@app.route('/webinar_panel/create_webinar', methods= ['POST'])
def create_webinar():
    webinar_list = Webinar.view_webinar()
    id = str(len(list(webinar_list)))
    N = 3
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    w_id = res+"_"+id
    if request.method in ['POST']:
        webinar_topic = request.json.get("topic")
        speaker = request.json.get("speaker")
        date_time = request.json.get("date")
        website = request.json.get("website")
        
        # Parse the datetime string
        dt = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        # Extract the date and time as separate strings
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S.%f")[:-10]  # Trim the last three digits of microseconds to match milliseconds
        
        webinar_data ={
        
        "id": w_id,
        
        "topic":webinar_topic,
        "speaker":speaker,
        "industry":request.json.get("industry"),
        "date_time":dt,
        "time":time_str,
        "date":date_str,
        "timeZone":request.json.get("timeZone"),
        "duration":request.json.get("duration"),
        "category":request.json.get("category"),
        
        "sessionLive":request.json.get("sessionLive"),
        "priceLive":request.json.get("priceLive"),
        "urlLive":request.json.get("urlLive"),
        
        "sessionRecording":request.json.get("sessionRecording"),
        "priceRecording":request.json.get("priceRecording"),
        "urlRecording":request.json.get("urlRecording"),

        "sessionDigitalDownload":request.json.get("sessionDigitalDownload"),
        "priceDigitalDownload":request.json.get("priceDigitalDownload"),
        "urlDigitalDownload":request.json.get("urlDigitalDownload"),
        
        "sessionTranscript":request.json.get("sessionTranscript"),
        "priceTranscript":request.json.get("priceTranscript"),
        "urlTranscript":request.json.get("urlTranscript"),

        "status":"Active",
        "webinar_url": process_url(webinar_topic),
        "website": website,
        "description":request.json.get("description"),
        
        }
        
        response_create_webinar = Webinar.create_webinar(webinar_data)
        respone_history_speaker = Speaker.update_history(speaker,webinar_topic)
        response = Website.insert_webinar(website, webinar_topic)
        if response.get("success") == True:
            return jsonify(response_create_webinar,respone_history_speaker,response),201
        else:
            return response, 403
            
@app.route('/webinar_panel/<w_id>', methods= ['GET','PUT','POST','DELETE'])
def update_webinar_panel(w_id):    
    
    
    webinar_data = Webinar.data_webinar(w_id)
    
    if request.method  == 'GET':
        
        return webinar_data,200
       
    elif request.method  =='POST':
        
        webinar_status = request.json.get("status")
        
        response = Webinar.edit_webinar(w_id, webinar_status)
        
        if response.get("success") == True:
            return response, 201
        
        else:
            return response,304
                
        
        
    elif request.method =='PUT':
        
        topic = request.json.get("topic")
        speaker = request.json.get("speaker")
        website = request.json.get("website")
        
        date_time = request.json.get("date")
        # Parse the datetime string
        dt = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        # Extract the date and time as separate strings
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S.%f")[:-10]  # Trim the last three digits of microseconds to match milliseconds
        
        webinar_data = {
        "id":w_id,
        
        "topic":topic,
        "industry":request.json.get("industry"),
        "speaker":speaker,
        "date_time":dt,
        "date":date_str,
        "time":time_str,
        "timeZone":request.json.get("timeZone"),
        "duration":request.json.get("duration"),
        "category":request.json.get("category"),
        
        "sessionLive":request.json.get("sessionLive"),
        "priceLive":request.json.get("priceLive"),
        "urlLive":request.json.get("urlLive"),
        
        "sessionRecording":request.json.get("sessionRecording"),
        "priceRecording":request.json.get("priceRecording"),
        "urlRecording":request.json.get("urlRecording"),

        "sessionDigitalDownload":request.json.get("sessionDigitalDownload"),
        "priceDigitalDownload":request.json.get("priceDigitalDownload"),
        "urlDigitalDownload":request.json.get("urlDigitalDownload"),
        
        "sessionTranscript":request.json.get("sessionTranscript"),
        "priceTranscript":request.json.get("priceTranscript"),
        "urlTranscript":request.json.get("urlTranscript"),

        "status":request.json.get("status"),
        "webinar_url": process_url(topic),
        "website": website,
        "description":request.json.get("description"),
        }
        
        Speaker.update_history(speaker, topic)
        Website.insert_webinar(website, topic)
        
        response = Webinar.update_webinar(w_id, webinar_data)
        if response.get("success") == True:
            return response,200
    
        else:
            return response,304
        
    elif request.method =='DELETE':
         
        response = Webinar.delete_webinar(w_id)
        
        if response.get("success") == True:
            
            return response, 202
        else:
            return response, 204

@app.route('/speaker_panel', methods = ['GET'])
def speaker_panel():
    
    speaker_list = Speaker.list_speaker()
    if request.method == 'GET':
        return jsonify(speaker_list),200
    

@app.route('/speaker_panel/create_speaker', methods = ['POST'])
def create_speaker():
    
    speaker_list = Speaker.view_speaker()
    
    id = str(len(speaker_list))
    
    if request.method == 'POST':
         
        speaker_name = request.form.get("name")
        # initializing size of string
        N = 3
        
        # using random.choices()
        # generating random strings
        res = ''.join(random.choices(string.ascii_uppercase +
                                    string.digits, k=N))
        s_id = res+"_"+id
        
        bucket_name = "webinarprof"
        object_key = ''.join(speaker_name.split(" "))+"_"+res
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/speaker/{object_key}.jpeg"
        image = request.files.get("photo")
        s3_client.put_object(
        Body=image, 
        Bucket=bucket_name, 
        Key=f'speaker/{object_key}.jpeg'
        )
        speaker_data ={
            "id": s_id,
            "name" :speaker_name,
            "email": request.form.get("email"),
            "industry": request.form.get("industry"),
            "contact" : request.form.get("contact"),
            "status":"Active",
            "bio": request.form.get("bio"),
            "history": [],
            "photo": s3_url,

        }
        
        response = Speaker.create_speaker(speaker_data)
        if response.get("success") == True:
            return response,201
        else:
            return response,403

@app.route('/speaker_panel/<s_id>', methods =['GET','PUT', 'POST', 'DELETE'])
def update_speaker_panel(s_id):
    
    
    
    if request.method == 'GET':
        speaker_data = Speaker.data_speaker(s_id)
       
        return jsonify(speaker_data),200        
            
    
    elif request.method == 'POST':

        speaker_status = request.json.get("status")
        
        response = Speaker.edit_speaker(s_id, speaker_status)
        
        if response.get("success") == True:
            return response, 201
        
        else:
            return response,304
        
    
    elif request.method == 'PUT':
        try:
            s3_url = request.form.get("photo")
            speaker_name = request.form.get("name")
            # initializing size of string
            """N = 3
            
            # using random.choices()
            # generating random strings
            res = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=N))
            bucket_name = "webinarprof"
            object_key = ''.join(speaker_name.split(" "))+"_"+res
            s3_url = f"https://{bucket_name}.s3.amazonaws.com/speaker/{object_key}.jpeg"
            s3_client.put_object(
            Body=image, 
            Bucket=bucket_name, 
            Key=f'speaker/{object_key}.jpeg')"""
            
            speaker_dict = {
                "id": s_id,
                "name": speaker_name,
                "email": request.form.get("email"),
                "contact" : request.form.get("contact"),
                "industry": request.form.get("industry"),
                "status": "Active",
                "bio": request.form.get("bio"),
                "photo": s3_url,
                
            }
            
            response= Speaker.update_speaker(s_id, speaker_dict)
            if response.get("success") == True:
                return response,200
        
            else:
                return response,500

        except Exception as e:
            return {"success": False, "message": str(e)}, 500
      
        
    elif request.method == 'DELETE':

        response= Speaker.delete_speaker(s_id)
    
        if response.get("success") == True:
            
            return response, 202
        else:
            return response, 400


@app.route('/order_panel', methods =['GET'])
def order_panel():
    
    order_list = Order.view_order()
    if request.method == 'GET':
        
        return jsonify(order_list), 200
    
@app.route('/order_panel/<int:o_id>', methods = ['GET'])
def order_detail(o_id):
    
    order_data = Order.order_data(o_id)
    
    if request.method == 'GET':
           return order_data,200
    

@app.route('/category', methods = ['GET', 'POST'])
def category():
    
    if request.method == 'GET':
        
        industry_data =  Category.industry()
        return jsonify(industry_data),200
        
    elif request.method == 'POST':
        industry_selected = request.json.get("industry")
        category_added = request.json.get("category")
        
        response = Category.categories(industry_selected,category_added)
        if response.get("success") == True:
            return response,201
        else:
            return response,403
        


@app.route('/newsletter_panel', methods = ['GET'])
def view_newsletter():
    if request.method == 'GET':
        response = Newsletter.list_newsletter()
        return response,200
#masterdata backend
@app.route('/newsletter_panel/<n_id>', methods = ['GET','POST'])
def update_newsletter(n_id):
   
        
    if request.method == 'POST':
        newsletter_status = request.json.get("status")
        response = Newsletter.edit_newsletter(n_id, newsletter_status)
        if response.get("success") == True:
            return response.get("message"),201
        else:
            return response.get("message"),304
# newsletter section -> updating for masterdata backend
# masterdatabackend

@app.route('/newsletter_panel/create_newsletter', methods = ['POST'])
def create_newsletter():
    newsletters = Newsletter.count_newsletter() # edit this function to count_newsletter
    id = str(len(newsletters)+1)

    if request.method == 'POST':
        newsletter_topic = request.form.get("topic")
        category = request.form.get("category")
        website = request.form.get("website")
        description = request.form.get("description")
        price = request.form.get("price")
        document = request.form.get("document")
        published_date = request.form.get("published_date")
        # Remove the `GMT` and timezone name from the string
        date_str = published_date.replace("GMT", "").split(" (")[0]
        # Parse the date string to datetime object
        date_obj = datetime.strptime(date_str, '%a %b %d %Y %H:%M:%S %z')
        
        # Convert to desired format for database (YYYY-MM-DD HH:MM:SS)
        formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        # Convert to ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sss+00:00)
        iso_format_date = date_obj.isoformat()
        # # Parse the date string to datetime object
        # date_obj = datetime.strptime(published_date, '%a %b %d %Y %H:%M:%S GMT%z (%Z)')
        # # dt = datetime.strptime(published_date,"%Y-%m-%dT%H:%M:%S.%fZ" )
        # # Convert to desired format for database (YYYY-MM-DD HH:MM:SS)
        # formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        # # date_str = dt.strftime("%Y-%m-%d")

        thumbnail = request.files.get("thumbnail")
        

        N=3
        res = ''.join(random.choices(string.ascii_uppercase+string.digits, k=N))
        n_id = res+"_"+id
        bucket_name = "webinarprof"
        object_key = ''.join(newsletter_topic.split(" "))+n_id
        # object_key_document = ''.join(newsletter_topic.split(" "))+"_"+id
        try:
            s3_client.put_object(
            Body=thumbnail, 
            Bucket=bucket_name, 
            Key=f'newsletter/{object_key}.jpeg'
            )
            s3_url_thumbnail = f"https://{bucket_name}.s3.amazonaws.com/newsletter/{object_key}.jpeg"
           
            
        except:
            s3_url_thumbnail = None
            
        
        newsletter_data = {
            "id":n_id,
            "topic": newsletter_topic,
            "category": category,
            "description": description,
            "website": website,
            "price": price,
            "status": "Active",
            "thumbnail":s3_url_thumbnail,
            "document":document,
            "published_date":iso_format_date,

        }

        response = Newsletter.create_newsletter(newsletter_data)
        if response.get("success") == True:
            return response,201
        else:
            return response,400

#text editor dummy model
@app.route("/submit", methods=["POST"])
def submit_entry():
    data = request.json
    # collection.insert_one(data)
    mongo.db.texteditor.insert_one(data)
    return jsonify({"message": "Data saved successfully!"}), 201

@app.route("/get_entries", methods=["GET"])
def get_entries():
    entries = list(mongo.db.texteditor.find({}, {"_id":0}))
    # entries = list(collection.find({}, {"_id": 0}))
    return jsonify(entries)


#upcoming webinars
@app.route('/g_csv', methods = ['GET'])
def generate_csv():
    s3_url = ""
    if request.method == 'GET':
        order_list = Order.view_order()
        # Convert to DataFrame
        df = pd.DataFrame(order_list)
        
        # Save DataFrame to CSV in memory
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        # Get the current date and time
        current_datetime = datetime.now()
        file_name = current_datetime
        bucket_name = "webinarprof"
        try:
            s3_client.put_object(
            Body=csv_buffer.getvalue(), 
            Bucket=bucket_name, 
            Key=f'misc/{file_name}.csv'
            )
            s3_url = f"https://{bucket_name}.s3.amazonaws.com/misc/{file_name}.csv"
           
            
        except Exception as e:
            s3_url = str(e)
        
        # s3_url = "https://webinarprofs.s3.amazonaws.com/websiteorder/070125_HCP_E67MTADQ.pdf"
        return jsonify(s3_url), 200

#upcoming webinars
@app.route('/ucw', methods = ['GET'])
def upcoming_webinarlist():
    if request.method == 'GET':
        ucw_list = Webinar.upcoming_webinar()
        return jsonify(ucw_list), 200

@app.route('/website_panel', methods= ['GET', 'POST'])
def website_utility():
    
    if request.method == 'GET':
        website_list = Website.view_website()
        return jsonify(website_list),200
    
    elif request.method == 'POST':
        
        website=request.json.get("website")
        response = Website.insert_website(website)
        if response.get("success") == True:
            return response,201
        else:
            return response,403
