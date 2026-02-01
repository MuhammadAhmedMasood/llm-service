from fastapi import FastAPI
from api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Enterprise LLM Service",
    version="1.0.0",
    description="API-first service for controlled LLM usage"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                  "https://llm-service-ui-ahmed.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["POST","GET"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/ready")
def readiness_check():
    return {"ready": True}
