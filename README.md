# backend

# Setup & Run

-- Create Environment:

python -m venv myenv  
source myenv/bin/activate  # Linux/macOS  
myenv\Scripts\activate     # Windows  


-- Install Dependencies:

pip install -r requirements.txt  

python main.py 

This script implements a WebSocket bridge server that receives raw audio data from a client (such as a microphone recorder) and forwards it to a Whisper transcription WebSocket server (ws://localhost:9090/client).



# client

-- Run:

python mic_client.py  # Ensure server is running on port 8765  


