from fastapi import FastAPI
from threading import Thread

from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, crypto, payments
from app.helpers.payments import check_payments


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
app.include_router(auth.router)
app.include_router(crypto.router)
app.include_router(payments.router)

Thread(target=check_payments).start()


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
def docs():
    return RedirectResponse(url='/docs')
