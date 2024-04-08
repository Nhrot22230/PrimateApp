import os
import librosa
import soundfile as sf

class AudioFixer:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def load_and_save_wav(self, filename):
        try:
            # Load the WAV file using librosa
            y, sr = librosa.load(filename, sr=None)

            # Perform any necessary processing or correction here

            # Save the corrected WAV file
            new_filename = os.path.join(self.output_dir, "fixed_" + os.path.basename(filename))
            sf.write(new_filename, y, sr)

            print("Fixed file saved as:", new_filename)
        except Exception as e:
            print("Error processing file:", filename)
            print("Error:", e)

    def process_audio_files(self):
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Iterate over files in the input directory
        for filename in os.listdir(self.input_dir):
            if filename.endswith(".wav"):
                filepath = os.path.join(self.input_dir, filename)
                self.load_and_save_wav(filepath)