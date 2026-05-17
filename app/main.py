from fastapi import FastAPI

"""
This is the main entry point for the PatchPilot AI FastAPI application.
It initializes the FastAPI app and defines basic routes.
"""

app = FastAPI(title="PatchPilot AI")


@app.get("/")
async def root():
    """
    Root endpoint for the PatchPilot AI API.
    Returns a simple message to indicate the service is running.
    """
    return {"message": "PatchPilot AI Running"}