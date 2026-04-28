# Website Component

from app import mongo

class Website():
    
    @staticmethod
    def insert_webinar(website, webinar):
        
        try:
            mongo.db.website_data.update_one(
                {"website": website},
                {"$addToSet":{"webinar":webinar}}
            )
            
            return {"success": True, "message": "webinar added to website"}
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    
    @staticmethod
    def view_website():
        website_list = []
        
        try:
            website_list_data = list(mongo.db.website_data.find({}).sort({"website":1}))
            for website in website_list_data:
                website_list.append({"website":website.get("website"), "webinar":website.get("webinar")})
        except:
           website_list = []
        
        return website_list
    
    
    @staticmethod
    def insert_website(website):
        
        try:
            mongo.db.website_data.insert_one({
                "website":website, "webinar":[]
            })
            return {"success": True, "message": "website added successfully"}
        
        except Exception as e:
            return {"success": False, "message": str(e)}
