import aiohttp_jinja2
from aiohttp import web
from app.utils import parseInt
from app import client, results_per_page
from app.telegram import get_chat_messages


@aiohttp_jinja2.template("index.html")
async def index_chat(req):
    chat_id = parseInt(req.match_info["chat"])
    
    try:
        offset = int(req.query.get('page', '1'))
    except:
        offset = 1
    try:
        search_query = req.query.get('search', '')
    except:
        search_query = ''
    offset_val = 0 if offset <=1 else offset-1
    
    try:
        results, chat = await get_chat_messages(chat_id, offset_val, search_query)
    except Exception as err:
        print(f"Chat {chat_id} not found")
        return web.HTTPFound("/")
    
    prev_page = False
    next_page = False
    if offset_val:
        query = {'page':offset_val}
        if search_query:
            query.update({'search':search_query})
        prev_page =  {
            'url': str(req.rel_url.with_query(query)),
            'no': offset_val
        }

    if len(results) == results_per_page:
        query = {'page':offset_val+2}
        if search_query:
            query.update({'search':search_query})
        next_page =  {
            'url': str(req.rel_url.with_query(query)),
            'no': offset_val+2
        }
    
    return {
        'chat_title': chat,
        'items':results,
        'prev_page': prev_page,
        'next_page': next_page,
        'cur_page' : offset,
        'search': search_query
    }