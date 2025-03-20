import boto3
import pandas as pd

def aws_client():
    ## read user keys 
    keys = pd.read_csv ("../team_user_accessKeys.csv")
    
    # id and keys 
    aws_access_key_id = keys.iloc[0, 0]
    aws_secret_access_key = keys.iloc[0, 1]

    # access the aws S3 client and return it
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    return s3_client