import os
import cv2
import requests
import numpy as np

from lxml import html


class DownloadResult:
    def __init__(self, e_number, ddlbatch):
        self.e_number = e_number
        self.ddlbatch = ddlbatch
        os.makedirs('./download', exist_ok=True)
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.gturesults.in',
            'priority': 'u=0, i',
            'referer': 'https://www.gturesults.in/Default.aspx',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        }
        self.session = requests.Session()
    
    def get_view_state(self, checkss=None, checkss_1=None):
        # params = {'ext': 'W2024', 'rof': '4121'}
        params = {
            'ext': 'archive',
        }
        
        if checkss:
            data = {
                '__EVENTTARGET': 'ddlsession',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': f'{checkss}',
                '__VIEWSTATEGENERATOR': 'CA0B0334',
                'ddlsession': 'W$2023',
                'ddlbatch': f'{self.ddlbatch}',
                'txtenroll': '',
                'txtSheetNo': '',
                'txtpassword': '',
                'CodeNumberTextBox': '',
            }
            self.print('view_state yes')
            response = self.session.post('https://www.gturesults.in/Default.aspx', headers=self.headers, data=data, params=params)
        else:
            self.print('view_state no')
            # response = self.session.get('https://www.gturesults.in/Default.aspx', params=params, headers=self.headers)
            response = self.session.get('https://www.gturesults.in/Default.aspx', headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            })
        
        con = html.fromstring(response.text)
        view_state = "".join(con.xpath('//input[@id="__VIEWSTATE"]/@value')).strip()
        
        if checkss or checkss_1:
            self.print('view_state 2 done')
            return view_state
        
        self.print('view_state 1 done')
        ss = self.get_view_state(checkss=view_state)
        return ss
    
    def download_captcha(self):
        response = self.session.get('https://www.gturesults.in/Handler.ashx', headers = {
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'i',
            'referer': 'https://www.gturesults.in/Default.aspx',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        })
        # response = self.session.get('https://www.gturesults.in/Handler.ashx', headers={
        #     'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        #     'accept-language': 'en-US,en;q=0.9',
        #     'priority': 'u=1, i',
        #     'referer': 'https://www.gturesults.in/Default.aspx?ext=archive',
        #     'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        #     'sec-ch-ua-mobile': '?0',
        #     'sec-ch-ua-platform': '"Windows"',
        #     'sec-fetch-dest': 'image',
        #     'sec-fetch-mode': 'no-cors',
        #     'sec-fetch-site': 'same-origin',
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        # })
        
        items = {}
        try:
            for i, j in response.cookies._cookies['www.gturesults.in']['/'].items():
                try:
                    items[i] = f'{j.value}'
                except:
                    pass
        except:
            items = {}
        
        return items, response
    
    def get_captcha_text(self, response):
        image = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_GRAYSCALE)
        
        # Define a kernel for dilation: Make changes in the kernel size to get better results
        kernel = np.ones((2, 1), np.uint8)
        dilation2 = cv2.dilate(image, kernel, iterations=1)
        
        _, buffer = cv2.imencode('.png', dilation2)
        image_bytes = buffer.tobytes()
        
        api_url = 'https://api.api-ninjas.com/v1/imagetotext'
        files = {'image': ('dilated_captcha.png', image_bytes, 'image/png')}
        headers = {'X-Api-Key': 'fu/4hdgteLzSiAbRM0QNVA==KFKWp3nh23tT0xXG'}
        
        try:
            r = requests.post(api_url, files=files, headers=headers)
            json_data = r.json()
            text = json_data[0]['text']
        except:
            text = None
        
        return text
    
    def get_text(self, text=None):
        if not text:
            text = open(f'''./download/{self.e_number}.html''', 'r', encoding='utf-8').read()
        
        con = html.fromstring(text)
        try:
            text_demo = " ".join(con.xpath('//span[@id="lblmsg"]//text()')).strip()
        except:
            text_demo = ''
        try:
            text_spi = " ".join(con.xpath('//span[@id="lblSPI"]//text()')).strip()
        except:
            text_spi = ''
        check = True
        if 'Incorrect' in text_demo or 'not available' in text_demo or not text_demo or 'not  available' in text_demo:
            check = False
        return f'{text_demo} || SPI:({text_spi})', check
    
    def print(self, str):
        return
        print(f'{str}')
    
    def main_fun(self):
        self.print('start')
        
        view_state = self.get_view_state(checkss_1=True)
        self.print('view_state done')
        
        co, img_response = self.download_captcha()
        self.print('download_captcha done')
        
        captcha = self.get_captcha_text(img_response)
        self.print(f'captcha done {captcha}')
        
        if not captcha:
            self.print(f'No Captcha, {False}, {self.e_number}, ')
            return 'No Captcha', False, self.e_number
        
        # url = 'https://www.gturesults.in/'
        url = 'https://www.gturesults.in/Default.aspx'
        
        # params = {'ext': 'archive', 'ext': 'W2024', 'rof': '4121'}
        
        # data = {
        #     '__EVENTTARGET': '',
        #     '__EVENTARGUMENT': '',
        #     '__LASTFOCUS': '', # New Params
        #     '__VIEWSTATE': f'{view_state}',
        #     '__VIEWSTATEGENERATOR': 'CA0B0334',
        #     'ddlsession': 'W$2023', # New Params
        #     'ddlbatch': f'{self.ddlbatch}',
        #     'txtenroll': f'{self.e_number}',
        #     'txtSheetNo': '',
        #     'txtpassword': 'M12Soni!@12)', # New Params
        #     'CodeNumberTextBox': f'{captcha}',
        #     'btnSearch': 'Search',
        # }
        data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': f'{view_state}',
            '__VIEWSTATEGENERATOR': 'CA0B0334',
            'ddlbatch': f'{self.ddlbatch}',
            'txtenroll': f'{self.e_number}',
            'txtSheetNo': '',
            'txtpassword': 'M12Soni!@12)', # New Params
            'CodeNumberTextBox': f'{captcha}',
            'btnSearch': 'Search',
        }
        
        # response = self.session.post(url, headers=self.headers, data=data, params=params, cookies=co)
        response = self.session.post(url, headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.gturesults.in',
            'priority': 'u=0, i',
            'referer': 'https://www.gturesults.in/Default.aspx',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        }, data=data, cookies=co)
        
        self.print('response done')
        
        with open(f'./download/{self.e_number}.html', 'w', encoding='utf-8') as f:
            tests = f'{response.text}'.replace('<div id="bodyloader">', '<div id="bodyloader" style="display: none !important;" >'). \
            replace('<style type="text/css">', 
        """<style type="text/css">
        td.Result.NR > *:not(span) {
            display: none !important;
        }
        td.Result.NR {
            padding: 20px !important;
        }
        td.printdiv {
            display: none !important;
        }
        td.header {
            display: none !important;
        }
        #tbRecheck {
            display: none !important;
        }
        .toptable {
            width: min-content !important;
        }""")
            f.write(tests)
        
        text, s = self.get_text(response.text)
        self.print('all done')
        return text, s, self.e_number


if __name__ == '__main__':
    # ddlbatch = '4381$S2024$2024-09-11$current$0'
    ddlbatch = '4378$S2024$2024-08-31$current$0'
    
    list_enroll = [
        # '231430131014',
        '221430142012',
    ]
    
    for i in list_enroll:
        counts = 0
        while True:
            text = DownloadResult(f'{i}', ddlbatch).main_fun()
            print(text)
            if counts > 3 or text[1]:
                break
            
            counts += 1
