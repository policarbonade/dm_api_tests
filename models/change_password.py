from pydantic import BaseModel, Field, ConfigDict


class ChangePassword(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    login: str = Field(...)
    token: str = Field(...)
    old_password: str = Field(..., alias='oldPassword')
    new_password: str = Field(..., alias='newPassword')
