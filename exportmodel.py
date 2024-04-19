import tensorflow as tf
import keras
import os


if __name__ == '__main__':
    model_dir = 'models'
    model_name = os.listdir(model_dir)[1]
    print(model_name)
    model = keras.models.load_model(os.path.join(model_dir, model_name))

    assert isinstance(model, keras.models.Model)

    model.summary()

    model.save('MAXPOOL.keras')

    print('Model saved')

    print(os.listdir('.'))


    