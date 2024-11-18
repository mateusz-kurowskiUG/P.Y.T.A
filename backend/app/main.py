from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import Settings
from app.core.utils.init_db import InitDB
from app.v1.auth import auth_router

setting = Settings()

InitDB()


def get_application() -> FastAPI:
	_app = FastAPI(title="P.Y.T.A", debug=setting.debug, root_path="/api")

	_app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	_app.include_router(auth_router)

	return _app


app = get_application()

if __name__ == "__main__":
	import uvicorn

	uvicorn.run("main:app", host="0.0.0.0", port=setting.port, reload=setting.debug)
