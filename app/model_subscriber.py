# Subscriber Component

from app import mongo

class Subscriber():

    @staticmethod
    def list_subscribers():
        subscriber_list = []

        try:
            subscriber_data = list(mongo.db.subscriber_list.find({}).sort({"date":-1}))
            for subscriber in subscriber_data:
                subscriber_dict = {
                    "id": str(subscriber.get("_id")),
                    "email": subscriber.get("email"),
                    "name": subscriber.get("name"),
                    "phone": subscriber.get("phone"),
                    "jobtitle": subscriber.get("jobtitle"),
                    "country": subscriber.get("country"),
                    "subscription_type": subscriber.get("subscription_type"),
                    "type": subscriber.get("type"),
                    "date": subscriber.get("date"),
                    "website": subscriber.get("website"),
                }
                subscriber_list.append(subscriber_dict)

        except Exception as e:
            subscriber_list = []

        return subscriber_list
