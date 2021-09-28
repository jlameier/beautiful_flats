# building a data class for flats, houses, buy and rent
# making some methods and validation/sanitation
# laster think about writing this to postgres

from typing import List, Optional
import pydantic
from datetime import datetime


class PriceRangeError(Exception):
    # custom error when price is out of range
    def __init__(self, value: str, message: str) -> None:
        self.message = message
        self.value = value
        super().__init__(message)


class RealEstate(pydantic.BaseModel):
    id: str
    space: int
    postID: str
    rent: bool
    price: int
    address: Optional[str]
    headline: Optional[str]
    num_rooms: Optional[int]
    long_description: Optional[str]
    found_date: Optional[datetime]

    @pydantic.validator("id")
    @classmethod
    def id_validate(cls, value):
        assert value.isalnum()
        return value


    @pydantic.validator("space")
    @classmethod
    def space_validate(cls, value):
        if not (0 < value < 10000):
            raise Exception("space out of range")
        elif type(value) != int:
            raise Exception("space is bad type")
        return value


    @pydantic.validator("postID")
    @classmethod
    def postID_validate(cls, value):
        if len(value) != 5:
            raise Exception("postID is not 5 digits ")
        if len([c for c in value if c in "0123456789"]) < len(value):
            raise Exception("postID contains bad characters ")
        return value


    @pydantic.validator("price")
    @classmethod
    def price_validate(cls, value, values, **kwargs):
        if values['rent'] == False:  # buying todo not good style. if assertion doesnt raise an error, this will occur as key error
            if value < values['space'] * 40:  # cheap price to buy
                raise PriceRangeError(value=value, message=" buying value of {name} is likely too small".format(name=values['id']))
            elif value > values['space'] * 8000:  # price in munic
                raise PriceRangeError(value=value, message=" buying value of {name} is likely too big".format(name=values['id']))
            return value

        else:  # Rental
            if value < values['space'] * 3: # cheap rental
                raise PriceRangeError(value=value, message=" rental value of {name} is likely too small".format(name=values['id']))
            elif value > values['space'] * 40: # expensive rental
                raise PriceRangeError(value=value, message=" rental value of {name} is likely too big".format(name=values['id']))
            return value


"""
found_online = {'id': 1, 'space': 110, 'postID': '01324',  'rent': False,'price': 300000, 'headline': 'buy me hard!',
                'found_date': datetime.today()}
found_online2 = {'id': 2, 'space': 10, 'postID': '01223', 'price': 400, 'rent': True, 'headline': 'buy me hard!'}

new_object = RealEstate(**found_online)
new_object2 = RealEstate(**found_online2)
print(new_object2)
"""