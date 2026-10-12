from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    result_type: str | None = None
    limit: int = 20
