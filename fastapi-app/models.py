from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal


# Schema field model
class FieldSchema(BaseModel):
    name: str
    type: Literal["string", "int32", "float", "bool"]
    facet: Optional[bool] = False
    optional: Optional[bool] = False
    index: Optional[bool] = True
    sort: Optional[bool] = False

# Main collection schema
class CollectionSchema(BaseModel):
    name: str
    fields: List[FieldSchema]
    default_sorting_field: Optional[str] = None  

    @validator("name")
    def name_must_be_alphanumeric(cls, v):
        if not v.isidentifier():
            raise ValueError("Collection name must be a valid identifier (no spaces, special chars)")
        return v