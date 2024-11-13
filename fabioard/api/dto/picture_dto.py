from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime

from fabioard.domain.business.picture import Picture


class PictureDto(BaseModel):
    url: str
    date: DateTime
    location: str

    @staticmethod
    def from_business(picture: Picture) -> "PictureDto":
        return PictureDto(url=picture.url, date=picture.date, location=picture.location)
