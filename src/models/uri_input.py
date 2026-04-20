from pydantic import BaseModel

class UriInput(BaseModel):
    uri: str