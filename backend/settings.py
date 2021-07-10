from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "HEART WEB"
    SECRET_KEY: str = "0f2dff302e7f48df91fc3f962590fc91"
    ALGORITHM: str = "HS256"
    BASE_URL: AnyHttpUrl = "http://localhost:8000"

    ACCESS_TOKEN_EXPIRE_MINUTES = 30


conf = Settings()
