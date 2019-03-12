from extensions import db
from helpers import scraping
from models import PageText, PageImage
from worker import celery_app


@celery_app.task(name='collect_text')
def collect_text(url: str):
    page_content = scraping.get_text_content(url)
    text = scraping.get_text_from_page(page_content)

    page_text = PageText(url=url, text=text)
    db.session.merge(page_text)
    db.session.commit()


@celery_app.task(name='collect_images')
def collect_images(url: str):
    page_content = scraping.get_text_content(url)
    images_relative_urls = scraping.get_images_relative_urls_from_page(page_content)
    images_urls = scraping.get_absolute_urls(url, images_relative_urls)

    for image_url in images_urls:
        image_data = scraping.get_bytes_content(image_url)

        page_image = PageImage(url=image_url, image=image_data, page_url=url)
        db.session.merge(page_image)
        db.session.commit()
