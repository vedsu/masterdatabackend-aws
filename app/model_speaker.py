# Speaker Component

from app import mongo
class Speaker():

    @staticmethod
    def view_speaker():
        
        # Speaker name list for drop down menu
        speaker_list =[]
         
        try:
            speaker_data = list(mongo.db.speaker_data.find({"status":"Active"}).sort({"name":1}))
            for speaker in speaker_data:
                speaker_list.append(speaker.get("name"))
        
        except Exception as e:
            speaker_list = []
        
        return speaker_list
    
    @staticmethod
    def list_speaker():
        
        # Speaker name list for drop down menu
        speaker_list = []
         
        try:
            speaker_data = list(mongo.db.speaker_data.find({}).sort({"name":1}))
            for speaker in speaker_data:
                
                speaker_dict ={

                "id":speaker.get("id"),
                "name":speaker.get("name"),
                "email":speaker.get("email"),
                "contact": speaker.get("contact"),
                "industry":speaker.get("industry"),
                "status":speaker.get("status"),
                "bio":speaker.get("bio"),
                }
                speaker_list.append(speaker_dict)
        
        except Exception as e:
            speaker_list = []
        
        return speaker_list
        
    @staticmethod
    def create_speaker(speaker_data):

        try:
            mongo.db.speaker_data.insert_one(speaker_data)
            return {"success": True, "message": "Speaker created successfully"}
        
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    @staticmethod
    def data_speaker(s_id):
        
        speaker_info = None  
        try:
            speaker_data = list(mongo.db.speaker_data.find({"id":s_id}))
            speaker = speaker_data[0]
            speaker_dict={
                "id": speaker.get("id"),
                "name": speaker.get("name"),
                "email":speaker.get("email"),
                "industry": speaker.get("industry"),
                "status": speaker.get("status"),
                "bio": speaker.get("bio"),
                "contact" :speaker.get("contact"),
                "photo": speaker.get("photo"),
                "history": speaker.get("history")
            }
            
            speaker_info = speaker_dict
        except Exception as e:
            speaker_info = None 
            
        
        return speaker_info
    

    @staticmethod
    def edit_speaker(s_id, speaker_status):

        try:
            mongo.db.speaker_data.update_one({"id":s_id}, {"$set":{"status": speaker_status}})
            return {"success": True, "message":"status update successfull"}
        
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    @staticmethod
    def update_speaker(s_id, speaker_data):

        try:
            mongo.db.speaker_data.update_one({"id":s_id}, {"$set": speaker_data})
            return {"success": True, "message": "speaker update successfull"}
        
        except Exception as e:
            return {"success":False, "message": str(e)}
        
    @staticmethod
    def delete_speaker(s_id):
        
        try:
            mongo.db.speaker_data.delete_one({"id":s_id})
            return {"success": True, "message": "speaker deletion successful"}
        
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    @staticmethod
    def update_history(s_name, webinar_topic):

        try:
            result= mongo.db.speaker_data.update_one(
               {"name": s_name},{"$addToSet":{"history":webinar_topic}}
           )
            return {"success":True, "message":result.modified_count}
        except Exception as e:
            return {"success":False, "message":str(e)}
