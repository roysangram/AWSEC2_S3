'''
Created on 19-Oct-2017

@author: skroy3

Steps -:
1- get the sqs message to be processed from inbox queue
2- delete the message form inbox
3- process the message and return the result
4- update the result in S3 bucket
5- update the result in outbox queue

'''
# Import the SDK
import boto3
import uuid
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Get the service resource
sqs = boto3.client('sqs')
s3 = boto3.client('s3')
bucket_name="sroy-bucket1"


# create a file to be uploaded into S3 bucket
def create_file(key_name,message_to_be_sent):
    file=open(key_name,"a")
    file.write('\n'+str(message_to_be_sent))
    file.close()
    print file.name
    return file.name


# Receive message from inbox SQS queue
def get_sqs_message():
    response = sqs.get_queue_url(QueueName='inbox')
    print response
    logging.info("get queue url response info: %s", response)
    url1 = response['QueueUrl']
    response = sqs.receive_message(
        QueueUrl=url1,
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
    logging.info("receive message response info: %s", response)
    message = response['Messages'][0]['Body']
    receipt_handle = response['Messages'][0]['ReceiptHandle']

    print "message received from inbox queue: %s",message
    # deleting  sqs message
    response=sqs.delete_message(
        QueueUrl=url1,
        ReceiptHandle=receipt_handle)
    logging.info("deleting sqs message inbox: %s", response)

    return message



#function to process the list of nos
'''it will take list of three nos and return /
          some,product and average  in a list '''


def process_message( message):

    msg_list=eval(message)

    list_of_nos =msg_list['the list of nos']
    print "list of no to be processed:",list_of_nos
    key_name=msg_list['key_name']
    print "S3 object key/pointer name is :",key_name
    operation = msg_list['operation']
    print "operations to be performed:",operation
    num1 = list_of_nos[0]
    num2 = list_of_nos[1]
    num3 = list_of_nos[2]
    sum = num1+num2+num3
    average = sum/3
    product = num1*num2*num3

    result = [sum,average,product]

    return result,key_name,operation


# below function is to send message to  sqs outbox after processing
def send_sqs_message(msg):

    response = sqs.get_queue_url(QueueName='outbox')
    logging.info("get queue url response info: %s", response)
    url2 = response['QueueUrl']

    response = sqs.send_message(QueueUrl=url2,\
                           MessageBody=str(msg))
    logging.info("send_message response info: %s", response)


# function to update s3 bucket with list of nos
def add_msg_s3_outbox(key_name,message):

    file_name = create_file(key_name,message)

    response=s3.upload_file(file_name, bucket_name, file_name)

    logging.info("response uploaded file in to S3: %s", response)


if __name__ == "__main__":

    msg = get_sqs_message()

    pr_msg,key_name,operation = process_message(msg)

    result_message={"the processed list of nos":pr_msg,"key_name":key_name,"operation":operation}

    send_sqs_message(result_message)

    add_msg_s3_outbox(key_name,result_message)


