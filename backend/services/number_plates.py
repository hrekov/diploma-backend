from functools import lru_cache

from openalpr import Alpr

from backend.logger import common_logger


@lru_cache
def load_alpr_library() -> Alpr:
    instance = Alpr("us", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")

    # Set the number of results to return (only the most accurate result)
    instance.set_top_n(1)

    return instance


def recognize_number_plate(photo_path: str) -> str | None:
    alpr = load_alpr_library()

    if not alpr.is_loaded():
        common_logger.warning('Failed to load alpr library')
        return None

    results = alpr.recognize_file(photo_path)

    if len(results['results']) > 0:
        return results['results'][0]['plate']
