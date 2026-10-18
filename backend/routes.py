from fastapi import APIRouter, WebSocket

from controllers import authController as auth
from controllers import ticketController as ticket
from controllers import userController as user
from controllers import customerController as customer
from controllers import metricsController as metrics

routes = APIRouter()

routes.include_router(auth.router, prefix='/auth')
routes.include_router(ticket.router, prefix='/tickets')
routes.include_router(user.router, prefix='/user')
routes.include_router(customer.router, prefix='/customer')
routes.include_router(metrics.router, prefix='/metrics')