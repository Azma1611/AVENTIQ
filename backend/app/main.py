from fastapi import FastAPI

app = FastAPI(
    title="AVENTIQ API",
    description="Backend services for AVENTIQ - From Ambition to Achievement",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": "AVENTIQ API",
        "version": "0.1.0",
    }

