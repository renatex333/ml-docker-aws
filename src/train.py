import os
import sys
import boto3
import pickle
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor

def main(data_path: str) -> None:
    """
    Main function to train the model.

    Args:
        data_path (str): Path to the sql script to retrieve the data.
    """
    load_dotenv()
    db_url = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)
    with open(data_path, "r", encoding="utf-8") as f:
        sql_script = f.read()
    with engine.connect() as conn:
        data = pd.read_sql(
            sql=sql_script,
            con=conn.connection
        )
    train_model(data, "total_sales", data_path)

def train_model(data: pd.DataFrame, target: str, data_path: str) -> None:
    X = data.drop(columns=[target])
    y = data[target]
    
    print("Training model...")
    model = RandomForestRegressor(n_estimators=100, random_state=195)
    model.fit(X, y)

    model_name = data_path.split("/")[-1]
    for ext in ["parquet", "csv", "sql"]:
        if model_name.endswith(ext):
            model_name = model_name.replace(f".{ext}", ".pkl").replace("train-", "model-")
            break
    if not model_name.startswith("model-"):
        model_name = f"model-{model_name}"
    save_model(model, model_name)

def save_model(model: RandomForestRegressor, model_name: str) -> None:
    """
    Save the model to disk.

    Args:
        model: Model to be saved.
        model_name: Name of the model.
    """
    model_dir = os.path.relpath("models", os.getcwd())
    model_path = os.path.join(model_dir, model_name)
    print(f"Saving model to {model_path}...")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    save_to_aws(model_path, model_name)

def save_to_aws(local_model_path, model_name):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    remote_model_path = f"renatolf1/{model_name}"
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    print(f"Saving model to bucket {bucket_name} on {remote_model_path}...")
    s3.upload_file(
        local_model_path,
        bucket_name,
        remote_model_path,  # Key (path on bucket)
    )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: python train.py <path to sql script>")
        sys.exit(1)
    else:
        DATA_PATH = sys.argv[-1]
        main(DATA_PATH)
        sys.exit(0)
