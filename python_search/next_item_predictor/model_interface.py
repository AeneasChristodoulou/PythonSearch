from typing import Tuple

import numpy as np
import os
from pyspark.sql import DataFrame


class BaseModel:
    """
    Sets of interfaces that need to be implemented to provide a new version of the NextItemPredictor model
    """

    def load_or_build_dataset(self):
        if os.path.exists("/tmp/dataset.parquet"):
            print("Loading dataset from /tmp/dataset.parquet")
            from pyspark.sql.session import SparkSession

            spark = SparkSession.builder.getOrCreate()

            return spark.read.parquet("/tmp/dataset.parquet")

        df = self.build_dataset(debug=False)

        df = df.drop("uuid")
        df.write.parquet("/tmp/dataset.parquet")

        return df

    def build_dataset(self) -> DataFrame:
        """
        Builds a dataset for the NextItemPredictor model.
        """
        raise Exception("Not implemented")

    def transform_single(self, inference_input: dict) -> np.ndarray:
        """
        Transforms a single inference input into a numpy array.
        Return X
        :param inference_input:
        :return:
        """
        raise Exception("Not implemented")

    def transform_collection(self, dataset: DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns X and Y
        :param dataset:
        :return:
        """
        raise Exception("Not implemented")

    def load_mlflow_model(self):
        raise Exception("Not implemented")
