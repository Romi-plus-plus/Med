from pydantic import BaseSettings


class Settings(BaseSettings):
    API_STR: str = "/api"

    PROJECT_NAME = "medtalk-ai"

    class Config:
        case_sensitive = True


settings = Settings()
print(settings)
