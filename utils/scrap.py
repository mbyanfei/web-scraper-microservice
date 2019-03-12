from bs4 import BeautifulSoup
from requests import get


def get_page_content(url: str) -> bytes:
    """
    Get content from page.

    :param url: page url
    :return: page content in bytes
    """

    # fix given url to use HTTP requests
    if not url.startswith('http'):
        url = 'http://' + url

    return get(url).content


def get_text_from_page(page_content: bytes) -> str:
    """
    Get clean text (without styles, tags or javascript) from page.

    :param page_content: page content
    :return: clean page text
    """

    soup = BeautifulSoup(page_content, 'lxml')

    for tag in soup.findAll(["script", "style"]):
        tag.extract()

    lines = (line.strip() for line in soup.get_text().splitlines())

    return '\n'.join(line for line in lines if line)  # remove empty lines


def get_images_relative_urls_from_page(page_content: bytes) -> list:
    """
    Get relative urls to all images from page.

    :param page_content: page content
    :return: list of relative urls
    """

    soup = BeautifulSoup(page_content, 'lxml')

    return [img_tag.get('src') for img_tag in soup.findAll('img')]


def get_absolute_urls(base_url: str, relative_urls: list) -> list:
    """
    Get absolute urls for relative_urls list with given base_url.

    :param base_url: base page url
    :param relative_urls: list of relative urls
    :return: list of absolute urls
    """

    return [get_absolute_url(base_url, relative_url) for relative_url in relative_urls]


def get_absolute_url(base_url: str, relative_url: str) -> str:
    """
    Get absolute url for relative_url with given base_url.

    :param base_url: base page url
    :param relative_url: list of relative urls
    :return: absolute url
    """

    absolute_url = relative_url

    if absolute_url.startswith('//'):
        absolute_url = absolute_url[2:]

    if absolute_url.startswith('/'):
        if base_url.endswith('/'):
            base_url = base_url[:-1]

        absolute_url = base_url + absolute_url

    return absolute_url
