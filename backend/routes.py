from fastapi import APIRouter, WebSocket

from controllers import authController as auth

routes = APIRouter()

routes.include_router(auth.router, prefix='/auth')
