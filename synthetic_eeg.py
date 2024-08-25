"""
Generate synthetic EEG signals
"""

import numpy as np
import pandas as pd
from neurodsp.sim import sim_oscillation
from neurodsp.utils import create_times


class SyntheticEEG:
    def __init__(self, n_seconds, fs):
        """
        Initialize the EEGWriter with the duration of the signals and sampling frequency.

        Parameters
        ----------
        n_seconds : float
            Length of the signal in seconds.
        fs : float
            Sampling frequency of the signal.
        """
        self.n_seconds = n_seconds
        self.fs = fs
        self.times = create_times(n_seconds, fs)
        self.df = pd.DataFrame(index=self.times)

    def generate_eeg_signal(self, central_freq, phase_degrees=0, amp_factor=10):
        """
        Generate an EEG signal centered around one frequency using neurodsp with a specific phase.

        Parameters
        ----------
        central_freq : float
            The central frequency of the EEG signal in Hz.
        phase_degrees : float, optional, default: 0
            The initial phase of the signal in degrees.
        amp_factor : float, optional, default: 1
            Amplitude scaling factor.

        Returns
        -------
        signal : 1d array
            Generated EEG signal.
        """
        phase_fraction = phase_degrees / 360.0
        signal = amp_factor * sim_oscillation(
            self.n_seconds, self.fs, central_freq, phase=phase_fraction
        )
        return signal

    def generate_synthetic_eeg(self):
        """
        Populate the dataframe with EEG signals for each 10-20 system channel.
        """
        # Frontal Region
        self.df["Fp1"] = self.generate_eeg_signal(3)
        self.df["Fp2"] = self.generate_eeg_signal(6)
        self.df["F3"] = self.generate_eeg_signal(11)
        self.df["F4"] = self.generate_eeg_signal(17)

        # Central Region
        self.df["C3"] = self.df[["Fp1", "Fp2", "F3", "F4"]].mean(axis=1).values
        self.df["Cz"] = (self.df["Fp1"].values + self.generate_eeg_signal(2.5)) / 2
        self.df["C4"] = (self.df["Fp2"].values + self.generate_eeg_signal(5.5)) / 2
        self.df["T3"] = (self.df["F3"].values + self.generate_eeg_signal(9.8)) / 2
        self.df["O1"] = (self.df["F4"].values + self.generate_eeg_signal(15)) / 2

        self.df["O2"] = (self.df["Fp1"].values + self.add_noise(noise_level=5)) / 2
        self.df["P3"] = (self.df["Fp2"].values + self.add_noise(noise_level=5)) / 2
        self.df["P4"] = (self.df["F3"].values + self.add_noise(noise_level=5)) / 2
        self.df["F7"] = (self.df["F4"].values + self.add_noise(noise_level=5)) / 2

        self.df["F8"] = (
            self.df["Fp1"].values + self.generate_eeg_signal(3, phase_degrees=30)
        ) / 2
        self.df["T4"] = (
            self.df["Fp2"].values + self.generate_eeg_signal(6, phase_degrees=60)
        ) / 2
        self.df["T5"] = (
            self.df["F3"].values + self.generate_eeg_signal(11, phase_degrees=90)
        ) / 2
        self.df["T6"] = (
            self.df["F4"].values + self.generate_eeg_signal(17, phase_degrees=120)
        ) / 2

        self.df["Fz"] = (
            self.generate_eeg_signal(3, amp_factor=20)
            + self.generate_eeg_signal(6, amp_factor=20)
            + self.generate_eeg_signal(11, amp_factor=20)
            + self.generate_eeg_signal(17, amp_factor=20)
        ) / 4

        self.df["Pz"] = (
            self.df[["F8", "T4", "T5", "T6"]].mean(axis=1).values
            + self.add_noise(noise_level=5)
        ) / 2

    def add_noise(self, noise_level=0.1):
        """
        Add random noise to all EEG channels.

        Parameters
        ----------
        noise_level : float, optional, default: 0.1
            The standard deviation of the Gaussian noise to be added to the signal.
        """
        noise = np.random.normal(0, noise_level, size=self.df.shape[0])
        return noise
