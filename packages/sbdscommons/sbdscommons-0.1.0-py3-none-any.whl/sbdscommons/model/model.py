from sagemaker import Session
from sagemaker.transformer import Transformer
from sbdscommons.constants import BUCKET
from sbdscommons.constants import PARAMS_FOLDER
from sbdscommons.utils.yaml_utils import load_from_yaml
from sbdscommons.constants import MODEL_INPUT_DATA_TEMPLATE_QUERY
from sbdscommons.constants import PREDICT_INPUT_DATA_TEMPLATE_QUERY

from .base import Model
from .base import PrepInput


class SbModel:
    separator = '-'

    def __init__(self,
                 model_name: str,
                 model: Model,
                 input_prep: PrepInput,
                 model_version: str,
                 bucket: str = BUCKET
                 ):
        self.model = model
        self.model_id = f'{model_name}{self.separator}{model_version}'
        self.input_prep = input_prep
        self.model_name = model_name
        self.input_train_path = f'{model_name}/input_data/train'
        self.input_predict_path = f'{model_name}/input_data/predict'
        self.output_path = f'{model_name}/output_data'
        self.model_path = f'{model_name}/model'
        self.bucket = bucket
        self.params_path = f'{PARAMS_FOLDER}/{model_name}.yaml'

    def __repr__(self):
        return self.model_id

    def load_model_params(self):
        ops_dict = load_from_yaml(self.params_path, key='options_dict')
        qry_dict = load_from_yaml(self.params_path, key='query_dict')
        return qry_dict, ops_dict

    def train(self, train_input):
        transformed_input = self.input_prep.transform(train_input)
        self.model.fit(transformed_input)

    def predict(self, predict_input):
        transformed_input = self.input_prep.transform(predict_input)
        return self.model.predict(transformed_input)

    def unload_model_data_to_s3(self):
        query_dict, options_dict = self.load_model_params()
        model_input_data_query = MODEL_INPUT_DATA_TEMPLATE_QUERY.format(self.model_name).format(**query_dict)
        predict_input_data_query = PREDICT_INPUT_DATA_TEMPLATE_QUERY.format(self.model_name).format(**query_dict)
        return model_input_data_query, predict_input_data_query

    def batch_transform_job(self):
        # CREATE A batch prediction job
        data_location = f's3://{self.bucket}/{self.output_path}'

        clf_trans = Transformer(
            base_transform_job_name='Batch-Transform',
            model_name=self.model_id,  # insert model name here
            instance_count=2,
            instance_type='ml.m5.2xlarge',
            output_path=data_location,
            sagemaker_session=Session(),
            max_payload=100
        )

        # Get some input data for the batch prediction job
        predict_data_key = f'{self.input_predict_path}/model_input_prediction000.csv'
        predict_data_location = f's3://{self.bucket}/{predict_data_key}'
        # start the prediction job
        clf_trans.transform(
            predict_data_location,
            content_type='text/csv',
            split_type='Line'
        )

        # wait until prediction job is completed
        clf_trans.wait()
