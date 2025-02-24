from typing import Optional, Self

import attrs  # type: ignore


@attrs.define
class ParcelData:
    label: str = attrs.field(default="", metadata={"json": "label"})
    order: int = attrs.field(default=0, metadata={"json": "order"})
    cancel: int = attrs.field(default=0, metadata={"json": "cancell"})

    @classmethod
    def from_json(cls, data: dict[str, str | int]) -> Self:
        return cls(
            label=data.get("label", ""),
            order=data.get("order", 0),
            cancel=data.get("cancell", 0),
        )  # type: ignore


@attrs.define
class ParcelHistory:
    user_name: Optional[str] = attrs.field(default=None, metadata={"json": "user_name"})
    courier_data: list[ParcelData] = attrs.field(
        default=None, metadata={"json": "courierData"}
    )
    source: str = attrs.field(default=None, metadata={"json": "source"})

    @classmethod
    def from_json(cls, data: dict[str, str | list[ParcelData]]) -> Self:
        return cls(
            user_name=data.get("user_name"),
            courier_data=[
                ParcelData.from_json(item)
                for item in data.get("courierData", [])  # type: ignore
            ],
            source=data.get("source"),
        )
