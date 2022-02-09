from typing import Tuple
from urllib import parse
from requests import get

from core.constants import SCHEDULES_PAGE_URL


def schedule_doc_data() -> Tuple[str, str]:
    # study_form = "Бакалавриат"
    # major = "Туризм"
    link = r"http://www.imomi.unn.ru/images/docs/raspisanie/2021_2022_2/%D0%A2%D1%83%D1%80%D0%B8%D0%B7%D0%BC.docx"
    name = str(parse.unquote(link)).split("/")[-1]
    return name, link


def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)
