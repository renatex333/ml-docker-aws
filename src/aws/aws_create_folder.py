import os
import boto3
from pprint import pprint
from dotenv import load_dotenv

def main():
    load_dotenv()

    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # Create folder
    res = s3.put_object(
        Bucket=os.getenv("AWS_BUCKET_NAME"),
        Key="renatolf1/",
    )

    print("Answer:")
    pprint(res)

if __name__ == "__main__":
    main()
