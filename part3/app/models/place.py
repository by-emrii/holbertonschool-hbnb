from app.models.base_model import BaseModel
""" Class Place represents to Place model in BL"""


class Place(BaseModel):
    def __init__(
            self, owner_id, title, price,
            address, latitude, longitude, image_url=None, amenity_ids=None, description=False
    ):
        super().__init__()
        self.owner_id = owner_id
        self.title = title
        self.description = description
        self.price = price
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.image_url = image_url
        self.amenity_ids = amenity_ids or []

    """Getter and Setter"""
    """ Owner ID """
    @property
    def owner_id(self):
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        if isinstance(value, int):    # in case of passed id is int
            value = str(value)
        if not isinstance(value, str):
            raise TypeError("Owner ID must be a string")
        if not value.strip():
            raise ValueError("Owner ID cannot be empty")
        self._owner_id = value.strip()

    """ Place title """
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        value = value.strip()
        if len(value) < 3:
            raise ValueError("Title must be at least 3 characters long")
        if len(value) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        self._title = value

    """ Description"""
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        value = value.strip()
        if len(value) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")
        self._description = value

    """ Price """
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (float)):
            raise TypeError("Price must be a positive number")
        if value < 0:
            value = float(value)
            raise ValueError("Price must be positive number")
        self._price = value

    """ Address """
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not isinstance(value, str):
            raise TypeError("Address must be a string")
        value = value.strip()
        if len(value) < 5 or len(value) > 200:
            raise ValueError("Address must be between 5 and 200 characters")
        self._address = value

    """ Latitude """
    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (float)):
            raise TypeError("Latitude must be a number")
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        self._latitude = float(value)

    """ Longitude """
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (float)):
            raise TypeError("Longitude must be a number")
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        self._longitude = float(value)

    """ Image URL """
    @property
    def image_url(self):
        return getattr(self, "_image_url", None)

    @image_url.setter
    def image_url(self, value):
        if value is None or str(value).strip() == "":
            self._image_url = None
            return
        if not isinstance(value, str):
            raise TypeError("image_url must be a string")
        v = value.strip()
        # 可选校验：只允许 http(s) 前缀
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("image_url must start with http(s)://")
        self._image_url = v

    """ Amenity_ids (List[str])"""
    @property
    def amenity_ids(self):
        return self._amenity_ids

    @amenity_ids.setter
    def amenity_ids(self, value):
        if not isinstance(value, list):
            raise TypeError("Amenity IDs must be a list")

        # keep the amenity id as string and remove duplication
        cleaned = list(dict.fromkeys(str(v).strip() for v in value if v))
        self._amenity_ids = cleaned
