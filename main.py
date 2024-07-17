from collections import defaultdict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests

from src.routers.pin import pin

from src.misc.helpers.helper_utils import compile_email_formats_mjml, generate_routes_json
from src.routers import company, misc, encrypt_decrypt
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status

from src.routers.home import router as home_router
from src.routers.accounts import router as accounts_router
from src.routers.admin import router as admin_router
from src.routers.user import router as user_router
from src.routers.franchise import router as franchise_router
from src.routers.pin import router as pin_router
from src.routers.wallet import router as wallet_router
from src.routers.withdrawal import router as withdrawal_router
from src.routers.security import router as security_router
from src.routers.team import router as team_details_router
from src.routers.investment import router as investment_router
from src.routers.topup import router as topup_router
from src.routers.docs import router as docs_router
from src.routers.support import router as support_router
from src.routers.income import router as income_router
from src.routers.repurchase import router as repurchase_router
from src.routers.setup import router as setup_router
from src.utilities.utils import config

app = FastAPI(title="MCT API", docs_url='/docs' if config['IsDevelopment'] else None, redoc_url='/redoc' if config['IsDevelopment'] else None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def custom_form_validation_error(request, exc):
    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(filtered_loc)
        reformatted_message[field_string].append(msg)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {"detail": "Invalid request", "errors": reformatted_message}
        ),
    )

app.include_router(home_router)
app.include_router(company.router)

app.include_router(accounts_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(franchise_router)
app.include_router(pin_router)
app.include_router(wallet_router)
app.include_router(withdrawal_router)
app.include_router(security_router)
app.include_router(team_details_router)
app.include_router(investment_router)
app.include_router(topup_router)
app.include_router(docs_router)
app.include_router(support_router)
app.include_router(income_router)
app.include_router(repurchase_router)
app.include_router(pin.router)
app.include_router(misc.router)


if config['IsDevelopment']:
    app.include_router(setup_router)
    app.include_router(encrypt_decrypt.router)
    generate_routes_json()


app.mount("/static", StaticFiles(directory="static"), name="static")

if config["CompileEmails"] or not config['IsDevelopment']:
    compile_email_formats_mjml()


@app.get('/')
def status():
    return 'Api is working!'
