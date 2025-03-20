# Welcome to ilab-07-2

## Federated deep learning for gastric cancer diagnosis

### General Rules
1) Each contributor must clone the repo
2) Create your own branch and commit to this.
3) **Do not** commit to main
4) When you are ready to contribute your code to main, create a PR and select a reviewer
5) Reviewer checks code and allows the merge to proceed


### Accessing the clinical images

All images are located in an AWS S3 bucket called `gastric-cancer-data`
* make sure your git repo is up to date with main

There are two easy ways to access the images;
1) aws cli
2) python code using the aws `boto3` library

### aws cli
1) install the aws cli using a package manager like [homebrew](https://brew.sh/)

```zsh
brew install awscli
```
Configure aws credentials:
```zsh
aws configure
```

Enter the key and secret from `team_user_accessKeys.csv` located in the project repo.
 

Check identity:

```zsh
aws sts get-caller-identity
```

View the bucket contents:

```zsh
aws s3 ls gastric-cancer-data
```

### Python and the [AWS SDK](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
2) Using a jupyter notebook;

```python
pip install boto3
```

```python
import boto3
import pandas as pd

key_df = pd.read_csv('team_user_accessKeys.csv', sep=',')

# Replace the following values with your access key details
aws_access_key_id = key_df.iloc[0,0]
aws_secret_access_key = key_df.iloc[0,1]
region_name = 'ap-southeast-2'

# Create an S3 client using the provided access keys
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# List all the buckets
buckets = s3_client.list_buckets()
for bucket in buckets['Buckets']:
    print(bucket['Name'])
```





