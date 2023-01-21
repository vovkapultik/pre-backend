from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str

    MONGODB_URI: str
    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_DATABASE_NAME: str

    ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE: int
    REFRESH_TOKEN_EXPIRE: int

    WEB3_NETWORK_NAME: str
    WEB3_INFURA_PROJECT_ID: str
    ADMIN_ADDRESS: str
    ADMIN_SEED_PHRASE: str
    PAYMENT_CONTRACT_ADDRESS: str
    PHYGITAL_CONTRACT_ADDRESS: str

    WFP_BASE_URL: str
    WFT_API_BASE_URL: str
    WFP_MERCHANT_LOGIN: str
    WFP_MERCHANT_KEY: str
    WFP_DOMAIN_NAME: str
    WFP_PAYMENT_CONFIRMATION_ROUTE: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
