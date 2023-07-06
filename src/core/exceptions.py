from fastapi.responses import JSONResponse


async def redis_connection_exception_handler(request, exc):
    return JSONResponse(
        status_code=503, content={"detail": "Redis service unavailable"}
    )


async def es_connection_exception_handler(request, exc):
    return JSONResponse(
        status_code=503,
        content={"detail": "ElasticSearch service unavaliable"},
    )
