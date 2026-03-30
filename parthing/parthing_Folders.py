from pydantic import BaseModel, Field, model_validator, field_validator, ValidationError
from utils import color


class BaseConfig(BaseModel):
    Width: int = Field(..., ge=2)
    Height: int = Field(..., ge=2)
    Entry: tuple[int, int]
    Exit: tuple[int, int]
    Output_file: str = Field("dont_fgt_me_maze.txt")
    Perfect: bool = Field(False)

    @field_validator("Entry", "Exit", mode="before")
    @classmethod
    def parse_string_to_tuple(cls, value) -> tuple:
        if isinstance(value, str):
            parts = value.split(",")
            if len(parts) != 2:
                raise ValueError(color("value must have a ','", 255, 100, 100))
            try:
                a, b = int(parts[0]), int(parts[1])
            except ValueError:
                raise ValueError(color("value can't be a float", 255, 100, 100))
            if a < 0 or b < 0:
                raise ValueError(color("the value can be negative", 255, 100, 100))
            return (a, b)
        return value

    @model_validator(mode="after")
    def parth_validation(self) -> "BaseConfig":
        if self.Entry == self.Exit:
            raise ValueError(
                color("the entry and exit can't be on the same place", 255, 150, 150)
            )
        if self.Entry[0] >= self.Width or self.Exit[0] >= self.Width:
            raise ValueError(
                color("the entry or exit can't be over the width map", 255, 150, 150)
            )
        if self.Entry[1] >= self.Height or self.Exit[1] >= self.Height:
            raise ValueError(
                color("the entry or exit can't be over the height map", 255, 150, 150)
            )

        return self


def parth_file_path(file_path: str) -> dict | None:
    config_dict = {}
    required_keys = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE"}
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.count("=") != 1:
                    raise ValueError(color(f"invalif line: {line}", 255, 150, 150))

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
    if config_dict == None:
        return None

    try:
        config_return = BaseConfig(
            Width=int(config_dict["WIDTH"]),
            Height=int(config_dict["HEIGHT"]),
            Entry=config_dict["ENTRY"],
            Exit=config_dict["EXIT"],
            Output_file=config_dict.get("OUTPUT_FILE", "dont_fgt_me_maze.txt"),
            Perfect=config_dict.get("PERFECT", "False").lower() == "true",
        )
    except ValidationError as e:
        print(color("Error : ", 250, 70, 70) + color(f"{e}", 200, 100, 100))
        return None
    except ValueError as e:
        print(color("Error : ", 250, 70, 70) + color(f"{e}", 200, 100, 100))
        return None

    return config_return
