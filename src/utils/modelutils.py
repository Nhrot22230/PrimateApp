import tensorflow as tf
import tensorflow_io as tfio
import os

def processAudioSample(sample, index):
    """
    Preprocesses an audio sample by computing the Short-Time Fourier Transform (STFT) and the magnitude of the STFT.

    Args:
        sample (tf.Tensor): Audio waveform sample.
        index (int): Index of the sample in the dataset.

    Returns:
        tf.Tensor: Preprocessed audio sample.
    """
    # Extract the audio sample from the input tuple
    sample = sample[0]

    # Pad the sample with zeros to make its length 13000 (if shorter)
    zero_padding = tf.zeros([13000] - tf.shape(sample), dtype=tf.float32)
    wav = tf.concat([zero_padding, sample], 0)

    # Compute the Short-Time Fourier Transform (STFT) of the audio waveform
    spectrogram = tf.signal.stft(wav, frame_length=320, frame_step=32)

    # Compute the magnitude of the STFT
    spectrogram = tf.abs(spectrogram)

    # Expand the dimensions of the spectrogram tensor
    spectrogram = tf.expand_dims(spectrogram, axis=2)

    return spectrogram

def load_wav_26k_mono(filename):
    """
    Loads a WAV file with a sample rate of 44.1kHz and a single channel.

    Args:
        filename (str): Path to the WAV file.

    Returns:
        tf.Tensor: Audio waveform with a sample rate of 26kHz.
    """
    # Load encoded WAV file
    file_contents = tf.io.read_file(filename)

    # Decode WAV (tensors by channels)
    wav, sample_rate = tf.audio.decode_wav(file_contents, desired_channels=1)

    # Removes trailing axis
    wav = tf.squeeze(wav, axis=-1)

    # Cast sample rate to int64
    sample_rate = tf.cast(sample_rate, dtype=tf.int64)

    # Resample audio from 44100Hz to 26000Hz
    wav = tfio.audio.resample(wav, rate_in=sample_rate, rate_out=26000)

    return wav

def performAudioClassification(model, recordings, recordings_dir):
    """
    Predicts the labels for a set of audio recordings using a trained model.
    
    Args:
        model (tf.keras.Model): Trained model for audio classification.
        recordings (list): List of audio recording file names.
        recordings_dir (str): Directory containing the audio recording files.

    Returns:
        dict: Dictionary containing the prediction results for each audio recording.
        error_files (list): List of files that could not be loaded.
    """
    # Initialize an empty dictionary to store the results
    results = {}
    error_files = []
    # Loop over each recording file
    for file in recordings:
        # Construct the file path of the current recording
        FILEPATH = os.path.join(recordings_dir, file)

        try:
            # Load the WAV file as a mono audio with a sample rate of 24kHz
            wav = load_wav_26k_mono(FILEPATH)
        except Exception as e:
            # If there is an error loading the file, print an error message and continue to the next file
            print(f"Error loading file {file}: {str(e)}")
            error_files.append(file)
            continue

        # Create time series dataset from the audio data with a sequence length of 13000 samples and stride of 1300 samples
        audio_slices = tf.keras.utils.timeseries_dataset_from_array(wav, wav, sequence_length=13000, sequence_stride=1300, batch_size=1)

        # Preprocess each audio slice in the dataset
        audio_slices = audio_slices.map(processAudioSample)

        # Batch the preprocessed dataset
        audio_slices = audio_slices.batch(16)

        # Predict the labels for the audio slices using the trained model
        yhat = model.predict(audio_slices)

        # Store the prediction results in the dictionary with the file name as the key
        results[file] = yhat

    return results, error_files

def predictSingleFile(model, file):
    """
    Predicts the label for an audio file using a trained model.

    Args:
        model (tf.keras.Model): Trained model for audio classification.
        file (str): Path to the audio file.

    Returns:
        str: Predicted label for the audio file.
    """
    # Load the WAV file as a mono audio with a sample rate of 26kHz
    wav = load_wav_26k_mono(file)

    # Create time series dataset from the audio data with a sequence length of 13000 samples and stride of 1300 samples
    audio_slices = tf.keras.utils.timeseries_dataset_from_array(wav, wav, sequence_length=13000, sequence_stride=1300, batch_size=1)

    # Preprocess each audio slice in the dataset
    audio_slices = audio_slices.map(processAudioSample)

    # Batch the preprocessed dataset
    audio_slices = audio_slices.batch(16)

    # Predict the label for the audio slices using the trained model
    yhat = model.predict(audio_slices)

    return yhat