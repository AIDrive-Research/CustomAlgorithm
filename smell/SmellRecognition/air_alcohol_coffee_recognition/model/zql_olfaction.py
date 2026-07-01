import joblib

from logger import LOGGER
from model import Model as BaseModel
from utils.file_utils import abspath


class Model(BaseModel):
    default_args = {
        'sensor_count': 10
    }

    def __init__(self, name, conf):
        self.sensor_count = None
        self.scaler = None
        self.label_encoder = None
        super().__init__(name, conf)

    def _load_args(self, args):
        try:
            self.sensor_count = int(args.get('sensor_count', self.default_args['sensor_count']))
        except:
            LOGGER.exception('_load_args')
            return False
        return True

    def _load_model(self, path):
        try:
            bundle = joblib.load(abspath(path, 'model'))
            self.model = bundle['model']
            self.scaler = bundle['scaler']
            self.label_encoder = bundle['label_encoder']
        except:
            LOGGER.exception('_load_model')
            return False
        return True

    def __check_data(self, data):
        if len(data) != self.sensor_count:
            LOGGER.error('Invalid sensor count, expect {}, but get {}, model_name={}'.format(
                self.sensor_count, len(data), self.name))
            return None
        return [float(v) for v in data]

    def infer(self, data, **kwargs):
        infer_result = {
            'label': None,
            'conf': None,
            'result': {}
        }
        if self.status:
            try:
                infer_data = self.__check_data(data)
                if infer_data is not None:
                    scaled = self.scaler.transform([infer_data])
                    probs = self.model.predict_proba(scaled)[0]
                    for cls, prob in zip(self.label_encoder.classes_, probs):
                        label = str(cls)
                        score = round(float(prob), 3)
                        if infer_result['conf'] is None or infer_result['conf'] < score:
                            infer_result['label'] = label
                            infer_result['conf'] = score
                        infer_result['result'][label] = score
                if infer_result:
                    return infer_result
            except:
                LOGGER.exception('infer')
        return infer_result
