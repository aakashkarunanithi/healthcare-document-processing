from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from models.api_response_dto import APIResponse
from models.uri_input import UriInput
from utils.exceptions.custom_app_exception import Custom_App_Exception
from utils.exceptions.error_codes import ErrorCode
from utils.exceptions.http_status import HttpStatusCode
from services.service import service
from utils.logger import logger

router = APIRouter(prefix="/health_care/api/v1")

@router.post("/invoice_process")
async def invoice_process_router(
    request: UriInput = Body(...)
) -> JSONResponse:
    logger.info(f"Received invoice process request with URI: {request.uri}")
    try:
        result = await service.invoice_process_service(request)
        logger.info("invoice processed successfully")
        data =APIResponse(
            data=result,
            code=HttpStatusCode.OK,
            message ='Health record extracted successfully'
        )
        return JSONResponse(
            content= data.to_dict(),
            status_code=data.code,
        )
    except Custom_App_Exception:
        raise
    except Exception as e:
        raise Custom_App_Exception(
            message=f"Router error: {str(e)}",
            code=ErrorCode.INTERNAL_SERVER_ERROR,
            status_code=HttpStatusCode.INTERNAL_SERVER_ERROR
        )