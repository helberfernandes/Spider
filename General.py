import os
from domain import get_domain_name
from database.DataBase import DataBase
from scrapy.ScrapySempreQuestione import ScrapySempreQuestione


class General:

    def __init__(self):
        self.db = DataBase()

    # Each website is a separate project (folder)
    def save_site(self, site_name, url):
        self.db.save_site(site_name, url)

    # Create queue and crawled files (if not created)
    # def create_data_files(self, project_name, base_url):
    #     if not os.path.isfile(queue):
    #         write_file(queue, base_url)
    #     if not os.path.isfile(crawled):
    #         write_file(crawled, '')

    # # Create a new file
    # def write_file(self, path, data):
    #     with open(path, 'w') as f:
    #         f.write(data)

    # Add data onto an existing file
    def append_to_file(self, path, data):
        with open(path, 'a') as file:
            file.write(data + '\n')

    # Delete the contents of a file
    def delete_file_contents(self, path):
        open(path, 'w').close()

    # Read a file and convert each line to set items
    def get_queue(self, file_name):
        return set(self.db.get_queue(file_name))

    # Iterate through a set, each item will be a line in a file
    def save_queue(self, site, links):
        for link in sorted(links):
            self.db.save_queue(site, link)

    def save_news(self, site, links):
        """
        Save all news crawled
        :param site:  site what published a news
        :param links: All pages crawled
        :return:
        """
        for link in sorted(links):
           sc= ScrapySempreQuestione(site, link)
           sc.process()
            # self.db.save_news(site, link, link)



    # Each website is a separate project (folder)
    def create_project_dir(self, directory):
        if not os.path.exists(directory):
            print('Creating directory ' + directory)
            os.makedirs(directory)

    # Create queue and crawled files (if not created)
    def create_data_files(self, project_name, base_url):
        queue = os.path.join(project_name, 'queue.txt')
        if not os.path.isfile(queue):
            self.write_file(queue, base_url)

    # Create a new file
    def write_file(self, path, data):
        with open(path, 'w') as f:
            f.write(data)

    # Add data onto an existing file
    def append_to_file(self, path, data):
        with open(path, 'a') as file:
            file.write(data + '\n')

    # Delete the contents of a file
    def delete_file_contents(self, path):
        open(path, 'w').close()

    # Read a file and convert each line to set items
    def file_to_set(self, file_name):
        results = set()
        with open(file_name, 'rt') as f:
            for line in f:
                results.add(line.replace('\n', ''))
        return results

    # Iterate through a set, each item will be a line in a file
    def set_to_file(self, links, file_name):
        with open(file_name, "w") as f:
            for l in sorted(links):
                f.write(l + "\n")

