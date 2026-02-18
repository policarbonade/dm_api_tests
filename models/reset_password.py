from pydantic import BaseModel, Field, ConfigDict


class ResetPassword(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(...)
    email: str = Field(...)
