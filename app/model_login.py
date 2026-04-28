# Login component
from app import mongo

class Login():
    
    @staticmethod
    def authenticate(login_email, login_password):
        try: 
            user = mongo.db.login_data.find_one({"email":login_email, "password": login_password})
            if user:
                return {"success": True, "message": "login successful"}
            else:
                return {"success": False, "message": "invalid credentials"}
        except Exception as e:
            return {"success": False, "message": str(e)}