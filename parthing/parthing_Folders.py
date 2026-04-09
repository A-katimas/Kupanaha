from pydantic import (
    BaseModel,
    Field,
    model_validator,
    field_validator,
    ValidationError,
)
from utils import color
from typing import Any


class BaseConfig(BaseModel):
    WIDTH: int = Field(..., ge=2)
    HEIGHT: int = Field(..., ge=2)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str = Field("dont_fgt_me_maze.txt")
    PERFECT: bool = Field(False)
    SEED: int | None = None

    @field_validator("ENTRY", "EXIT", mode="before")
    @classmethod
    def parse_string_to_tuple(
        cls, value: tuple[int, int] | str
    ) -> tuple[int, int]:
        if isinstance(value, str):
            parts = value.split(",")
            if len(parts) != 2:
                raise ValueError(color("value must have a ','", 255, 100, 100))
            try:
                a, b = int(parts[0]), int(parts[1])
            except ValueError:
                raise ValueError(
                    color("value can't be a float", 255, 100, 100)
                )
            if a < 0 or b < 0:
                raise ValueError(
                    color("the value can be negative", 255, 100, 100)
                )
            return (a, b)
        return value

    @model_validator(mode="after")
    def parth_validation(self) -> "BaseConfig":
        if self.ENTRY == self.EXIT:
            raise ValueError(
                color(
                    "the entry and exit can't be on the same place",
                    255,
                    150,
                    150,
                )
            )
        if self.ENTRY[0] >= self.WIDTH or self.EXIT[0] >= self.WIDTH:
            raise ValueError(
                color(
                    "the entry or exit can't be over the width map",
                    255,
                    150,
                    150,
                )
            )
        if self.ENTRY[1] >= self.HEIGHT or self.EXIT[1] >= self.HEIGHT:
            raise ValueError(
                color(
                    "the entry or exit can't be over the height map",
                    255,
                    150,
                    150,
                )
            )
        return self


def parth_file_path(file_path: str) -> dict[str, Any] | None:
    config_dict = {}
    required_keys = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE"}
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.count("=") != 1:
                    raise ValueError(
                        color(f"invalif line: {line}", 255, 150, 150)
                    )

                key, value = line.split("=", 1)
                config_dict[key.strip().upper()] = value.strip()

        missing = required_keys - config_dict.keys()
        if missing:
            raise ValueError(color(f"Missing keys: {missing}", 255, 150, 150))
    except ValueError as e:
        print(color("Error : ", 250, 70, 70) + color(f"{e}", 200, 100, 100))
        return None

    return config_dict


def parth(file_path: str) -> BaseConfig | None:
    config_dict = parth_file_path(file_path)
    if config_dict is None:
        return None

    try:
        config_return = BaseConfig(**config_dict)
    except ValidationError as e:
        print(color("Error : ", 250, 70, 70) + color(f"{e}", 200, 100, 100))
        return None
    except ValueError as e:
        print(color("Error : ", 250, 70, 70) + color(f"{e}", 200, 100, 100))
        return None

    return config_return
