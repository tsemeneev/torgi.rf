import json
import requests
from pprint import pprint

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    # 'Cookie': '_ym_uid=1722849986863425768; _ym_d=1722849986; _ym_isad=1; SESSION=ZGMzN2Q4MDktMDFiYi00N2I3LTg0NzctMmZhNmY3OGZjNjMx; _ym_visorc=w',
    'Referer': 'https://torgi.gov.ru/new/public/lots/reg',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'branchId': 'null',
    'organizationId': 'null',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'traceparent': '00-132d6ca35bbc7f7c99fa2f5fb7e358e7-157d4c6891b69915-01',
}

response = requests.get(
    'https://torgi.gov.ru/new/api/public/lotcards/search?lotStatus=PUBLISHED,APPLICATIONS_SUBMISSION,DETERMINING_WINNER&matchPhrase=false&byFirstVersion=true&withFacets=true&size=10&sort=firstVersionPublicationDate,desc',
    headers=headers,
)

ids = [x['id'] for x in response.json()['content']]
for id in ids:
    response = requests.get(f'https://torgi.gov.ru/new/api/public/lotcards/{id}', headers=headers)
    pprint(response.json()['lotName'])

# with open('req.json', 'w', encoding='utf-8') as file:
#     json.dump(response.json(), file, ensure_ascii=False, indent=4)