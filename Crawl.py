import requests
from bs4 import BeautifulSoup

GET_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Host": "m.dcinside.com",
    "Connection": "keep-alive",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}

POST_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "m.dcinside.com",
    "Origin": "http://m.dcinside.com",
    "Referer": "http://m.dcinside.com/write.php?id=alphago&mode=write",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

GALLARY_CODE = {'football_new5': '해외축구', 'comic_new1': '만화'}

SET_WORD = ''

TITLE_LIST = []

mod = 0


class WebCrawler:
    def __init__(self, basic_url):
        self.text = ''
        self.url = basic_url
        self.get_params = {}

    def GetText(self, **kwargs):
        with requests.Session() as s:
            requesting = s.get(self.url, **kwargs)
            if requesting.status_code == 200:
                self.text = requesting.text
            else:
                print(">> Internet access failed.")
                print(">> Error Code", requesting.status_code)


def GetPage(num):
    # GET & parse data===================
    req.get_params.update({'page': num})
    req.GetText(headers=set_header, params=req.get_params, timeout=3)

    soup = BeautifulSoup(req.text, 'html.parser')
    parsed_data = soup.find_all("span", "title", "txt")

    return parsed_data


def GallaryName():
    print('갤러리 ID 목록:', GALLARY_CODE)
    code = input(">> Insert gallery's id : ")

    if code in GALLARY_CODE:
        print('\n{} 갤러리를 검색합니다.\n'.format(GALLARY_CODE[code]))
        req.get_params['id'] = code
    else:
        print('코드를 찾을 수 없습니다.\n')
        GallaryName()


def TitleSearching(title):
    if len(title) > 0:
        for i in range(len(title)):
            TITLE_LIST.append(SplitText(str(title[i]), 'txt">', '<'))
    else:
        print('>> data is empty')


def TitlePrint(text):
    TitleSearching(text)
    for i in range(len(TITLE_LIST)):
        print('>> no.{}:'.format(i + 1), TITLE_LIST[i], '\n')

    print('>> page {} is ended'.format(req.get_params['page']))
    print('\n============================================\n')
    TITLE_LIST.clear()


def SplitText(title, start='', end=''):
    s = title.find(start, 0)
    s += len(start)

    e = title.find(end, s)

    except_word = []

    if len(except_word) != 0:
        for j in range(len(except_word)):
            if except_word[j] in title[s:e]:
                return 'excepted'

    return title[s:e]


def CountWord():
    s = 0
    for i in range(len(TITLE_LIST)):
        if SET_WORD in TITLE_LIST[i]:
            print('searched :', TITLE_LIST[i])
            s += 1
    TITLE_LIST.clear()

    return s


if __name__ == '__main__':
    req = WebCrawler('http://m.dcinside.com/list.php')
    page_text = ''

    set_header = GET_HEADERS.copy()
    set_header['Referer'] = req.url

    print('=================================\n'
          '==== [DC-INSIDE 게시물 검색기] =====\n'
          '=================================\n')

    GallaryName()
    print('=================================================\n')

    while 1:
        print('====================== mod ========================================\n'
              '= 1. 글 제목 리스트  |   2. 단어 수 검색  |   3. 갤러리 변경 |   4. 종료  =\n'
              '===================================================================\n')
        mod = int(input('>> Select mod : '))

        if mod == 1:
            page_loop = int(input('>> Page Limit : '))
            for i in range(1, page_loop + 1):
                page_text = GetPage(i)
                TitlePrint(page_text)

        elif mod == 2:
            SET_WORD = input('>> 대상 단어 : ')
            page_loop = int(input('>> Page Limit : '))

            word_num = 0
            for i in range(1, page_loop + 1):
                page_text = GetPage(i)
                TitleSearching(page_text)

                word_num += CountWord()

            print('\n[{}]가'.format(SET_WORD), word_num,
                  '개만큼 검색되었습니다.[{} / {}]\n'.format(word_num, page_loop * 25))
            SET_WORD = ''

        elif mod == 3:
            print('검색할 갤러리를 변경합니다.\n'
                  '==========================================')
            GallaryName()

        elif mod == 4:
            print('수고링~')
            exit()

        else:
            print('모드 상태가?')
