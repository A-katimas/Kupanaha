from pydantic import (
    BaseModel,
    Field,
    model_validator,
    field_validator,
    ValidationError,
)
from utils import color
from typing import Any
from maze.maker import THEMES

algodispo = {"prims": 1, "backtrack": 1, "Prims": 1, "BackTrack": 1}


class BaseConfig(BaseModel):
    """
    Configuration model for maze generation.

    This class validates and stores all parameters required to generate a maze,
    including dimensions, entry/exit points, algorithm selection, and output
    options.
    """

    WIDTH: int = Field(..., ge=2)
    HEIGHT: int = Field(..., ge=2)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str = Field("dont_fgt_me_maze.txt")
    PERFECT: bool = Field(False)
    SEED: int | None = None
    THEME: str = Field("white")
    ALGO: str = Field("BackTrack")

    @field_validator("ENTRY", "EXIT", mode="before")
    @classmethod
    def parse_string_to_tuple(
        cls, value: tuple[int, int] | str
    ) -> tuple[int, int]:
        """
        Convert a string representation of coordinates into a tuple.

        Accepts values like "x,y" and converts them into (x, y).
        Ensures both values are integers and non-negative.

        Args:
            value: A tuple of integers or a string in the format "x,y".

        Returns:
            A tuple of two integers.

        Raises:
            ValueError: If the format is invalid or values are not valid
            integers.
        """
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
        """
        Perform cross-field validation after model initialization.

        Ensures:
        - ENTRY and EXIT are not the same
        - ENTRY and EXIT are within the maze boundaries

        Returns:
            The validated BaseConfig instance.

        Raises:
            ValueError: If any validation rule is violated.
        """
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
    """
    Parse a configuration file into a dictionary.

    The file must contain key=value pairs, one per line.
    Lines starting with '#' and empty lines are ignored.
    Keys are normalized to uppercase.

    Required keys:
        - WIDTH
        - HEIGHT
        - ENTRY
        - EXIT
        - OUTPUT_FILE

    Args:
        file_path: Path to the configuration file.

    Returns:
        A dictionary containing configuration values, or None if an error
        occurs.

    Raises:
        ValueError: If the file format is invalid or required keys are missing.
    """
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
    """
    Load and validate a configuration file into a BaseConfig object.

    This function:
    1. Parses the file into a dictionary
    2. Validates it using the BaseConfig model
    3. Verifies that the selected THEME and ALGO exist

    Args:
        file_path: Path to the configuration file.

    Returns:
        A validated BaseConfig instance, or None if an error occurs.

    Raises:
        ValidationError: If the configuration does not satisfy BaseConfig
        constraints.
        KeyError: If THEME or ALGO is not recognized.
    """
    config_dict = parth_file_path(file_path)
    if config_dict is None:
        return None

    try:
        config_return = BaseConfig(**config_dict)
        THEMES[config_return.THEME]
        algodispo[config_return.ALGO]

    except ValidationError as e:
        print(color("Error : ", 250, 70, 70) + color(f"{e}", 200, 100, 100))
        return None
    except ValueError as e:
        print(color("Error : ", 250, 70, 70) + color(f"{e}", 200, 100, 100))
        return None
    except KeyError as e:
        print(
            color("Error in key: ", 250, 70, 70) + color(f"{e}", 200, 100, 100)
        )
        return None

    return config_return
