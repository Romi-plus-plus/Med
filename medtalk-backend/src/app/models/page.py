from sqlmodel import Field, SQLModel

class PageParams(SQLModel):
    sort_by: str | None = Field(default=None, description="Key on sorting")
    desc: bool = Field(default=False, description="Whether descending")
