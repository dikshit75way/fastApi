from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import iterate_in_threadpool
import json

from app.core.config import settings
from app.modules.user.route import router as auth_router
from app.modules.project.routes import router as project_router
from app.modules.purchase.routes import router as purchase_router
from app.modules.wallet.routes import router as wallet_router
from app.modules.reviews.routes import router as review_router
from app.modules.project_module.routes import router as project_module_router
from app.modules.payment.routes import router as payment_router

app = FastAPI(
    title="Market Place API",
    description="Market Place API",
    version="0.0.1",
)

@app.middleware("http")
async def wrap_response(request: Request, call_next):
    response = await call_next(request)
    
    # Skip wrapping for docs, openapi, and health
    if any(path in request.url.path for path in ["/docs", "/openapi.json", "/health", "/redoc"]):
        return response

    if response.status_code < 400:
        try:
            # We must capture the response body carefully in FastAPI middleware
            response_body = [section async for section in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            
            # Combine body parts and parse JSON
            full_body = b"".join(response_body)
            data = json.loads(full_body.decode())
            
            # If already wrapped, just return
            if isinstance(data, dict) and "success" in data:
                return response

            return JSONResponse(
                status_code=response.status_code,
                content={
                    "success": True,
                    "data": data
                }
            )
        except Exception:
            # Fallback for non-JSON or other errors
            return response
            
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(purchase_router)
app.include_router(wallet_router)
app.include_router(review_router)
app.include_router(project_module_router)
app.include_router(payment_router)

@app.get("/health" , tags=["Health"])
async def health():
    return {"status": "ok" , "env": settings.ENV}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    