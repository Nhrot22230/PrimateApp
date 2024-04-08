import os
import librosa
import soundfile as sf


class AudioManager:
    def __init__(self):
        pass

    def audio_file_exists(self, filepath):
        """
        Check if the specified audio file exists.

        Parameters:
            filepath (str): The path to the audio file.

        Returns:
            bool: True if the audio file exists, False otherwise.
        """
        return os.path.isfile(filepath)

    def load_audio_data(self, filepath, sr=None):
        """
        Load audio data from the specified file.

        Parameters:
            filepath (str): The path to the audio file.
            sr (int, optional): Sampling rate to resample the audio data to. Default is None.

        Returns:
            tuple: A tuple containing the audio data (as a NumPy array) and the sampling rate.
        """
        if self.audio_file_exists(filepath):
            data, sampling_rate = librosa.load(filepath, sr=sr)
            return data, sampling_rate
        else:
            raise FileNotFoundError(f"Audio file '{filepath}' not found.")

    def save_audio_data(self, filepath, data, sampling_rate):
        """
        Save audio data to the specified file.

        Parameters:
            filepath (str): The path to save the audio file.
            data (ndarray): The audio data as a NumPy array.
            sampling_rate (int): The sampling rate of the audio data.
        """
        sf.write(filepath, data, sampling_rate)

    def resample_audio_data(self, data, current_sr, target_sr):
        """
        Resample audio data to the target sampling rate.

        Parameters:
            data (ndarray): The audio data as a NumPy array.
            current_sr (int): The current sampling rate of the audio data.
            target_sr (int): The target sampling rate to resample to.

        Returns:
            ndarray: The resampled audio data.
        """
        return librosa.resample(data, orig_sr=current_sr, target_sr=target_sr)

    def normalize_audio_data(self, data):
        """
        Normalize audio data to have maximum amplitude of 1.

        Parameters:
            data (ndarray): The audio data as a NumPy array.

        Returns:
            ndarray: The normalized audio data.
        """
        return librosa.util.normalize(data)
