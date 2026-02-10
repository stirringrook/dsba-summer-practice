from pydantic import BaseModel


class Settings(BaseModel):
    """Project configuration.

    The internship prototype uses a local SQLite database file for portability
    and reproducibility.
    """

    database_url: str = "sqlite:///./reviewpulse.db"


settings = Settings()
