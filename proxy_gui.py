import wx
import re
import requests
from lxml import etree

class get_the_data(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Proxy Test', size=(420, 250))
        panel = wx.Panel(self, -1,(100,100))

        self.jpg = wx.Icon('./imag/tb.jpeg', wx.BITMAP_TYPE_JPEG)

        self.SetIcon(self.jpg)
        
        ip_txt = wx.StaticText(panel, wx.ID_ANY, "IP", (30, 25))  # IP文本位置

        port_txt = wx.StaticText(panel, wx.ID_ANY, "port", (230, 25))  # 端口文本位置

        output_txt = wx.StaticText(panel, wx.ID_ANY, "put", (30, 110))  # 输出文本位置

        self.ip_txt_input = wx.TextCtrl(panel, pos=(60, 20), size=(150, 30))  # IP文本框位置

        self.port_txt_input = wx.TextCtrl(panel, pos=(270, 20), size=(110, 30))  # 端口文本框位置

        self.output_txt_input = wx.TextCtrl(panel, pos=(60, 70), size=(320, 100))  # 输出文本框位置

        self.button = wx.Button(panel, -1, u"验证", pos=(300, 180))  # 验证按钮位置

        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()
        self.clicked_times = 0


    def OnClick(self, event, respones_ip=None):
        ip = self.ip_txt_input.GetValue()
        port = self.port_txt_input.GetValue()
        url = 'http://www.cip.cc'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
        proxy_ip = ip + ':' + port
        proxy = {
            'http': proxy_ip
        }
        try:
            timeout = int(5)
            response = requests.get(url=url, headers=headers, proxies=proxy, timeout=timeout)
            response = str(response.text)

            response = response.replace('	: ', ':')

            obj = re.compile(r'<body>.*?<div class="data kq-well">.*?<pre>IP:(?P<ip>.*?)地址.*?数据二:(?P<yys>.*?)数据三:(?P<sjs>.*?)URL.*?</pre>',re.S)

            result = obj.finditer(response)
            for nam in result:
                data = "IP地址是:"  + nam.group("ip") +  '\n' + 'IP归属地:' +  nam.group("yys")  + 'IP运营商:' +  nam.group("sjs")
                datalog = '-------------------------------\n' + proxy_ip +'\n' + nam.group("yys") + nam.group("sjs") +'-------------------------------'
                self.output_txt_input.SetValue(data)
                file_handle = open('./access.log', mode='a')
                file_handle.write(datalog)
        except:
            self.output_txt_input.SetValue('被测代理' + proxy_ip + '未存活，请检查后重新输入！')
            pass


if __name__ == '__main__':
    app = wx.App()
    frame = get_the_data()
    frame.Show()
    app.MainLoop()

