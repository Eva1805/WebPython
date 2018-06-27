from bs4 import BeautifulSoup
from decimal import Decimal

def convert(amount, cur_from, cur_to, date, requests):

    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req=%s' % date)
    soup = BeautifulSoup(response.text, 'html.parser')
    cur_from_soup = soup.find('charcode', text=cur_from)
    # try:
    parent_from = cur_from_soup.find_parent()
    nominal_from = int(parent_from.find('nominal').get_text())
    value_from = Decimal(parent_from.find('value').get_text().replace(',','.'))
    value_from_ru = Decimal(value_from / nominal_from) * amount
    # except:
    #     if cur_from == 'RUR':
    #         nominal_from = 1
    #         value_from =  1
    #         value_from_ru = Decimal(value_from / nominal_from) * amount

    cur_to_soup = soup.find('charcode', text=cur_to)
    parent_to = cur_to_soup.find_parent()
    nominal_to = int(parent_to.find('nominal').get_text())
    value_to = Decimal(parent_to.find('value').get_text().replace(',','.'))
    value_to_one = value_to / nominal_to


    result = Decimal(value_from_ru / value_to_one)
    result = result.quantize(Decimal('1.0000'))
    return result  # не забыть про округление до 4х знаков после запятой
