# -*- coding: utf-8 -*-
"""Audio Post Processing Function .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1M_9B29kB3HsxDxfEj1XRxHfCmmRnXFeb
"""

import torch
import torchaudio
import torchaudio.functional as Tf
import matplotlib.pyplot as plt
import torchaudio.transforms as T

def plot_waveform(waveform, sample_rate):
    waveform = waveform.numpy()

    num_channels, num_frames = waveform.shape
    time_axis = torch.arange(0, num_frames) / sample_rate

    figure, axes = plt.subplots(num_channels, 1)
    if num_channels == 1:
        axes = [axes]
    for c in range(num_channels):
        axes[c].plot(time_axis, waveform[c], linewidth=1)
        axes[c].grid(True)
        if num_channels > 1:
            axes[c].set_ylabel(f"Channel {c+1}")
    figure.suptitle("waveform")
    plt.show(block=False)

def plot_specgram(waveform, sample_rate, title="Spectrogram"):
    waveform = waveform.numpy()

    num_channels, num_frames = waveform.shape

    figure, axes = plt.subplots(num_channels, 1)
    if num_channels == 1:
        axes = [axes]
    for c in range(num_channels):
        axes[c].specgram(waveform[c], Fs=sample_rate)
        if num_channels > 1:
            axes[c].set_ylabel(f"Channel {c+1}")
    figure.suptitle(title)
    plt.show(block=False)

file_path = "y2mate.is - You Won t Believe What Obama Says In This Video -cQ54GDm1eL0-192k-1696266710.wav"
waveform, sample_rate = torchaudio.load(file_path)
def lowpasss(file_path):
  waveform, sample_rate = torchaudio.load(file_path)

  cutoff_freq = 500
  filtered_waveform = Tf.lowpass_biquad(waveform,sample_rate=sample_rate,cutoff_freq=cutoff_freq)

  output_path = 'output_filtered_audio.wav'
  torchaudio.save(output_path, filtered_waveform, sample_rate)
  print(f"Filtered audio saved to {output_path}")
  return filtered_waveform

file_path = "y2mate.is - You Won t Believe What Obama Says In This Video -cQ54GDm1eL0-192k-1696266710.wav"
def up_down_sampling(file_path):
  waveform, sample_rate = torchaudio.load(file_path)

  target_sample_rate_up = 50000
  target_sample_rate_down = 45000

  resample_up = T.Resample(orig_freq=sample_rate, new_freq=target_sample_rate_up)
  upsampled_waveform = resample_up(waveform)

  resample_down = T.Resample(orig_freq=sample_rate, new_freq=target_sample_rate_down)
  downsampled_waveform = resample_down(waveform)

  output_path_up = 'output_upsampled_audio.wav'
  output_path_down = 'output_downsampled_audio.wav'

  torchaudio.save(output_path_up, upsampled_waveform, target_sample_rate_up)
  torchaudio.save(output_path_down, downsampled_waveform, target_sample_rate_down)

  print(f"Upsampled audio saved to {output_path_up}")
  print(f"Downsampled audio saved to {output_path_down}")
  return upsampled_waveform, downsampled_waveform

original_audio_path = "y2mate.is - You Won t Believe What Obama Says In This Video -cQ54GDm1eL0-192k-1696266710.wav"
def external_noise(original_audio_path):
  waveform, sample_rate = torchaudio.load(original_audio_path)
  desired_snr_db = 3
  noise_waveform = torch.randn_like(waveform)
  original_power = torch.mean(waveform ** 2)
  noise_power = torch.mean(noise_waveform ** 2)
  scaling_factor = torch.sqrt(original_power / (3 ** (desired_snr_db / 10) * noise_power))
  noise_waveform *= scaling_factor
  noisy_waveform = waveform + (noise_waveform/10)
  output_path = 'output_noisy_audio.wav'
  torchaudio.save(output_path, noisy_waveform, sample_rate)
  print(f"Noisy audio saved to {output_path}")
  return noisy_waveform

original_audio_path = "y2mate.is - You Won t Believe What Obama Says In This Video -cQ54GDm1eL0-192k-1696266710.wav"
def bichannel_mono(original_audio_path):
  bichannel_audio, sample_rate = torchaudio.load(original_audio_path)
  print("Bichannel audio shape:", bichannel_audio.shape)
  mono_audio = torch.mean(bichannel_audio, dim=0)
  return mono_audio

filtered_waveform = lowpasss(file_path)
upsampled_waveform, downsampled_waveform = up_down_sampling(file_path)
noisy_waveform = external_noise(original_audio_path)
mono_audio = bichannel_mono(original_audio_path)

from IPython.display import Audio
Audio(waveform.numpy()[0], rate=sample_rate)

Audio(filtered_waveform.numpy()[0], rate=sample_rate)

Audio(upsampled_waveform.numpy()[0], rate=sample_rate)

Audio(downsampled_waveform.numpy()[0], rate=sample_rate)

Audio(noisy_waveform.numpy()[0], rate=sample_rate)

Audio(mono_audio, rate=sample_rate)

plot_specgram(waveform, sample_rate)

plot_specgram(noisy_waveform, sample_rate)

plot_specgram(downsampled_waveform, sample_rate)

time scaling
frequency scaling
SIgnal to Noise Ratio

increase by 1 from 0 to 10