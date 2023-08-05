from pydantic import BaseModel
from typing import Optional

class Locations(BaseModel):
    query: str = ""
    businessType: str = ""
    listingType: str = ""
    constructionStatus: str = ""

class Listings(BaseModel):
    categoryPage: str = ""
    businessType: str = ""
    listingType: str = ""
    constructionStatus: str = ""
    addressType: str = ""
    addressStreet: str = ""
    addressNeighborhood: str = ""
    addressZone: str = ""
    addressCity: str = ""
    addressState: str = ""
    addressLocationId: str = ""
    addressPointLat: str = ""
    addressPointLon: str = ""
    ammount: str = "0"
    unit_type: dict = {}
    sheet_name: Optional[str] = ""
    sheet_share_users: Optional[list] = []