from bs4 import BeautifulSoup
import re
from typing import TypedDict


class ParseResult(TypedDict):
    method: str | None
    path: str | None
    headers: dict[str, str] | None
    params: dict[str, str] | None
    cookies: dict[str, str] | None
    forms: dict[str, str] | None
    files: dict[str, str] | None


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')

    result: ParseResult = {
        'method': get_method(soup),
        'path': get_path(soup),
        'headers': get_headers(soup),
        'params': get_params(soup),
        'cookies': get_cookies(soup),
        'forms': get_forms(soup),
        'files': get_files(soup)
    }

    return result


def table_to_dict(table):
    result = {}

    for row in table.find_all('tr'):
        cells = row.find_all('td')

        if len(cells) != 2:
            continue

        key = cells[0].get_text(strip=True)
        value = cells[1].get_text(strip=True)

        result[key] = value

    return result


def get_method(soup):
    text = soup.get_text()

    if 'POST-запрос' in text:
        return 'POST'

    if 'Перейдите' in text:
        return 'GET'

    return None


def get_path(soup):
    link = soup.find('a')

    if link is not None:
        return link.get('href')

    text = soup.find(string=re.compile('по адресу'))

    if text is not None:
        code = text.find_next('code')

        if code is not None:
            return code.get_text(strip=True)

    return None


def get_cookies(soup):
    for table in soup.find_all('table'):
        description = table.find_previous(
            string=lambda s: s and s.strip()
        )

        if description and 'cookie' in description.lower():
            return table_to_dict(table)

    return None


def get_files(soup):
    files = {}

    for table in soup.find_all('table'):
        rows = table.find_all('tr')

        if not rows:
            continue

        headers = [th.get_text(strip=True) for th in rows[0].find_all('th')]

        if headers != ['Имя файла', 'Содержимое']:
            continue

        for row in rows[1:]:
            cells = row.find_all('td')

            if len(cells) != 2:
                continue

            filename = cells[0].get_text(strip=True)
            content = cells[1].get_text(strip=True)

            files[filename] = content

    return files if len(files) > 0 else None


def get_headers(soup):
    for table in soup.find_all('table'):
        description = table.find_previous(
            string=lambda s: s and s.strip()
        )

        if description and 'заголовки' in description.lower():
            return table_to_dict(table)

    return None


def get_params(soup):
    for table in soup.find_all('table'):
        description = table.find_previous(
            string=lambda s: s and s.strip()
        )

        if description and 'параметры запроса' in description.lower():
            return table_to_dict(table)

    return None


def get_forms(soup):
    for table in soup.find_all('table'):
        description = table.find_previous(
            string=lambda s: s and s.strip()
        )

        if description and 'данные формы' in description.lower():
            return table_to_dict(table)

    return None