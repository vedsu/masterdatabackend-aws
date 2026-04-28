
# Order Component
from app import mongo

class Order:

    
    @staticmethod
    def view_coupon():
        coupon_list = [] 
        try:
            coupon_data = list(mongo.db.coupon_data.find({}))
            for coupon in coupon_data:
                
                    coupon_dict = {
                    "id": coupon.get("id"),
                    "coupon": coupon.get("coupon"),
                    "type": coupon.get("type"),
                    "amount": coupon.get("amount"),
                    "status": coupon.get("status")
                    }
                    coupon_list.append(coupon_dict)
        except Exception as e:
            coupon_list = {"error": str(e)}           
        
        return coupon_list
    
    
    @staticmethod
    def new_coupon(coupon_data):
        try:
            mongo.db.coupon_data.insert_one(coupon_data)
            return ({"success":True, "message":"coupon inserted"}),201
        except Exception as e:
             return ({"success":False, "message":str(e)}),403
            
    @staticmethod
    def update_coupon(c_id,coupon_status):
        try:
            mongo.db.coupon_data.update_one({"id":c_id},{"$set":{"status":coupon_status}})
            return ({"success":True, "message":"coupon status updated"}),201
        except Exception as e:
             return ({"success":False, "message":str(e)}),403
    
    @staticmethod
    def view_order():
        order_list =[]

        try:
            order_data = list(mongo.db.order_data.find({}))
            for order in order_data:
                
                    order_dict = {
                    "id": order.get("id"),
                    "orderdate": order.get("orderdate"),
                    "webinardate": order.get("webinardate"),
                    "topic": order.get("topic"),
                    "session": order.get("session", []),  # Array, defaults to an empty list if not found
                    "customername": order.get("customername"),
                    "customeremail": order.get("customeremail"),
                    "billingemail": order.get("billingemail"),
                    "orderamount": order.get("orderamount"),
                    "paymentstatus": order.get("paymentstatus"),
                    "country": order.get("country"),
                    "state": order.get("state"),
                    "city": order.get("city"),
                    "zipcode": order.get("zipcode"),
                    "address": order.get("address"),
                    "document": order.get("document_ist"),
                    "website": order.get("website")
                }

                    order_list.append(order_dict)
    
        except Exception as e:
            order_list = {"error": str(e)}
        
        return order_list
        

    @staticmethod
    def order_data(o_id):
        order_dict={}
        try:
            order_data = list(mongo.db.order_data.find({"id": o_id}))
            order = order_data[0]
            order_dict = {
                "id": order.get("id"),
                "orderdate": order.get("orderdate"),
                "webinardate": order.get("webinardate"),
                "topic": order.get("topic"),
                "session": order.get("session"), # Array
                "customername": order.get("customerName"),
                "customeremail": order.get("customerEmail"),
                "billingemail": order.get("billingEmail"),
                "orderamount": order.get("orderamount"),
                "paymentstatus": order.get("paymentstatus"),
                "country" : order.get("country"),
                "state" : order.get("state"),
                "city" : order.get("city"),
                "zipcode" : order.get("zipcode"),
                "address": order.get("address"),
                "document": order.get("document_ist"),
                "website" : order.get("website")

            }

        except Exception as e:
            order_dict = {}
            
        return order_dict
        
