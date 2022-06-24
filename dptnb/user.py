from nameko.rpc import rpc

import dependencies

class UserService:

    name = 'user_service'

    database = dependencies.Database()

    @rpc
    def regis(self, a, b):
        user = self.database.regis(a, b)
        return user
    
    @rpc
    def getu(self):
        user = self.database.getu()
        return user
    
    @rpc
    def login(self, a, b):
        user = self.database.login(a, b)
        return user

    @rpc
    def get_news(self):
        news = self.database.get_news()
        return news

    @rpc
    def get_news_by_id(self, id):
        news = self.database.get_news_by_id(id)
        return news

    @rpc
    def insert_news(self, category, date):
        news = self.database.insert_news(category, date)
        return news

    @rpc
    def edit_news(self, id, category, date):
        news = self.database.edit_news(id, category, date)
        return news

    @rpc
    def delete_news(self, id):
        news = self.database.delete_news(id)
        return news
    