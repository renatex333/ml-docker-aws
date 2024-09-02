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

    obj = s3.get_object(
        Bucket=os.getenv("AWS_BUCKET_NAME"),
        Key="welcome.txt",
        # Key="renatolf1/hello.txt",
    )

    file_content = obj["Body"].read().decode("utf-8")

    print(f"File Content:\n{file_content}")

if __name__ == "__main__":
    main()
