import aiohttp_jinja2
from aiohttp import web
from app.helper.utils import parseChat
from app import client, results_per_page
from app.helper.telegram import get_chat_messages


class IndexChat(web.View):
    async def post(self):
        chat = await parseChat(self.request)
        return web.HTTPFound("/"+chat_id)

    
    @aiohttp_jinja2.template("index.html")
    async def get(self):
        try:
            chat = await parseChat(self.request)
        except:
            return web.HTTPFound("/")
        
        try:
            offset = int(self.request.query.get('page', '1'))
        except:
            offset = 1
        try:
            search_query = self.request.query.get('search', '')
        except:
            search_query = ''
        offset_val = 0 if offset <=1 else offset-1
    
        try:
            results = await get_chat_messages(chat, offset_val, search_query)
        except Exception as err:
            print(f"Chat {chat['chat_id']} not found")
            return web.HTTPFound("/")
    
        prev_page = False
        next_page = False
        if offset_val:
            query = {'page':offset_val}
            if search_query:
                query.update({'search':search_query})
            prev_page =  {
                'url': str(self.request.rel_url.with_query(query)),
                'no': offset_val
            }

        if len(results) == results_per_page:
            query = {'page':offset_val+2}
            if search_query:
                query.update({'search':search_query})
            next_page =  {
                'url': str(self.request.rel_url.with_query(query)),
                'no': offset_val+2
            }
    
        return {
            'chat_title': chat['title'],
            'items': results,
            'prev_page': prev_page,
            'next_page': next_page,
            'cur_page' : offset,
            'search': search_query
        }