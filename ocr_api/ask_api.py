import asyncio
import aiohttp
import random
from hashlib import md5

class AskForAPI:
    def __init__(self):
        self.appid = ''
        self.appkey = ''
        self.from_lang = 'jp'
        self.to_lang = 'zh'
        self.endpoint = 'http://api.fanyi.baidu.com'
        self.path = '/api/trans/vip/translate'
        self.url = self.endpoint + self.path
        self.query = '私はあなたが好きで、私はとてもあなたが好きで、私はあなたのボーイフレンドになりたいです'
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.payload = {}
        self.ans = ""

    #更改翻译词汇
    def change_word(self, word):
        self.query = word

    def make_md5(self, s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    async def getready(self):
        salt = random.randint(32768, 65536)
        sign = self.make_md5(self.appid + self.query + str(salt) + self.appkey)
        self.payload = {
            'appid': self.appid,
            'q': self.query,
            'from': self.from_lang,
            'to': self.to_lang,
            'salt': salt,
            'sign': sign
        }

    async def send_request(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, data=self.payload, headers=self.headers) as r:
                result = await r.json()
                if "trans_result" in result and len(result["trans_result"]) > 0:
                    self.ans = result["trans_result"][0]["dst"]
                else:
                    print("No translation result found.")

    async def main(self):
        await self.getready()
        await self.send_request()
        print(self.ans)

if __name__ == '__main__':
    ask_api = AskForAPI()
    asyncio.run(ask_api.main())
