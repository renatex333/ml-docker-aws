# ML-Docker-AWS

Welcome to this Machine Learning project!

This project is designed to train a machine learning model using data sourced from a local Docker container database. Once the model is trained, it will be stored in an AWS S3 bucket for future use.

## Installation

To set up the project and install dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Project Structure

- **`data/`**: Contains SQL scripts for querying data from the Docker container database.
- **`models/`**: Stores the trained machine learning models and encoders.
- **`src/`**: Contains the core source code responsible for data collection, processing, model training, and making predictions.

## Usage

### To Train a Model:

Run the following command to train a model using data from a SQL script:

```bash
python train.py <path_to_sql_script>
```

- `<path_to_sql_script>`: Path to the SQL script that retrieves the data for training.

### To Run Predictions:

Run the following command to make predictions using a pre-trained model:

```bash
python predict.py <model_name> <path_to_sql_script>
```

- `<model_name>`: The name of the trained model file (e.g., `.pkl`).
- `<path_to_sql_script>`: Path to the SQL script that retrieves the data for prediction.
