import os
import sys
import boto3
import pickle
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sklearn.ensemble import RandomForestRegressor

def main(data_path: str, model_name: str) -> None:
    """
    Main function to predict the total sales.

    Args:
        data_path (str): Path to the sql script to retrieve the data.
        model_name (str): Path to the model.
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

    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    bucket_name = os.getenv("AWS_BUCKET_NAME")
    remote_model_path = f"renatolf1/{model_name}"
    obj = s3.get_object(
        Bucket=bucket_name,
        Key=remote_model_path,
    )
    file_content = obj["Body"].read()
    model = pickle.loads(file_content)
    print(f"Loaded model {model_name} from bucket {bucket_name}...")

    prediction_path = data_path.split("/")[-1].replace("predict-", "predict-done-")
    if not prediction_path.startswith("predict-done-"):
        prediction_path = f"predict-done-{prediction_path}"
    predict(data, model, engine)

def predict(data: pd.DataFrame, model: RandomForestRegressor, engine: Engine) -> None:
    """
    Predict the total sales.

    Args:
        data (pd.DataFrame): Data to be used for prediction.
        model: Model to be used for prediction.
        engine (Engine): Database engine.
    """
    predictions = model.predict(data)
    data["prediction_total_sales"] = predictions

    data.to_sql(
        name=os.getenv("DB_PREDICTION_TABLE"),
        con=engine,
        schema=os.getenv("DB_PREDICTION_SCHEMA"),
        if_exists="replace",
        index=False
    )
    print("Predictions saved to database.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("USAGE: python predict.py <name of the model> <path to sql script>")
        sys.exit(1)
    else:
        DATA_PATH = sys.argv[-1]
        MODEL_PATH = sys.argv[-2]
        main(DATA_PATH, MODEL_PATH)
        sys.exit(0)
