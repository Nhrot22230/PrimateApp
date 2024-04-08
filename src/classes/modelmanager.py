from src.utils.modelutils import *
from src.utils.plotutils import smooth_results
import tensorflow as tf
import os
import io

class ModelManager():
    def __init__(self, models_dir):
        self.models_dir = models_dir
        self.models = {}

    def scan_models(self):
        model_name_list = []
        for model_name in os.listdir(self.models_dir):
            model_name_list.append(model_name)
            self.models[model_name] = None
        return model_name_list
    
    def load_model(self, model_name):
        model_path = os.path.join(self.models_dir, model_name)
        model = tf.keras.models.load_model(model_path)
        self.models[model_name] = model

    def get_model(self, model_name):
        if model_name not in self.models:
            return None
        return self.models[model_name]
    
    def predict(self, model_name, file):
        model = self.get_model(model_name)
        results = predictSingleFile(model, file)
        return smooth_results(results)
    
    def get_model_info(self, model_name):
        stream = io.StringIO()
        model = self.get_model(model_name)
        model.summary(print_fn=lambda x: stream.write(x + '\n'))
        summary_string = stream.getvalue()
        stream.close()
        print(summary_string)
        return summary_string