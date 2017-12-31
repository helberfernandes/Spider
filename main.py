import threading
from queue import Queue
from spider import Spider
from domain import *
from General import *

PROJECT_NAME = 'semprequestione'
HOMEPAGE = 'http://www.semprequestione.com/search/label/Papa'
# PROJECT_NAME = 'acidigital'
# HOMEPAGE = 'http://www.acidigital.com/'
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

general = General()

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in general.file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = general.file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()
