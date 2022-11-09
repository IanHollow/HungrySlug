import datetime as dt
from operator import itemgetter
import os

from firebase_admin import credentials, initialize_app, firestore

CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(
    __file__), "", "../google-credentials.json")


def generate_timestamp():
    return dt.datetime.now(tz=dt.timezone.utc)


class FirebaseService:
    def __init__(self):
        self.creds = credentials.Certificate(CREDENTIALS_FILEPATH)
        self.app = initialize_app(self.creds)
        self.db = firestore.client()

    #
    # PRODUCTS
    #

    def fetch_products(self):
        products_ref = self.db.collection("products")
        products = [doc.to_dict() for doc in products_ref.stream()]
        return products

    #
    # ORDERS
    #

    @property
    def orders_ref(self):
        return self.db.collection("orders")

    def create_order(self, user_email, product_info):
        """
        Params :
            user_email (str)
            product_info (dict) with name, description, price, and url
        """
        new_order_ref = self.orders_ref.document()  # new document with auto-generated id
        new_order = {
            "user_email": user_email,
            "product_info": product_info,
            "order_at": generate_timestamp()
        }
        results = new_order_ref.set(new_order)
        # print(results) #> {update_time: {seconds: 1648419942, nanos: 106452000}}
        return new_order, results

    def fetch_orders(self):
        orders = [doc.to_dict() for doc in self.orders_ref.stream()]
        return orders

    def fetch_user_orders(self, user_email):
        query_ref = self.orders_ref.where("user_email", "==", user_email)

        # sorting requires configuration of a composite index on the "orders" collection,
        # ... so to keep it simple for students, we'll sort manually (see below)
        # query_ref = query_ref.order_by("order_at", direction=firestore.Query.DESCENDING) #.limit_to_last(20)

        # let's return the dictionaries, so these are serializable (and can be stored in the session)
        docs = list(query_ref.stream())
        orders = []
        for doc in docs:
            order = doc.to_dict()
            order["id"] = doc.id
            # breakpoint()
            # order["order_at"] = order["order_at"].strftime("%Y-%m-%d %H:%M")
            orders.append(order)
        # sorting so latest order is first
        orders = sorted(orders, key=itemgetter("order_at"), reverse=True)
        return orders
