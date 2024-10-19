程序基于paddle_ocr（cpu）和百度翻译实现
```python
#主要环境
      pytonh = 3.9
      paddle_ocr(cpu版本)请在官网根据电脑配置选择好环境
```

如想使用，需在百度翻译开放平台：https://api.fanyi.baidu.com/ 注册账号
注册后将appid与密钥分别填入ocr_api文件下ask_api.py中的self.appid和self.appkey中
```python
        self.appid = ''
        self.appkey = ''
```
程序不止限于翻译日文，若想翻译其他语言，可以在查找百度翻译的文档与paddleocr文档后将ask_api.py中“self.from_lang”和ocr.py中“self.ocr = PaddleOCR(use_angle_cls=True, lang="japan")”参数更改为相应语言
```python
# /ocr_api/ask_api.py
        self.from_lang = 'jp'
# /ocr_api/ocr.py
        self.ocr = PaddleOCR(use_angle_cls=True, lang="japan")#更改lang=''中即可
```

温馨提示：  
本程序仅是作者使用软件时对ocr的好奇心驱使下借鉴团子翻译器写的，非常敷衍，如果想有良好的翻译体验，作者推荐在完成百度翻译注册后使用团子翻译器  
恳请兄弟们给我点颗星，虽然写的很敷衍。但也是我学习以来第一个做出来的东西，给我点激励。  
跪谢！！！！！！
