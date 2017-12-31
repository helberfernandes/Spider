from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from General import General


class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    general = General()
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        Spider.general.create_project_dir(Spider.project_name)
        Spider.general.create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = Spider.general.file_to_set(Spider.queue_file)
        Spider.general.save_site(Spider.project_name,Spider.base_url)
        # create_data_files(Spider.project_name, Spider.base_url)



    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            if page_url in Spider.queue:
                Spider.queue.remove(page_url)
            if page_url.find('papa') != -1 or page_url.find('vaticano') != -1 or page_url.find('bispos') != -1:
                Spider.crawled.add(page_url)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        Spider.general.set_to_file(Spider.queue, Spider.queue_file)
        # Spider.general.save_queue(Spider.project_name, Spider.queue)
        Spider.general.save_news(Spider.project_name, Spider.crawled)
