import random
from enum import Enum

from aiobalaboba import balaboba

from core.utils import singleton


class BalabobaStyles(Enum):
    Unstyled = 0
    ConspiracyTheory = 1
    TVReport = 2
    Toast = 3
    BoyQuotes = 4
    AdvSlogans = 5
    Stories = 6
    InstagramSigns = 7
    Wiki = 8
    MovieSynopsis = 9
    Horoscope = 10
    FolkWisdom = 11
    NewEuropeanTheatre = 18


@singleton
class MemeService:
    BALABOBA_INPUT_STRINGS = ["Студенты ИМОМИ", "Студенты ННГУ", "Студенты Туризма"]

    async def get_answer_sign(self):
        input = random.choice(self.BALABOBA_INPUT_STRINGS)
        style = random.choice(list(BalabobaStyles))
        return await balaboba(input, intro=style.value)
