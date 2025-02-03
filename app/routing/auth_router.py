from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.database.models.models import User
from app.database.connector import get_session
from app.database.models.models import User
from app.exc.bad_email import BadEmail
from app.schems.request.access import AccessRequest
from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
auth_router = APIRouter(prefix="/access", tags=["System Access"])


@auth_router.post("/auth")
async def auth(request: AccessRequest, session: AsyncSession = Depends(get_session)):
    result = await UserService(session).auth(request)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return {
        "userId": result.value}
    

@auth_router.post("/register")
async def register(registerRequest: AccessRequest, session: AsyncSession = Depends(get_session)):
    registered = await UserService(session).register(registerRequest)
    if not registered.success:
        raise HTTPException(status_code=400, detail=registered.error)
    return {
        "message": registered.value
    }