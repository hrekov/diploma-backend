from dataclasses import dataclass


@dataclass
class VehicleModel:
    year: int
    name: str


def recognize_vehicle_model(image_path: str) -> tuple[str, int] | None:
    # TODO: Stub implementation, use trained model here
    return VehicleModel(name='Jeep Wrangler', year=2020)
