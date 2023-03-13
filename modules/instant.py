from pydantic import BaseModel
from typing import Union

class CanHo(BaseModel):
    project_name: str                                       # require
    real_estate_type: Union[str, None] = "căn hộ chung cư"
    street: Union[str, None] = None
    ward: Union[str, None] = None
    district: Union[str, None] = None
    city: str                                               # require
    n_bedroom: Union[int, None] = 2
    area: Union[float, None] = None
    floor: Union[int, None] = None
    direction: Union[str, None] = None
    rate_direction: Union[float, None] = None
    corner: Union[str, None] = None
    rate_corner: Union[float, None] = None
