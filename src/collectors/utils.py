import json

from google.cloud import pubsub_v1
from google.auth import jwt


class PubSubHelper:
    def __init__(self, project_id: str, service_account_path: str):
        """
        Initialize PubSub Helper with service account authentication.

        :param service_account_path: Path to the service account JSON key file
        :param project_id: Google Cloud project ID
        """
        try:
            publisher_audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
            credentials = jwt.Credentials.from_service_account_file(
                service_account_path,
                audience=publisher_audience
            )
            credentials_pub = credentials.with_claims(
                audience=publisher_audience)

            # Create publisher and subscriber clients
            self.publisher_client = pubsub_v1.PublisherClient(
                credentials=credentials_pub)
            self.subscriber = pubsub_v1.SubscriberClient(
                credentials=credentials)

            self.project_id = project_id
        except Exception as e:
            raise ValueError(f"Authentication failed: {str(e)}.") from e

    def create_topic(self, topic_name):
        """
        Create a topic if it doesn't already exist.

        :param topic_name: Name of the topic to create
        :return: Full topic path
        """
        topic_path = self.publisher_client.topic_path(self.project_id,
                                                      topic_name)

        # check if topic already exists
        try:
            self.publisher_client.get_topic(request={"topic": topic_path})
            return topic_path
        except Exception:
            # Create topic if it doesn't exist
            try:
                self.publisher_client.create_topic(
                    request={"name": topic_path})
                print(f"Topic {topic_name} created successfully.")
                return topic_path
            except Exception as e:
                raise ValueError(f"Failed to create topic: {str(e)}") from e

    def publish_message(self, topic_name, message, attributes=None):
        """
        Publish a message to a specified topic.

        :param topic_name: Name of the topic to publish to
        :param message: Message to publish (can be string or dict)
        :param attributes: Optional dictionary of message attributes
        :return: Message ID
        """
        # Ensure topic exists
        topic_path = self.create_topic(topic_name)

        try:
            # Convert message to bytes
            if isinstance(message, dict):
                message = json.dumps(message).encode('utf-8')
            elif isinstance(message, str):
                message = message.encode('utf-8')

            # Prepare attributes (optional)
            message_attributes = attributes or {}

            # Publish message
            future = self.publisher_client.publish(
                topic_path, message, **message_attributes)
            message_id = future.result()

            print(f"Message published to {topic_name} with ID: {message_id}")
            return message_id
        except Exception as e:
            raise ValueError(f"Failed to publish message: {str(e)}") from e

    def create_subscription(self, topic_name, subscription_name):
        """
        Create a subscription to a topic.

        :param topic_name: Name of the topic to subscribe to
        :param subscription_name: Name of the subscription
        :return: Full subscription path
        """
        # Ensure topic exists
        topic_path = self.create_topic(topic_name)

        try:
            # Create subscription path
            subscription_path = self.subscriber.subscription_path(
                self.project_id, subscription_name
            )

            # Check if subscription already exists
            try:
                self.subscriber.get_subscription(
                    request={"subscription": subscription_path})
                print(f"Subscription {subscription_name} already exists.")
            except Exception:
                # Create subscription if it doesn't exist
                self.subscriber.create_subscription(
                    request={
                        "name": subscription_path,
                        "topic": topic_path
                    }
                )
                print(
                    f"Subscription {subscription_name} created successfully.")

            return subscription_path
        except Exception as e:
            raise ValueError(f"Failed to create subscription: {str(e)}") from e
