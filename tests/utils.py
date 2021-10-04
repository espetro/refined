import os
from typing import List


def get_message_lines(message: str) -> List[str]:
    return [_.strip() for _ in str(message).split(os.linesep) if _]
