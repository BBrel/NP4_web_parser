from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pydantic import Field

secure_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'secure')

class PostgresConfig(BaseSettings):
    host: str
    port: int
    database: str
    userr: str
    password: str

    model_config = SettingsConfigDict(env_file=os.path.join(secure_dir, 'bdd.env'))

    @property
    def connection_string(self):
        return f'postgresql://postgres:Brelgin_4@db:5432/web_api'


class Settings(BaseSettings):
    postgres: PostgresConfig = Field(PostgresConfig())
    path_root: str = Field(os.path.dirname(os.path.abspath(__file__)))


settings = Settings()

if __name__ == '__main__':
    print(settings.model_dump())
