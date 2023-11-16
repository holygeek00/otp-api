from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import pyotp
import time

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/generate-otp/")
def generate_otp(secret_key: str = Body(..., embed=True)):
    try:
        # Verify the secret key is not empty
        if not secret_key:
            raise ValueError("Invalid secret key.")
            
        # Instantiate a TOTP object
        totp = pyotp.TOTP(secret_key)
        
        # Generate the current OTP
        otp = totp.now()
        
        # Calculate the remaining time for the current OTP
        remaining_time = totp.interval - int(time.time()) % totp.interval
        
        # Return the current OTP and the remaining time
        return {"otp": otp, "remaining_time": remaining_time}
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid secret key provided.")
