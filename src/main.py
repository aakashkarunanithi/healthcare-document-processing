import uvicorn
# ==================== FASTAPI IMPORTS ====================
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routers.router import router
from models.api_response_dto import APIResponse, Error
from utils.exceptions.custom_app_exception import Custom_App_Exception
from utils.exceptions.error_codes import ErrorCode
from utils.exceptions.http_status import HttpStatusCode
from utils.logger import logger
from utils.get_create_update_blueprint import get_create_update_blueprint
from settings import config
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Application starting up...")
    blueprint_arn=get_create_update_blueprint.get_or_create_blueprint()
    get_create_update_blueprint.update_project_with_blueprint(config.project_arn,blueprint_arn)
    yield
    logger.info("Application shutting down")

# ==================== FASTAPI APPLICATION INITIALIZATION ====================
app = FastAPI(

    title="Health Care API",
    description="Health Care API to extract data from document",
    version="1.0.0",
    lifespan=lifespan
)

# SQ_1.18 to 1.19 fetch_groups
# ==================== MIDDLEWARE CONFIGURATION ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router)

# ==================== EXCEPTION HANDLERS ====================
@app.exception_handler(Custom_App_Exception)
async def Custom_App_Exception_handler(request: Request, exc: Custom_App_Exception) -> JSONResponse:
    api_response = exc.to_api_response()
    return JSONResponse(
        status_code=exc.status_code,
        content=api_response.to_dict()
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = []
    for error in exc.errors():
        errors.append(Error(
            code=ErrorCode.VALIDATION_ERROR,
            message=f"{error['loc'][-1]}: {error['msg']}"
        ))
    
    api_response = APIResponse(
        data=None,
        errors=errors,
        code=HttpStatusCode.UNPROCESSABLE_ENTITY
    )
    
    return JSONResponse(
        status_code=HttpStatusCode.UNPROCESSABLE_ENTITY,
        content=api_response.to_dict()
    )

# ==================== APPLICATION ENTRY POINT ====================
if __name__ == "__main__":
    """
    Main entry point for running the FastAPI application locally.
    """
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )