import csv, re, random, requests

from bs4 import BeautifulSoup
from celery import shared_task
from django.db.utils import DataError, IntegrityError
from .models import Website, WebsiteCategory, WebsitePage

pattern = re.compile(r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.'
                         r'[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')

@shared_task
def upload_from_csv():
    with open('/home/iwan96/Pulpit/aplikacja_rekrutacyjna/top-1m.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if int(line[0]) < 8:
                alexa_rank = line[0]
                url = line[1]
                if WebsiteCategory.objects.all().count() > 0:
                    random_idx = random.randint(0, WebsiteCategory.objects.count() - 1)
                    random_obj = WebsiteCategory.objects.all()[random_idx]
                    Website.objects.update_or_create(url="https://" + url, alexa_rank=alexa_rank, category=random_obj)
                else:
                    Website.objects.update_or_create(url="https://" + url, alexa_rank=alexa_rank)

    return "Website List from top-1m.csv file uploaded"



@shared_task
def website_detail(id):
    website = Website.objects.get(id=id)
    r = requests.get(website.url)
    soup = BeautifulSoup(r.text, 'html.parser')
    website.title = soup.title.string
    website.save()

    website_pages = []

    for link in soup.find_all('a', href=pattern):
        website_pages.append(link.get('href'))

    for page in website_pages:
        try:
            r2 = requests.get(page)
            soup2 = BeautifulSoup(r2.text, 'html.parser')
            WebsitePage.objects.update_or_create(website=website, url=page, title=soup2.title.string)

        except AttributeError:
            continue
        except DataError:
            continue
        except IntegrityError:
            continue

    website_page_detail.delay(id)
    return "Website details updated"

#not used in project. This task is for updating each Websites details.
@shared_task
def each_website_detail():
    website_list = Website.objects.all()
    for website in website_list:
        r = requests.get(website.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        website.title = soup.title.string
        website.save()

    return "Each Website details updated"

@shared_task
def website_page_detail(id):
    website = Website.objects.get(id=id)
    website_page_list = WebsitePage.objects.filter(website=website)
    for page in website_page_list:
        r = requests.get(page.url)
        soup = BeautifulSoup(r.text, 'html.parser')

        for link in soup.find_all('a', href=pattern):
            print(link.get('href'))

    return "Website's pages have been scanned !"

@shared_task
def category_count():
    category_list = WebsiteCategory.objects.all()
    for category in category_list:
        count = Website.objects.filter(category=category).count()
        category.count = count
        category.save()

    return "Category's count updated !"

