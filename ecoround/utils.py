import os
from typing import List


def get_files_by_uid(uid: str) -> List[str]:
    path = os.path.dirname(os.path.abspath(__file__))

    return [
        os.path.join(f"{path}/../data/{uid}", file)
        for file in os.listdir(f"{path}/../data/{uid}")
    ]
