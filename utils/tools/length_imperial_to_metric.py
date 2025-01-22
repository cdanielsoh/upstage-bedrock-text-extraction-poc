from utils.tool import Tool


class LengthImperialToMetric(Tool):
    @staticmethod
    def invoke(length: float, unit: str, target_unit: str) -> float:
        # First convert to inches
        to_inches = {
            "in": 1,
            "ft": 12,
            "yd": 36,
            "mi": 63360
        }

        # Then convert inches to target metric unit
        to_metric = {
            "mm": 25.4,
            "cm": 2.54,
            "m": 0.0254,
            "km": 0.0000254
        }

        if unit not in to_inches:
            raise ValueError(f"Unsupported imperial unit: {unit}")
        if target_unit not in to_metric:
            raise ValueError(f"Unsupported metric unit: {target_unit}")

        inches = length * to_inches[unit]
        return inches * to_metric[target_unit]

    @staticmethod
    def get_info():
        return {
            "type": "function",
            "function": {
                "name": "length_imperial_to_metric",
                "description": "Convert the given length in imperial units to specified metric unit",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "length": {
                            "type": "number",
                            "description": "The length value to convert"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["in", "ft", "yd", "mi"],
                            "description": "The imperial unit to convert from"
                        },
                        "target_unit": {
                            "type": "string",
                            "enum": ["mm", "cm", "m", "km"],
                            "description": "The metric unit to convert to"
                        }
                    },
                    "required": ["length", "unit", "target_unit"]
                },
                "returns": {
                    "type": ["number"],
                    "description": "Length in target_unit"
                }
            }
        }

