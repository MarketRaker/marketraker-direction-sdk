from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.Routers import MarketDirection_Router

app = FastAPI()

app.include_router(MarketDirection_Router.router, prefix="/marketraker")

@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """
    Root endpoint that redirects to the /docs endpoint.

    Returns:
        RedirectResponse: The redirect response.

    """
    return RedirectResponse(url="/docs")