## IOT Communication using Google Pub/Sub

Google Pub/Sub is a real time messaging service where you could create topics (streams) to which messages can be published and received.
It provides a consistent latency and has a free quota of 10GB per month. Pub/Sub stands for Publish/Subscribe model, similar to how push notifications work.

It must be noted that Pub/Sub does not relay messages in order, so publishing a burst of messages is not going to work as intended. (Timestamps can be used to order them, client side).

## Setting up

1. To set up Pub/Sub, follow the steps [here][https://cloud.google.com/pubsub/docs/quickstart-client-libraries]
2. The 'publish.py' is used to publish the messages.
3. The 'receive.py' will act as a client and receive the messages.
4. Create a project at [Google Cloud Console][https://console.cloud.google.com] and note the project id.
5. Get a client secret file and store it in your device. Use `export GOOGLE_APPLICATION_CREDENTIALS=<path_to_file>` on your command line.
6. Create a topic using the GCP > Pub/Sub > Create Topic. ( Note this name )
7. Create a subscription using which messages are going to be received. Go to the created topic > Create Subscription > Give a name and make its delivery type as 'Pull'
8. Use the values of project id, topic name, subscription name to run the samples.

