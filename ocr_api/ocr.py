import asyncio

from paddle.base.libpaddle.eager.ops.legacy import lod_reset_
from paddleocr import PaddleOCR

class OCR:
    def __init__(self):
        self.loading_ocr()
        self.ocr_text = ""

    def loading_ocr(self):
        # 初始化 OCR，指定语言为日文
        self.ocr = PaddleOCR(use_angle_cls=True, lang="japan")
        print("loading_complite")

    async def pd_ocr(self):
        # 初始化 OCR，指定语言为日文
        #ocr = PaddleOCR(use_angle_cls=True, lang="japan")

        # 识别图片中的文字，图片路径为 './picture/pict.jpg'
        image_path = './picture/pict.jpg'
        result = self.ocr.ocr(image_path, det=True, rec=True)

        # 提取识别到的文字
        recognized_texts = []
        for line in result:
            for box, (text, score) in line:
                recognized_texts.append(text)

        # 将识别的文字存入变量 ori
        ori = "".join(recognized_texts)
        self.ocr_text = ori
        # 输出变量 ori 的内容
        print(ori)

if __name__ == '__main__':
    oc = OCR()
    asyncio.run(oc.pd_ocr())