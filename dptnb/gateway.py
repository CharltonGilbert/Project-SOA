from datetime import date
import json
import string
from unicodedata import category
import requests as req
from unittest import result
from xml.etree.ElementTree import tostring

from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from session import SessionProvider

class GatewayService:
    name = 'gateway'

    newsrpc = RpcProxy('user_service')
    session_provider = SessionProvider()
    
    @http('POST', '/regis')
    def regis(self, request):
        data = format(request.get_data(as_text=True))
        arr  =  data.split("&")

        username = "" 
        password = "" 
        for el in arr:
            node     = el.split("=")
            if node[0] == "username":
                username = node[1]
            if node[0] == "password":
                password = node[1]
        rooms = self.newsrpc.regis(username, password)
        return json.dumps(rooms)
    
    @http('GET', '/login')
    def login(self, request):
        data = format(request.get_data(as_text=True))
        arr  =  data.split("&")

        username = "" 
        password = "" 
        for el in arr:
            node     = el.split("=")
            if node[0] == "username":
                username = node[1]
            if node[0] == "password":
                password = node[1]
        flags = self.newsrpc.login(username, password)
        
        if(flags == 1):
            user_data = {
                'username': username,
                'password': password
            }
            session_id = self.session_provider.set_session(user_data)
            response = Response(str(user_data))
            response.set_cookie('SESSID', session_id)
            return response
        else:
            result = []
            result.append("Username/password incorrect")
            return json.dumps(result)
    
    @http('GET', '/check')
    def check(self, request):
        cookies = request.cookies
        return Response(cookies['SESSID'])
    
    @http('POST', '/logout')
    def logout(self, request):
        cookies = request.cookies
        if cookies:
            confirm = self.session_provider.delete_session(cookies['SESSID'])
            if (confirm):
                response = Response('Logout Successful')
                response.delete_cookie('SESSID')
            else:
                response = Response("Logout Failed")
            return response
        else:
            response = Response('Login Required')
            return response

    @http('GET', '/news')
    def get_news(self, request):
        news = self.newsrpc.get_news()
        return json.dumps(news)

    @http('GET', '/news/<int:id>')
    def get_news_by_id(self, request, id):
        news = self.newsrpc.get_news_by_id(id)
        return json.dumps(news)

    @http('POST', '/news')
    def insert_news(self, request):
        cookies = request.cookies

        if cookies:
            data = format(request.get_data(as_text=True))
            arr  =  data.split("&")

            category = "" 
            date = "" 
            for el in arr:
                node     = el.split("=")
                if node[0] == "category":
                    category = node[1]
                if node[0] == "date":
                    date = node[1]
            rooms = self.newsrpc.insert_news(category, date)
            return json.dumps(rooms)
        else:
            response = Response('You need to Login First')
            return response

    @http('PUT', '/news/<int:id>')
    def update_news(self, request, id):
        cookies = request.cookies

        if cookies:
            data = format(request.get_data(as_text=True))
            arr  =  data.split("&")

            category = "" 
            date = "" 
            for el in arr:
                node     = el.split("=")
                if node[0] == "category":
                    category = node[1]
                if node[0] == "date":
                    date = node[1]
            rooms = self.newsrpc.edit_news(id, category, date)
            return json.dumps(rooms)
        
        else:
            response = Response('You need to Login First')
            return response

    @http('DELETE', '/news/<int:id>')
    def delete_news(self, request, id):
        cookies = request.cookies

        if cookies:
            news = self.newsrpc.delete_news(id)
            return json.dumps(news)
        else:
            response = Response('You need to Login First')
            return response