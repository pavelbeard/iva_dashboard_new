from typing import List

from pydantic import BaseModel


class HashableModel(BaseModel):
    def __hash__(self):
        return hash((type(self), ) + tuple(self.__dict__.values()))


class Target(BaseModel):
    address: str
    port: int
    username: str
    password: str


class PackageIn(BaseModel):
    hosts: List[Target]
