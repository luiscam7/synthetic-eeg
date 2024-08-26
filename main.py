from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import EEGData
from synthetic_eeg import SyntheticEEG

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Change this to specific domains for production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Simulated EEG Application!"}


@app.get("/eeg/", response_model=EEGData)
async def retrieve_eeg_data() -> EEGData:
    eeg_writer = SyntheticEEG(n_seconds=600, fs=100)
    eeg_writer.generate_synthetic_eeg()
    return eeg_writer.df.to_dict(orient="list")
