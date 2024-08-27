import json

import requests
from bs4 import BeautifulSoup
from io import BytesIO
import pytesseract
from PIL import Image
import numpy as np
import cv2


class USTCPassportLogin(object):
    def __init__(self):
        self.passport = "https://passport.ustc.edu.cn/login"
        self.cas_url = 'https://passport.ustc.edu.cn/login?service=https%3A%2F%2Frecapi.ustc.edu.cn%2Fapi%2Fv2%2Fustc_login%3Fclient_id%3Df10f162e-3945-4183-b2b9-f7afe472615f%26key%3Dhttps%253A%252F%252Frec.ustc.edu.cn%252Flogin_terminal'
        self.validate_url = "https://passport.ustc.edu.cn/validatecode.jsp?type=login"
        self.getTokenURL = "https://recapi.ustc.edu.cn/api/v2/check/temp/token/"
        self.sess = requests.session()
        self.token = ''
        self.sess.headers = {
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
        }

    def get_LT(self):
        """
        验证码
        """
        # pytesseract.pytesseract.tesseract_cmd = r'D:\OCR\tesseract.exe'
        text = self.sess.get(self.validate_url, stream=True).content
        image = Image.open(BytesIO(text))
        image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        kernel = np.ones((3, 3), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.erode(image, kernel, iterations=1)
        return pytesseract.image_to_string(Image.fromarray(image))[:4]

    def _get_cas_lt(self):
        """
        获取登录时需要提供的验证字段
        """
        response = self.sess.get(self.passport)

        # 使用BeautifulSoup解析响应的HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 从<script>标签中提取JavaScript代码

        # 查找所有的script标签
        scripts = soup.find_all('script')

        # 获取最后一个script标签的内容
        script_text = scripts[-1].string

        start_index = script_text.find('$("#CAS_LT").val("') + len('$("#CAS_LT").val("')
        end_index = script_text.find('");', start_index)

        # 提取CAS_LT的值
        CAS_LT = script_text[start_index:end_index]

        return CAS_LT

    def login(self, username, password, resultInput):
        """
        登录,需要提供用户名、密码
        """
        self.sess.cookies.clear()
        try:
            CAS_LT = self._get_cas_lt()
            LT = self.get_LT()
            login_data = {
                'username': username,
                'password': password,
                'warn': '',
                'CAS_LT': CAS_LT,
                'showCode': '1',
                'button': '',
                'model': 'uplogin.jsp',
                'service': '',
                'LT': LT,
                'resultInput': resultInput
            }
            # 登录Center
            self.sess.post(self.passport, login_data)
            # 登录rec重定向
            responce2 = self.sess.get(self.cas_url, allow_redirects= False)

            redirectURLWithST = responce2.headers.get("location")
            # 获得ST
            responce3 = self.sess.get(redirectURLWithST, allow_redirects=False)
            # 'https://recapi.ustc.edu.cn/api/v2/ustc_login?client_id='
            redirectURL = responce3.headers.get("location")
            # 客户端ID 后续备用
            clientID = redirectURL.split("=")[1].split("&")[0]
            # 获得Token
            responce4 = self.sess.get(redirectURL, allow_redirects=False)
            # 'https://rec.ustc.edu.cn/login_terminal?token='
            redirectURLWithToken = responce4.headers.get("location")
            Token = redirectURLWithToken.split("=")[1]
            # https://recapi.ustc.edu.cn/api/v2/check/temp/token/?clientid=
            self.getTokenURL = self.getTokenURL + Token + "?clientid=" + clientID
            # 拿到x_auth_token
            responce5 = self.sess.get(self.getTokenURL)
            # 'x-auth-token'
            decoded_content = responce5.content.decode('utf-8-sig')
            json_data = json.loads(decoded_content)
            x_auth_token = json_data['entity']['x_auth_token']
            self.token = x_auth_token
            return x_auth_token is not None
        except Exception as e:
            print(e)
            return False
