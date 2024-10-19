import asyncio

from cv2.typing import map_int_and_double

from ocr_api.ask_api import AskForAPI
from ocr_api.ocr import OCR

#调用ocr和api，将翻译存入self.txt
class GET_TRAN:
    def __init__(self):
        self.api = AskForAPI()
        self.ocr = OCR()
        self.ori_txt = ""
        self.txt = ""

    async def ocr_api(self):
        await self.ocr.pd_ocr()
        self.ori_txt = self.ocr.ocr_text
        self.api.change_word(self.ori_txt)
        await self.api.main()
        self.txt = self.api.ans
        return self.txt

if __name__ == '__main__':
    get_tran = GET_TRAN()
    asyncio.run(get_tran.ocr_api())
    print(get_tran.txt)