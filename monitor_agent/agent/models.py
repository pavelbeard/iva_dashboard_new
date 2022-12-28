from typing import List

from pydantic import BaseModel


class HashableModel(BaseModel):
    def __hash__(self):
        return hash((type(self), ) + tuple(self.__dict__.values()))


class Target(BaseModel):
    host: str
    port: int
    username: str
    password: str
    cmd: str


class Targets(BaseModel):
    hosts: List[Target]
