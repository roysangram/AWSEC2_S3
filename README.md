# AWSECInstallation - boto3 for python

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
