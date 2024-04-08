# Matplotlib for data visualization
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import resample
import os

def smooth_results(results, window_size=5):
    """
    Smooth the prediction results using a moving average.

    Args:
    - results (list): List of prediction scores.
    - window_size (int): Size of the window for the moving average.

    Returns:
    - smoothed_results (list): List of smoothed prediction scores.
    """
    # Create a list to store the smoothed results
    smoothed_results = []

    # Compute the moving average for the prediction scores
    for i in range(len(results)):
        window = results[max(0, i - window_size // 2):min(len(results), i + window_size // 2)]    
        sum = 0
        mid = len(window) // 2
        sum_distances = 0
        for index in range(len(window)):
            distance_from_mid = abs(index - mid)
            sum += window[index] * (1 - distance_from_mid / mid)
            sum_distances += (1 - distance_from_mid / mid)

        smoothed_results.append(sum / sum_distances)

    return smoothed_results

def createPredictionPlot(results, file):
    """
    Plot the prediction scores for the audio clips in the file.

    Args:
    - results (list): List of prediction scores.
    - file (str): Name of the audio file.

    Returns:
    - fig (Figure): Matplotlib figure containing the plot.
    """
    # Extract the prediction scores
    prediction_scores = smooth_results(results)

    # Create an array containing the indices of the audio clips
    clip_indices = [x * 0.05 for x in range(len(prediction_scores))]

    # Set up the plot
    fig, ax = plt.subplots()
    ax.plot(clip_indices, prediction_scores, marker='o', linestyle='-')  # Add markers and linestyle
    ax.set_xlabel('Index of Clip')  # Set x-axis label
    ax.set_ylabel('Prediction Score')  # Set y-axis label
    ax.set_title('Prediction Scores for Audio Clips in {}'.format(file))  # Set title
    ax.grid(True)  # Add grid
    fig.tight_layout()  # Adjust layout to prevent clipping of labels

    return fig, ax

def createSpectrogram(file, audio_dir):
    """
    Plot the spectrogram of the audio file.

    Args:
    - file (str): Name of the audio file.
    - audio_dir (str): Root directory containing the audio files.

    Returns:
    - canvas (FigureCanvasTkAgg): Tkinter-compatible canvas containing the plot.
    """
    # Read the WAV file
    sampling_freq, audio = wavfile.read(os.path.join(audio_dir, file))

    # Resample the audio to a target frequency of 26000 Hz
    target_freq = 26000
    audio_resampled = resample(audio, int(len(audio) * target_freq / sampling_freq))

    # Compute the spectrogram of the resampled audio
    fig, ax = plt.subplots()
    ax.specgram(audio_resampled, Fs=target_freq)

    # Set title, labels, and color bar
    ax.set_title('File: {} Resampled Spectrogram ({} Hz)'.format(file, target_freq))
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    fig.colorbar(ax.specgram(audio_resampled, Fs=target_freq)[3], ax=ax, label='Intensity (dB)')

    # Set font sizes for ticks
    ax.tick_params(axis='both', which='major')
    ax.tick_params(axis='both', which='minor')

    return fig, ax
