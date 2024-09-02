# docker-aws-api

Welcome to this ML project!

This project aims to train a machine learning model using data from a local docker container database and then store the trained model in an S3 bucket.

## Installing Dependencies

To install the project dependencies, use the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

## Project Structure

- `data`: Contains the data used by the model.
- `models`: Contains the machine learning models and encoders.
- `notebooks`: Contains the notebooks used for data exploration and visualization.
- `src`: Contains the main source code to collect and process data, train models and make predictions.
- `tests`: Contains unit and integration tests to guarantee code stability.

## Usage

To train a model:
```bash
python train.py <path_to_sql_script>
```

To run predictions:
```bash
python predict.py <model_name> <path_to_sql_script>
```