from app.models.base_model import BaseModel
import re

class Review(BaseModel):
    def __init__(self, userId, placeId, rating, comment, upload_image =None):
        super().__init__()
        self.userId = userId
        self.placeId = placeId
        self.rating = rating
        self.comment = comment
        self.upload_image  = upload_image

    """ Getters and Setters """
    """ Rating: rating must be between 1 and 5 stars"""
    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Rating must be a number (int or float)")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5 stars")
        self._rating = value

    """ Comment """
    @property
    def comment(self):
        return self._comment
    
    @comment.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Comment name must be a string")
        value = value.strip()
        if len(value) == 0:
            raise ValueError("Comment cannot be empty.")
        if len(value) > 100:
            raise ValueError("Comment must not be over 100 characters")
        self._comment = value

    """ Upload image """
    @property
    def upload_image(self):
        return self._upload_image

    @upload_image.setter
    def upload_image(self, images):
        if not isinstance(images, list):
            raise TypeError("upload_image must be a list of image files.")
        if len(images) > 3:
            raise ValueError("You can upload up to 3 images only.")
        
        validated_images = []
        for img in images:
            try:
                pil_img = PILImage.open(img)
                if pil_img.format not in self.ALLOWED_FORMATS:
                    raise ValueError(f"Image format must be JPEG or PNG, got {pil_img.format}")
                validated_images.append(img)
            except Exception:
                raise ValueError("Each upload must be a valid image file (JPEG or PNG).")
        
        self._upload_image = validated_images
    
    """ save """
    # method to save the input using basemodel
    def save(self):
        data = super().save()
        data.update(
            {
            "userId": self.userId,
            "placeId": self.placeId,
            "rating": self.rating,
            "comment": self.comment,
            "upload_image": self.upload_image       
        })
        return data
