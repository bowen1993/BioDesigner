import os
import django
import sys
from BeautifulSoup import BeautifulSoup
import urllib2
import traceback
pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import paper

def main():
    paper_list = paper.objects.all()
    for paper_obj in paper_list:
        set_paper_title(paper_obj)

def set_paper_title(paper_obj):
    print paper_obj.paper_id
    if paper_obj.paper_name != None:
        return
    try:
        baseUrl = paper_obj.paper_url
        req = urllib2.Request(baseUrl)
        response = urllib2.urlopen(req)
        resStr = response.read()
        soup = BeautifulSoup(resStr)
        rprt_div = soup.find('div', {"class": "rprt_all"})
        title_tag = rprt_div.find('h1')
        paper_obj.paper_name = title_tag.string
        paper_obj.save()
    except:
        pass


if __name__ == '__main__':
    django.setup()
    main()