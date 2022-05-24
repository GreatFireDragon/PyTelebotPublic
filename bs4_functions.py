import bs4   #beautifulsoup4
from random import randrange
import json
import requests
from datetime import datetime



def get_anekdot():
    array_anedots = []

    req_anek = requests.get('http://anekdotme.ru/random')
    soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
    result_find = soup.select('.anekdot_text')

    for result in result_find:
        array_anedots.append(result.getText().strip())
    return array_anedots[0]



def get_news(message):

    covid = requests.get('https://yandex.ru/')
    soup = bs4.BeautifulSoup(covid.text, "html.parser")
    result_find = soup.select('.news__item-content')

    array = []

    for result in result_find:
        array.append(result.getText().strip())

    try:
        ans = array[randrange(9)]
        return ans
    except IndexError:
       return "ERROR 404 NOT FOUND"



def valute():

    all_content = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    content = all_content['Valute']

    date = all_content["Date"]
    date = date[:10]
    date = datetime.strptime(date, '%Y-%m-%d')
    date = date.strftime("%m/%d/%Y")

    ans = ""
    ans += "Курс на следующую дату: " + date + "\n"
    ans += str(content['EUR']['Name']) + " " + str(content['EUR']['Value']) + " рублей" + "\n"
    ans += str(content['USD']['Name']) + " " + str(content['USD']['Value']) + " рублей"

    return(ans)

def fill_wordle_txt():
    base_url = 'https://www.bestwordlist.com/5letterwordspage'
    n = 0

    file = open('wordle.txt', 'w')

    # for the first page
    req_anek = requests.get('https://www.bestwordlist.com/5letterwords.htm')
    soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
    result_find = soup.select('.mot2')

    # print(result_find)
    import re
    for string in result_find:
        string = str(string)
        ans = re.search(r">.{6}<", string)
        n += 1
        try:
            ans = ans.group()[2:-1]
            file.write(ans + '\n')
        except Exception:
            pass

    for i in range(14):
        url = base_url + str(i + 2) + '.htm'
        print(url)

        req_anek = requests.get(url)
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select('.mot2')

        # print(result_find)
        import re
        for string in result_find:
            string = str(string)
            ans = re.search(r">.{6}<", string)
            n += 1
            try:
                ans = ans.group()[2:-1]
                file.write(ans + '\n')
            except Exception:
                pass

    file.close()

# fill_wordle_txt()