'''
Created on 19-Oct-2017

@author: skroy3

     message contains list of nos, process to performed and key_name to the S3 object(file name)
     puts message in sqs inbox queue
     puts the same message in S3 bucket
     waits for response for sqs outbox queue
     get the message from sqs out box and delete the message from outbox
     print the message from S3 bucket
'''
# Import the SDK

import boto3;
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

#creating sqs client
sqs = boto3.client('sqs')

#creating s3 client
s3 = boto3.client('s3')

list_of_nos=[5,6,7]
bucket_name = "sroy_bucket1"
key_name="S3_66117.txt"

#message to sent to S3 bucket and inbox queue
message_to_be_sent= {"the list of nos":list_of_nos,"key_name":key_name,"operation":"sum//average/product"}

#function to create file to uploaded to S3
def create_file(message_to_be_sent):
    file=open(key_name,"a")
    file.write('\n'+str(message_to_be_sent))
    file.close()
    print file.name
    return file.name

# this function will put the message to inbox queue
def put_sqs_message(message_to_be_sent):
    response = sqs.get_queue_url(QueueName='inbox')
    logging.info("get queue url response info: %s", response)
    url1 = response['QueueUrl']
    response =sqs.send_message(
            QueueUrl=url1,MessageBody=(str(message_to_be_sent))
     )
    logging.info("get send message response info: %s", response)

#this function upload the message to S3 bucket
def add_msg_s3_inbox():
    s3 = boto3.client('s3')
    #s3.create_bucket(Bucket='my-bucket')
    file_name=create_file(message_to_be_sent)

    print "uploading file in to S3 bucket:", file_name

    s3.upload_file(file_name,bucket_name,file_name)


# get the response from outbox queue and delete the outbox message
def get_sqs_message_outbox():
    response = sqs.get_queue_url(QueueName='outbox')
    logging.info("get queue url response info: %s", response)
    url2= response['QueueUrl']
    response = sqs.receive_message(
        QueueUrl=url2,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=30,
        WaitTimeSeconds=20
    )
    logging.info("get outbox sqs message response info: %s", response)
    message = response['Messages'][0]['Body']
    receipt_handle = response['Messages'][0]['ReceiptHandle']
    print  "processed message from outbox:",message

    # deleting message
    response=sqs.delete_message(
        QueueUrl=url2,
        ReceiptHandle=receipt_handle)
    logging.info("deleting sqs message outbox: %s", response)

    return message

#print the S3 bucket details after processing in the console
def get_s3_message():
    s3 = boto3.resource('s3')

    print " printing S3 object details after processing: "

    print s3.Object(bucket_name, key_name).get()['Body'].read()


if __name__ == "__main__":

    put_sqs_message(message_to_be_sent)

    add_msg_s3_inbox()

    message=get_sqs_message_outbox()

    get_s3_message()







