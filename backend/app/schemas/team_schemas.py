from pydantic import BaseModel

class CreateTeam(BaseModel):
    team_name: str

class JoinTeam(BaseModel):
    team_name: str
