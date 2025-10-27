from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import upload, transactions, analyze, forecast

app = FastAPI(title="Finance Copilot API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)
app.include_router(transactions.router)
app.include_router(analyze.router)
app.include_router(forecast.router)



# from fastapi import FastAPI, File, UploadFile
# import pandas as pd

# app = FastAPI(title="Copilot Finance API") # Initialize FastAPI app with title

# @app.get("/") # Define root endpoint for health check
# def root():
#     return {"message": "Welcome to Copilot for Personal Finance API"}

# @app.post("/upload") # Define endpoint for file upload and processing
# async def upload(file: UploadFile = File(...)): # Upload file parameter
#     # Read CSV into pandas DataFrame
#     df = pd.read_csv(file.file)
#     # For now, just return simple metadata
#     return {"rows": len(df), "columns": list(df.columns)} # Return number of rows and column names
