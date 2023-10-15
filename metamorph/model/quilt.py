import pydantic
from typing import List


class LoaderVersion(pydantic.BaseModel):
    separator: str
    build: int
    maven: str
    version: str


class LoaderVersions(pydantic.BaseModel):
    __root__: List[LoaderVersion]
