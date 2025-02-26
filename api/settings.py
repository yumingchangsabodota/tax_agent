from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.healthcheck import healthcheck
from api.routers.tax_agent import tax_agent

from api.auth.poc_auth import poc_auths


tags = [
    {
        'name': 'Utilities',
        'description': 'Backend Utilities API'
    },
    {
        'name': 'Tax Agent',
        'description': 'Tax Agent'
    }
]


origins = ["*"]
app = FastAPI(title="Tax Agent Backend API",
              openapi_tags=tags,
              version="0.1.0",
              root_path="/api",
              docs_url="/docs"
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(healthcheck.router, tags=["Utilities"])
app.include_router(tax_agent.router,
                   prefix="/tax-agent", tags=["Tax Agent"], dependencies=poc_auths)
