from fastapi import APIRouter
from .routemodels import Locations, Listings
# from scraper.webscraper import *
# from question_answer.qa import *
from crawler.algoz_crawler import ZapCrawler
import time
import json

# class Locations(BaseModel):
    # query: str = ""
    # businessType: str = ""
    # listingType: str = ""
    # constructionStatus: str = ""

# class Listings(BaseModel):
#     categoryPage: str = ""
#     businessType: str = ""
#     listingType: str = ""
#     constructionStatus: str = ""
#     addressType: str = ""
#     addressStreet: str = ""
#     addressNeighborhood: str = ""
#     addressZone: str = ""
#     addressCity: str = ""
#     addressState: str = ""
#     addressLocationId: str = ""
#     addressPointLat: str = ""
#     addressPointLon: str = ""
#     ammount: str = "0"
#     unit_type: dict = {}
#     sheet_name: Optional[str] = ""
#     sheet_share_users: Optional[list] = []

class Handler:
    def __init__(self):
        router = APIRouter()
        self.router = router

        @router.post("/locations")
        async def get_locations(params: Locations, _debug=False):
            start_time = time.time()
            search_input = {
                "query": params.query,
                "businessType": params.businessType,
                "listingType": params.listingType,
                "constructionStatus": params.constructionStatus
            }
            zapClass = ZapCrawler(_debug=True)
            locations_res = zapClass.get_locations(search_input=search_input, _retry=2)
            if _debug:
                locations_res["took"] = time.time() - start_time
            return locations_res
        
        @router.post("/listings")
        async def get_listings(params: Listings, _debug=True):
            start_time = time.time()
            search_input = {
                "categoryPage": params.categoryPage,
                "businessType": params.businessType,
                "listingType": params.listingType,
                "constructionStatus": params.constructionStatus,
                "addressStreet": params.addressStreet,
                "addressNeighborhood": params.addressNeighborhood,
                "addressType": params.addressType,
                "addressZone": params.addressZone,
                "addressCity": params.addressCity,
                "addressState": params.addressState,
                "addressLocationId": params.addressLocationId,
                "addressPointLat": params.addressPointLat,
                "addressPointLon": params.addressPointLon,
                "ammount": params.ammount,
                "unit_type": params.unit_type
            }
            if params.ammount != "0":
                search_input['sheet_name'] = params.sheet_name
                search_input['sheet_share_users'] = params.sheet_share_users
            
            zapClass = ZapCrawler(_debug=True)
            listings_res = zapClass.get_listings(search_input=search_input, _retry=2)
            if _debug:
                listings_res["took"] = time.time() - start_time
            return listings_res