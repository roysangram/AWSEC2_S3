# AWSEC

Objective – 
•	To build an application in AWS that uses EC2, S3 and SQS 
•	Be familiar with EC2, S3 and sqs and to understand how they work in real time environment
•	Understand how different aws component communicate to the application

To achieve this first we need to build two apps: 
1-	 Client App-: cc_clientapp.py
2-	ec2_instance app-: cc_ec2_instance_app.py

Client APP-:

Create an application that should do the following:
•	It should run locally on your machine.
•	User inputs a comma-separated list of numbers.
•	Puts this list in the S3-bucket (and remembers the key/pointer to this object).
•	Puts a message in the SQS-inbox with a key/pointer to the object in the S3-bucket, along with a process to be executed on these numbers.
•	Waits until a response is generated in the SQS-outbox (should contain a pointer to a new, and processed, object in the S3-bucket along with the process executed).
•	Reads the result from the S3-bucket
•	Prints the results along with the original numbers and the process that was done.
•	Delete the message from sqs-outbox

EC2- Instance APP-:

Instance app should do the following 
•	Run locally during development and testing phase and should run from EC2 instance 
•	get the sqs message to be processed from sqs-inbox queue
•	delete the message form sqs-inbox
•	process the message and return the result
•	update the result in S3 bucket
update the result in outbox queue



Installation - boto3 for python

Check for python-pip installation - just run pip command , if it shows info and pip details then it is installed

installing boto3 - pip install boto3

Manual steps need to be done befor running the scripts -:

a- create a S3 bucket and update the name of bucket in the scripts
b- create 2 queue named inbox and outbox with long pooling enabled
c- update secret key/access key and region in credentials and config file in ~/.aws/credentials and config file

 bash-3.2$ cd ~/.aws/
 bash-3.2$ cat credentials 
[default]
aws_access_key_id=XXXXXXXXXXXXXX
aws_secret_access_key=XXXXXXXXXXXXX
bash-3.2$ cat config
[default]
region=ap-south-1
bash-3.2$ 

run1 - : both ec2_instanccode and local app should run locally

open two terminals in your laptop

in one terminal run local_app.py and then another terminal run ec2_instancecode.py

if you see the list of nos sent and processed_list of nos in  S3 bucket file as well as in console then it is running fine

commands to run python file-:

python file_name.py



run 2- 

create 2 EC2 instance - 

and put ec2_instance code in both the instance

then similarly first run local app then run ec2_instance code  from one of EC2 instance 

if you see the list of nos sent and processed_list of nos in file as well as in console then it is running fine

similarly for 2nd ec2 instance-:

then similary first run local app then run ec2_instance code  from 2nd EC2 instance 

if you see the list of nos sent and processed_list of nos in S3 bucket file as well as in console with no error then it is running fine
