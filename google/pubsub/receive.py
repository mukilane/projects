import argparse
import time
from google.cloud import pubsub_v1

def receive_messages(project, subscription_name):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription_name)

    def callback(message):
        print('Received message: {}'.format(message))
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)
    print('Listening on {}'.format(subscription_path))

    # Continue listening until user exits
    while True:
        time.sleep(100)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project", help="Google Cloud Project ID")
    parser.add_argument("-s", "--subscription", help="Subscription name")
    args = parser.parse_args()
    if args.project and args.subscription:
        receive_messages(args.project, args.subscription)
    else:
        print("Parameters missing")


