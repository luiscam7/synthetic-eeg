"""
Serve synthetic eeg data for testing and visualization purposes.
"""

from fastapi import FastAPI

from models import EEGData
from synthetic_eeg import SyntheticEEG

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Simulated EEG Application!"}


@app.get("/eeg/", response_model=EEGData)
async def retrieve_eeg_data() -> EEGData:
    eeg_writer = SyntheticEEG(n_seconds=600, fs=100)
    eeg_writer.generate_synthetic_eeg()
    return eeg_writer.df.to_dict(orient="list")
