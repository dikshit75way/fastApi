from fastapi import FastAPI
from app.core.config import settings
from app.modules.user.route import router as auth_router
from app.modules.project.routes import router as project_router
from app.modules.purchase.routes import router as purchase_router
from app.modules.wallet.routes import router as wallet_router
from app.modules.reviews.routes import router as review_router
from app.modules.project_module.routes import router as project_module_router

app = FastAPI(
    title="Market Place API",
    description="Market Place API",
    version="0.0.1",
)

# Include routers
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(purchase_router)
app.include_router(wallet_router)
app.include_router(review_router)
app.include_router(project_module_router)

@app.get("/health" , tags=["Health"])
async def health():
    return {"status": "ok" , "env": settings.ENV}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    