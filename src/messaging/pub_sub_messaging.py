# import json
# import os

# from google.cloud import pubsub_v1
# from google.auth import jwt
# from dotenv import load_dotenv

# load_dotenv('.env')  # for local dev

# SERVICE_ACCOUNT_FILE_PATH = os.getenv(
#     "SERVICE_ACCOUNT_FILE_PATH", "Variable Not Set")


# class PubSub:
#     def init(self, SERVICE_ACCOUNT_FILE_PATH):
#         """Create the topic if it doesn't exist"""
#         self.SERVICE_ACCOUNT_FILE_PATH = SERVICE_ACCOUNT_FILE_PATH
#         pass

#     def get_client(self) -> pubsub_v1.PublisherClient:
#         """Initialize and return a client"""
#         with open(self.SERVICE_ACCOUNT_FILE_PATH, 'r', encoding='utf-8') as f:
#             service_account_info = json.load(f)

#         publisher_audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
#         credentials = jwt.Credentials.from_service_account_info(
#             service_account_info, audience=publisher_audience
#         )
#         credentials_pub = credentials.with_claims(audience=publisher_audience)
#         publisher_client = pubsub_v1.PublisherClient(
#             credentials=credentials_pub)

#         return publisher_client
