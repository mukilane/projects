import argparse
from google.cloud import pubsub_v1

def publish_message(project, topic_name, data):

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    data = data.encode('utf-8')
    publisher.publish(topic_path, data=data)
    
    print("Done")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project", help="Google Cloud Project ID")
    parser.add_argument("-t", "--topic", help="Topic name")
    parser.add_argument("-d", "--data", help="Data")
    args = parser.parse_args()
    if args.project and args.topic and args.data:
        publish_message(args.project, args.topic, args.data)
    else:
        print("Parameters missing")
    
