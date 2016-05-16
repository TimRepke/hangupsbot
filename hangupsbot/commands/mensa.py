import asyncio, requests, datetime
from bs4 import BeautifulSoup

from hangups import hangouts_pb2

from hangupsbot.utils import strip_quotes, text_to_segments
from hangupsbot.commands import command


# helpful links:
#   string formatting: https://github.com/tdryer/hangups/blob/master/hangups/message_parser.py#L69
#   command examples: https://github.com/xmikos/hangupsbot/tree/master/hangupsbot/commands

def get_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser') 

def get_foods(soup, selector):
    food = [''.join(f.find_all(text=True, recursive=False)).strip() for f in soup.select(selector + ' td.mensa_day_speise_name')]
    price = [''.join(f.find_all(text=True, recursive=False)).strip() for f in soup.select(selector + ' td.mensa_day_speise_preis')]

    return ''.join(['{} _({} €)_\n'.format(food, price[i][4:8]) for i, food in enumerate(food)])


def get_date(soup):
    return soup.select('div.full_page p b')[0].get_text()

def get_url(args):
    baseurl = 'http://www.studentenwerk-berlin.de/mensen/speiseplan/hu_adlershof/'
    dow = datetime.datetime.today().weekday()
    lc_args = [a.lower() for a in args]

    if 'morgen' in lc_args: 
        if datetime.datetime.now().hour <= 15:
            return baseurl + '01.html'
        else:
            return baseurl + '00.html'
    
    days = ['montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag']
    inter = list(set(days).intersection(lc_args))
    if len(inter)>0 and days.index(inter[0]) > dow:
        fixer = 0 if datetime.datetime.now().hour <= 15 else 1
        return baseurl + '0' + str(days.index(inter[0]) - dow - fixer) + '.html'
    
    return baseurl + 'index.html' 


@command.register
def dessert(bot, event, *args):
    """Desserts in der Mensa
       Usage: /mensa dessert [tag]
         tag: morgen oder wochentag (Montag, Mittwoch,...)"""
    url = get_url(args)
    soup = get_soup(url)
    
    text = _(
       '**{}**\n\n'
       '**Desserts**\n'
       '{}'
    ).format(get_date(soup), get_foods(soup,'.desserts'))

    yield from event.conv.send_message(text_to_segments(text))


@command.register
def aktion(bot, event, *args):
    """Aktionsstand in der Mensa
       Usage: /mensa aktion [tag]
         tag: morgen oder wochentag (Montag, Mittwoch,...)"""
    url = get_url(args)
    soup = get_soup(url)

    text = _(
       '**{}**\n\n'
       '**Aktionsstand**\n'
       '{}'
    ).format(get_date(soup), get_foods(soup,'.special'))

    yield from event.conv.send_message(text_to_segments(text))


@command.register
def suppe(bot, event, *args):
    """Suppen in der Mensa
       Usage: /mensa suppe [tag]
         tag: morgen oder wochentag (Montag, Mittwoch,...)"""
    url = get_url(args)
    soup = get_soup(url)

    text = _(
       '**{}**\n\n'
       '**Suppen**\n'
       '{}'
    ).format(get_date(soup), get_foods(soup,'.soups'))
    
    yield from event.conv.send_message(text_to_segments(text))


@command.register
def essen(bot, event, *args):
    """Essen in der Mensa zu Studentenpreisen
       Usage: /mensa essen [tag]
         tag: morgen oder wochentag (Montag, Mittwoch,...)"""
    url = get_url(args)
    soup = get_soup(url)

    text = _(
       '**{}**\n\n'
       '**Essen**\n'
       '{}\n'
       '**Beilagen**\n'
       '{}'
    ).format(get_date(soup), get_foods(soup, '.food'), get_foods(soup, '.side_dishes'))
 
    yield from event.conv.send_message(text_to_segments(text))


# some aliases
@command.register
def nachtisch(bot, event, *args):
    dessert(bot, event, args)
