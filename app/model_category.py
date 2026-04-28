# Category Component

from app import mongo

class Category():

    @staticmethod
    def industry():
        industry_list = []

        try:
            industry_data = list(mongo.db.category_data.find({}))
            for industry in industry_data:
                industry_dict = {
                    "industry": industry["industry"],
                    "categories": industry["categories"]
                }
                industry_list.append(industry_dict)
                
        
        
        except Exception as e:
            industry_list = []
        
        return industry_list
    
    @staticmethod
    def categories(industry, category):

        try:
            mongo.db.category_data.update_one(
                {"industry":industry},
                {"$addToSet": {"categories": category}})
            return {"success":True, "message": "category added successfully"}
        
        except Exception as e:
            return {"success": False, "message":str(e)}