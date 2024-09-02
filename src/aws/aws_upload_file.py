import os
import boto3
from dotenv import load_dotenv

def main():
    load_dotenv()

    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    s3.upload_file(
        os.path.relpath("data/hello.txt", os.getcwd()), # Local file path
        os.getenv("AWS_BUCKET_NAME"),  # Bucket name
        "renatolf1/hello.txt",  # Key (path on bucket)
    )

if __name__ == "__main__":
    main()
