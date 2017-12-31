import py2neo
from py2neo import Graph
from database.model.Model import Site
from database.model.Model import News
from database.model.Model import Tipo

class DataBase:

    def __init__(self):
        py2neo.authenticate("localhost:7474", "neo4j", "st1215")
        self.graph = Graph("http://localhost:7474/db/data/")


    # def get_queue(self, site_url):
    #     queue=set()
    #     for s in SiteQueue.select(self.graph).where(site=site_url):
    #         queue.add(s.page)
    #     return queue
    #
    # def save_queue(self, site, page):
    #     queue=SiteQueue()
    #     queue.site=site
    #     queue.page=page
    #     self.graph.push(queue)

    def get_site(self, name):
        sites = Site.select(self.graph).where(name=name)
        for site in sites:
            return site

    def get_clazz(self, name):
        tipos = Tipo.select(self.graph).where(description=name)
        for tipo in tipos:
            return tipo

    def save_site(self, site_name, url):
        site=Site()
        site.name=site_name
        site.url=url
        self.graph.push(site)

    def save_news(self, site, url, title, content, tipo):
        s=self.get_site(site)
        # t = self.get_clazz(tipo)
        news =News()
        news.site.add(s)
        # news.tipo.add(t)
        news.title=title
        news.content=content
        news.url=url
        self.graph.merge(news)




    def create_rel(self, node1, node2):
        self.graph.create("(s:Site)-[:PUBLICOU]->(n:News)")

    def install(self):
        self.graph.run("MATCH (n) DETACH DELETE n")
        self.graph.run("MATCH (n) DETACH DELETE n")

    def delete(self):
        self.graph.delete_all();
        tipo = Tipo()
        tipo.description='False'
        self.graph.merge(tipo)
        tipo = Tipo()
        tipo.description = 'True'
        self.graph.merge(tipo)

# #
# db = DataBase()
# db.delete()