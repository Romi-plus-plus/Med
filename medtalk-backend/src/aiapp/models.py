from sqlmodel import Field, SQLModel


class BaseCount(SQLModel):
    key: str = Field(primary_key=True)
    value: int = Field(default=0, index=True)


class WordCount(BaseCount, table=True):
    ...


class IntentCount(BaseCount, table=True):
    ...


class EntityCount(BaseCount, table=True):
    # group: str = Field(primary_key=True)
    ...