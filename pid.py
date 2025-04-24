import requests
import pickle as p
import test
import os
import re
import sys
import time
import shutil
import socket
import numpy as np
import pyperclip as pc
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QComboBox
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest,QNetworkReply
from PyQt5.QtCore import QUrl, Qt
from untitled import Ui_MainWindow
from untitled1 import Ui_Formshezhi
from untitled2 import Ui_Formguanyu
from untitled3 import Ui_Formpiliang
from untitled4 import Ui_Formweitongguo
from configparser import RawConfigParser



def dns_validation():
    """DNS解析验证核心函数"""
    target_ip = "192.168.86.1"
    domain = "pid.lvxv.top"

    try:
        # 获取完整的DNS解析信息
        _, _, ip_list = socket.gethostbyname_ex(domain)

        # 多重条件验证
        if not ip_list:
            print("[错误] 域名未解析到任何IP地址")
            return False
        elif target_ip not in ip_list:
            #print(f"[错误] 解析IP {ip_list} 与目标IP {target_ip} 不匹配")
            return False
        return True
    except socket.gaierror as e:
        print(f"[DNS错误] 域名解析失败 ({e})")
        return False
    except socket.timeout:
        print("[超时] DNS服务器响应超时")
        return False
    except Exception as e:
        print(f"[系统错误] 发生未知异常: {e}")
        return False

def panduan(s):
    if len(s) >= 2 and s.startswith('"') and s.endswith('"'):
        return s
    else:
        return f'"{s}"'

def get_bing_url():
    try:
        headers = {
            "User-Agent""": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        }
        response = requests.get("https://api.hn/api.php/?zd=mobile&gs=json&fl=fengjing", timeout=10, headers=headers)
        response.raise_for_status()  # 检查HTTP错误
        data = response.json()
        return data.get("imgurl")
    except requests.exceptions.RequestException as e:
        print("请求异常：", e)
    except ValueError as e:
        print("JSON解析失败：", e)

def fenleibiaoqian(flbq, biaoqian):
    #print(biaoqian)
    if "高热ugc" in biaoqian:
        return "垂类"
    elif ("2025长期红包" in biaoqian) or ("2025抖音三端支付测试" in biaoqian) or ("2024长期红包" in biaoqian):
        return "其他红包"
    elif ("\"203\"" in flbq) or ("\"2955\"" in flbq) or ("\"1804\"" in flbq) or ("\"200\"" in flbq) or ("\"201\"" in flbq) or ("\"202\"" in flbq) or ("\"197\"" in flbq) or ("\"199\"" in flbq):
        return "常规红包"
    elif ("\"177\"" in flbq) or ("\"17143\"" in flbq):
        return "游戏"
    elif ("\"17108\"" in flbq) or ("\"20368\"" in flbq) or ("\"20369\"" in flbq):
        return "短剧"
    elif ("\"215\"" in flbq) or ("\"213\"" in flbq) or ("\"2954\"" in flbq) or ("\"214\"" in flbq) or ("\"2087\"" in flbq):
        return "音乐"
    elif ("\"17065\"" in flbq) or ("\"17066\"" in flbq) or ("\"17067\"" in flbq) or ("\"17068\"" in flbq) or ("\"17069\"" in flbq) or ("\"17070\"" in flbq) or ("\"17071\"" in flbq) or ("\"17072\"" in flbq) or ("\"17073\"" in flbq) or ("\"17074\"" in flbq) or ("\"17075\"" in flbq) or ("\"17076\"" in flbq) or ("\"17077\"" in flbq) or ("\"17078\"" in flbq) or ("\"17079\"" in flbq) or ("\"17080\"" in flbq) or ("\"17133\"" in flbq) or ("\"17134\"" in flbq) or ("\"17081\"" in flbq) or ("\"17327\"" in flbq) or ("\"17483\"" in flbq):
        return "生服"
    elif ("\"4590\"" in flbq) or ("\"4588\"" in flbq) or ("\"4589\"" in flbq) or ("\"4591\"" in flbq) or ("\"4592\"" in flbq) or ("\"4586\"" in flbq) or ("\"4593\"" in flbq) or ("\"4587\"" in flbq) or ("\"7044\"" in flbq) or ("\"8447\"" in flbq) or ("\"7022\"" in flbq) or ("\"8557\"" in flbq) or ("\"8558\"" in flbq) or ("\"17145\"" in flbq) or ("\"17146\"" in flbq) or ("\"18285\"" in flbq) or ("\"17450\"" in flbq):
        return "电商"
    elif "\"1870\"" in flbq:
        return "88元红包"
    else:
        return "垂类"


def get_app_path():
    """返回程序资源路径（打包后的临时目录或脚本目录）"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

def get_config_path():
    """返回用户可写入的配置文件路径"""
    app_name = "pid"  # 替换为你的应用名称
    user_config_dir = os.path.join(os.path.expanduser('~'), '.config', app_name)
    os.makedirs(user_config_dir, exist_ok=True)
    return os.path.join(user_config_dir, 'config.ini')

# 初始化配置文件
def init_config():
    app_path = get_app_path()
    src_config = os.path.join(app_path, 'config.ini')
    dst_config = get_config_path()

    # 如果用户目录下无配置文件，则从资源目录复制
    if not os.path.exists(dst_config):
        shutil.copyfile(src_config, dst_config)

    return dst_config

# 使用配置文件路径
config_file = init_config()
# 后续读写操作均使用config_file路径


class MyPyQT_Form(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MyPyQT_Form,self).__init__()
        self.setupUi(self)
        self.actionagent.triggered.connect(self.actionagent_cb)
        self.actioncookie.triggered.connect(self.actioncookie_cb)
        self.actionpiliang.triggered.connect(self.actionpiliang_cb)
        self.setWindowIcon(QIcon(':/favicon.ico'))
        # 初始化下拉菜单
        self.comboBox.addItems(["常规直达链接", "电商人群", "强插实验", "激励人群", "全量活", "iaa短剧", "生服人群", "ios测试", "素材测试", "原神拉活", "中间页", "H5—中间页"])
        self.comboBox_2.addItems(["内容拉活", "金币拉活", "生服拉活", "电商拉活——低价秒杀", "电商拉活——抽奖（电商红包）"])
        # 绑定信号：一级菜单变动时触发二级菜单更新
        self.comboBox.currentIndexChanged.connect(self.update_city_combo)
        self.manager = QNetworkAccessManager()  # 初始化网络管理器

        url = QUrl(get_bing_url())
        # print(url)
        request = QNetworkRequest(url)
        reply = self.manager.get(request)
        reply.finished.connect(lambda: self.on_image_loaded(reply))

    def update_city_combo(self):
        # 清空二级下拉菜单
        self.comboBox_2.clear()

        # 根据一级菜单动态填充二级菜单
        province = self.comboBox.currentText()
        if province == "常规直达链接":
            self.comboBox_2.addItems(["内容拉活", "金币拉活", "生服拉活", "电商拉活——低价秒杀", "电商拉活——抽奖（电商红包）"])
        elif province == "电商人群":
            self.comboBox_2.addItems(["电商"])
        elif province == "强插实验":
            self.comboBox_2.addItems(["强插实验"])
        elif province == "激励人群":
            self.comboBox_2.addItems(["激励人群&三期——88元", "激励人群&三期——38元、常规金币"])
        elif province == "全量活":
            self.comboBox_2.addItems(["内容", "生服、电商", "热点（自定义标签：高热ugc）", "高价值游戏"])
        elif province == "iaa短剧":
            self.comboBox_2.addItems(["iaa 短剧"])
        elif province == "生服人群":
            self.comboBox_2.addItems(["常规素材（非活动素材）", "活动素材", "闭眼抢"])
        elif province == "ios测试":
            self.comboBox_2.addItems(["常规feed流"])
        elif province == "素材测试":
            self.comboBox_2.addItems(["短剧", "小说", "非激励素材", "一元秒杀", "抽奖", "激励素材", "抖券节", "周一尖叫日", "日日有新", "火锅季", "冰雪季", "今天值得抢", "上新/大牌日"])
        elif province == "原神拉活":
            self.comboBox_2.addItems(["原神"])
        elif province == "中间页":
            self.comboBox_2.addItems(["内容拉活", "金币拉活", "生服&电商拉活"])
        elif province == "H5—中间页":
            self.comboBox_2.addItems(["电商（通投）", "短剧", "小说"])

    def on_image_loaded(self, reply):
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)

            # 自适应标签大小
            scaled_pixmap = pixmap.scaled(
                self.label_14.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label_14.setPixmap(scaled_pixmap)
        else:
            self.label_14.setText(f"加载失败: {reply.errorString()}")

        reply.deleteLater()  # 释放内存

    def actionagent_cb(self):
        my_pyqt_guanyu.open()

    def actioncookie_cb(self):
        my_pyqt_cookie.open()

    def actionpiliang_cb(self):
        my_pyqt_piliang.open()

    def pid_click(self):
        pc.copy(self.textEdit.toPlainText())
    def bid_click(self):
        pc.copy(self.textEdit_2.toPlainText())
    def gid_click(self):
        pc.copy(self.textEdit_12.toPlainText())
    def shijian_click(self):
        pc.copy(self.textEdit_4.toPlainText())
    def sucai_click(self):
        pc.copy(self.textEdit_7.toPlainText())
    def chuangyi_click(self):
        pc.copy(self.textEdit_8.toPlainText())
    def image_url_click(self):
        pc.copy(self.textEdit_6.toPlainText())
    def video_url_click(self):
        pc.copy(self.textEdit_9.toPlainText())
    def lhzdlj_click(self):
        pc.copy(self.textEdit_10.toPlainText())
    def zhantie_click(self):
        try:
            self.textEdit_3.setText(pc.paste())
            self.caxun_click()
        except:
            self.textEdit_5.setText("粘贴失败，请重新粘贴")
    def caxun_click(self):
        self.textEdit_5.setText("查询失败，请检查CID并重试")
        try:
            qdh = self.textEdit_11.toPlainText()
            province = self.comboBox.currentText()
            province_2 = self.comboBox_2.currentText()
            cid = self.textEdit_3.toPlainText()
            cid = str(cid)
            agent = str(config.get('settings', 'agent', fallback=0))
            cookie = str(config.get('settings', 'cookie', fallback=0))
            cid = cid.replace('\n', '').replace('\r', '').replace(' ', '')
            cid = cid[-32:]
            #print(cid)
            url="https://usergrowth.com.cn/chameleon/api/creative/{cid}".format(cid = cid)
            #print(url)
            headers = {
                'User-Agent' : '{agent}'.format(agent = agent),
                "Cookie" : "{cookie}".format(cookie = cookie)
            }

            resp = requests.get(url, headers=headers)
            #print(resp.text)
        except:
            self.textEdit_5.setText("请重试")
            return
        if resp.text == "Unauthorized":
            self.textEdit_5.setText("Cookie已失效，\n请到设置中更新Cookie并重启软件")
        else:
            try:
                try:
                    pid1 = re_pid1.search(resp.text)
                    pid1 = str(pid1)
                    pid = re_pid.search(pid1).group()
                except:
                    pid1 = re_pid1.search(resp.text)
                    pid1 = str(pid1)
                    pid = re_pid.search(pid1)
                #print(pid)
                try:
                    bid1 = re_bid1.search(resp.text)
                    bid1 = str(bid1)
                    bid = re_bid.search(bid1).group()
                except:
                    bid1 = re_bid1.search(resp.text)
                    bid1 = str(bid1)
                    bid = re_bid.search(bid1)
                #print(bid)
                try:
                    gid1 = re_gid1.search(resp.text)
                    gid1 = str(gid1)
                    gid = re_gid.search(gid1).group()
                except:
                    gid1 = re_gid1.search(resp.text)
                    gid1 = str(gid1)
                    gid = re_gid.search(gid1)
                #print(gid)
                try:
                    youxiid1 = re_youxiid1.search(resp.text)
                    youxiid1 = str(youxiid1)
                    youxiid = re_youxiid.search(youxiid1).group()
                except:
                    youxiid1 = re_youxiid1.search(resp.text)
                    youxiid1 = str(youxiid1)
                    youxiid = re_youxiid.search(youxiid1)
                #print(youxiid)

                shijian = re_chuangjianshijian.findall(resp.text)
                shijian = str(shijian)
                #print(shijian)
                scm = re_scm.findall(resp.text)
                scm = str(scm)
                scm = scm.strip('[\'')
                scm = scm.strip('\']')
                #print(scm)
                image_url = re_image_url.findall(resp.text)
                image_url = str(image_url)
                image_url = image_url.strip('[\'')
                image_url = image_url.strip('\']')
                #print(image_url)
                video_url = re_video_url.findall(resp.text)
                video_url = str(video_url)
                video_url = video_url.strip('[\'')
                video_url = video_url.strip('\']')
                #print(video_url)
                cyly = re_cyly.findall(resp.text)
                cyly = str(cyly)
                cyly = cyly.strip('[\'')
                cyly = cyly.strip('\']')
                #print(cyly)
                biaoqian = re_biaoqian.findall(resp.text)
                biaoqian = str(biaoqian)
                biaoqian = biaoqian.strip('[\'')
                biaoqian = biaoqian.strip('\']')
                biaoqian = biaoqian.replace('\",\"', '\n')
                # print(biaoqian)
                flbq = re_flbq.findall(resp.text)
                flbq = str(flbq)
                flbq = flbq.strip('[\'')
                flbq = flbq.strip('\']')
                flbq = fenleibiaoqian(flbq, biaoqian)
                #print(flbq)
                url = QUrl(image_url.strip())
                #print(url)
                request = QNetworkRequest(url)
                reply = self.manager.get(request)
                reply.finished.connect(lambda: self.on_image_loaded(reply))


                #3
                stats3 = re_stats3.findall(resp.text)
                stats3 = str(stats3)
                stats3 = stats3.replace('\']',',\"]')
                if stats3 == "[]":
                    stats3 = "无"
                else:
                    #print(stats3)
                    cost3 = re_cost3.findall(stats3)
                    cost3 = str(cost3)
                    cost3 = cost3.strip('[\'')
                    cost3 = cost3.strip('\']')
                    cost3 = float(cost3)
                    #print(cost3)
                    impression3 = re_impression3.findall(stats3)
                    impression3 = str(impression3)
                    impression3 = impression3.strip('[\'')
                    impression3 = impression3.strip('\']')
                    #print(impression3)
                    click3 = re_click3.findall(stats3)
                    click3 = str(click3)
                    click3 = click3.strip('[\'')
                    click3 = click3.strip('\']')
                    #print(click3)
                    activation3 = re_activation3.findall(stats3)
                    activation3 = str(activation3)
                    activation3 = activation3.strip('[\'')
                    activation3 = activation3.strip('\']')
                    #print(activation3)
                    ad3 = re_ad3.findall(stats3)
                    ad3 = str(ad3)
                    ad3 = ad3.strip('[\'')
                    ad3 = ad3.strip('\']')
                    #print(ad3)
                    ctr3 = re_ctr3.findall(stats3)
                    ctr3 = str(ctr3)
                    ctr3 = ctr3.strip('[\'')
                    ctr3 = ctr3.strip('\']')
                    ctr3 = float(ctr3) * 100
                    #print('%.2f'%ctr3)
                    cvr3 = re_cvr3.findall(stats3)
                    cvr3 = str(cvr3)
                    cvr3 = cvr3.strip('[\'')
                    cvr3 = cvr3.strip('\']')
                    cvr3 = float(cvr3) * 100
                    #print('%.2f'%cvr3)
                    retention3 = re_retention3.findall(stats3)
                    retention3 = str(retention3)
                    retention3 = retention3.strip('[\'')
                    retention3 = retention3.strip('\']')
                    retention3 = float(retention3) * 100
                    #print('%.2f'%retention3)
                    cpa3 = re_cpa3.findall(stats3)
                    cpa3 = str(cpa3)
                    cpa3 = cpa3.strip('[\'')
                    cpa3 = cpa3.strip('\']')
                    cpa3 = float(cpa3)
                    #print(cpa3)
                    cpm3 = float(cost3) / float(impression3) * 1000
                    #print(cpm3)
                #7
                stats7 = re_stats7.findall(resp.text)
                stats7 = str(stats7)
                stats7 = stats7.replace('\']',',\"]')
                if stats7 == "[]":
                    stats7 = "无"
                else:
                    #print(stats7)
                    cost7 = re_cost7.findall(stats7)
                    cost7 = str(cost7)
                    cost7 = cost7.strip('[\'')
                    cost7 = cost7.strip('\']')
                    cost7 = float(cost7)
                    #print(cost7)
                    impression7 = re_impression7.findall(stats7)
                    impression7 = str(impression7)
                    impression7 = impression7.strip('[\'')
                    impression7 = impression7.strip('\']')
                    #print(impression7)
                    click7 = re_click7.findall(stats7)
                    click7 = str(click7)
                    click7 = click7.strip('[\'')
                    click7 = click7.strip('\']')
                    #print(click7)
                    activation7 = re_activation7.findall(stats7)
                    activation7 = str(activation7)
                    activation7 = activation7.strip('[\'')
                    activation7 = activation7.strip('\']')
                    #print(activation7)
                    ad7 = re_ad7.findall(stats7)
                    ad7 = str(ad7)
                    ad7 = ad7.strip('[\'')
                    ad7 = ad7.strip('\']')
                    #print(ad7)
                    ctr7 = re_ctr7.findall(stats7)
                    ctr7 = str(ctr7)
                    ctr7 = ctr7.strip('[\'')
                    ctr7 = ctr7.strip('\']')
                    ctr7 = float(ctr7) * 100
                    #print('%.2f'%ctr7)
                    cvr7 = re_cvr7.findall(stats7)
                    cvr7 = str(cvr7)
                    cvr7 = cvr7.strip('[\'')
                    cvr7 = cvr7.strip('\']')
                    cvr7 = float(cvr7) * 100
                    #print('%.2f'%cvr7)
                    retention7 = re_retention7.findall(stats7)
                    retention7 = str(retention7)
                    retention7 = retention7.strip('[\'')
                    retention7 = retention7.strip('\']')
                    retention7 = float(retention7) * 100
                    #print('%.2f'%retention7)
                    cpa7 = re_cpa7.findall(stats7)
                    cpa7 = str(cpa7)
                    cpa7 = cpa7.strip('[\'')
                    cpa7 = cpa7.strip('\']')
                    cpa7 = float(cpa7)
                    #print(cpa7)
                    cpm7 = float(cost7) / float(impression7) * 1000
                    #print(cpm7)
                #15
                stats15 = re_stats15.findall(resp.text)
                stats15 = str(stats15)
                stats15 = stats15.replace('\']',',\"]')
                if stats15 == "[]":
                    stats15 = "无"
                else:
                    #print(stats15)
                    cost15 = re_cost15.findall(stats15)
                    cost15 = str(cost15)
                    cost15 = cost15.strip('[\'')
                    cost15 = cost15.strip('\']')
                    cost15 = float(cost15)
                    #print(cost15)
                    impression15 = re_impression15.findall(stats15)
                    impression15 = str(impression15)
                    impression15 = impression15.strip('[\'')
                    impression15 = impression15.strip('\']')
                    #print(impression15)
                    click15 = re_click15.findall(stats15)
                    click15 = str(click15)
                    click15 = click15.strip('[\'')
                    click15 = click15.strip('\']')
                    #print(click15)
                    activation15 = re_activation15.findall(stats15)
                    activation15 = str(activation15)
                    activation15 = activation15.strip('[\'')
                    activation15 = activation15.strip('\']')
                    #print(activation15)
                    ad15 = re_ad15.findall(stats15)
                    ad15 = str(ad15)
                    ad15 = ad15.strip('[\'')
                    ad15 = ad15.strip('\']')
                    #print(ad15)
                    ctr15 = re_ctr15.findall(stats15)
                    ctr15 = str(ctr15)
                    ctr15 = ctr15.strip('[\'')
                    ctr15 = ctr15.strip('\']')
                    ctr15 = float(ctr15) * 100
                    #print('%.2f'%ctr15)
                    cvr15 = re_cvr15.findall(stats15)
                    cvr15 = str(cvr15)
                    cvr15 = cvr15.strip('[\'')
                    cvr15 = cvr15.strip('\']')
                    cvr15 = float(cvr15) * 100
                    #print('%.2f'%cvr15)
                    retention15 = re_retention15.findall(stats15)
                    retention15 = str(retention15)
                    retention15 = retention15.strip('[\'')
                    retention15 = retention15.strip('\']')
                    retention15 = float(retention15) * 100
                    #print('%.2f'%retention15)
                    cpa15 = re_cpa15.findall(stats15)
                    cpa15 = str(cpa15)
                    cpa15 = cpa15.strip('[\'')
                    cpa15 = cpa15.strip('\']')
                    cpa15 = float(cpa15)
                    #print(cpa15)
                    cpm15 = float(cost15) / float(impression15) * 1000
                    #print(cpm15)
                #30
                stats30 = re_stats30.findall(resp.text)
                stats30 = str(stats30)
                stats30 = stats30.replace('\']',',\"]')
                if stats30 == "[]":
                    stats30 = "无"
                else:
                    #print(stats30)
                    cost30 = re_cost30.findall(stats30)
                    cost30 = str(cost30)
                    cost30 = cost30.strip('[\'')
                    cost30 = cost30.strip('\']')
                    cost30 = float(cost30)
                    #print(cost30)
                    impression30 = re_impression30.findall(stats30)
                    impression30 = str(impression30)
                    impression30 = impression30.strip('[\'')
                    impression30 = impression30.strip('\']')
                    #print(impression30)
                    click30 = re_click30.findall(stats30)
                    click30 = str(click30)
                    click30 = click30.strip('[\'')
                    click30 = click30.strip('\']')
                    #print(click30)
                    activation30 = re_activation30.findall(stats30)
                    activation30 = str(activation30)
                    activation30 = activation30.strip('[\'')
                    activation30 = activation30.strip('\']')
                    #print(activation30)
                    ad30 = re_ad30.findall(stats30)
                    ad30 = str(ad30)
                    ad30 = ad30.strip('[\'')
                    ad30 = ad30.strip('\']')
                    #print(ad30)
                    ctr30 = re_ctr30.findall(stats30)
                    ctr30 = str(ctr30)
                    ctr30 = ctr30.strip('[\'')
                    ctr30 = ctr30.strip('\']')
                    ctr30 = float(ctr30) * 100
                    #print('%.2f'%ctr30)
                    cvr30 = re_cvr30.findall(stats30)
                    cvr30 = str(cvr30)
                    cvr30 = cvr30.strip('[\'')
                    cvr30 = cvr30.strip('\']')
                    cvr30 = float(cvr30) * 100
                    #print('%.2f'%cvr30)
                    retention30 = re_retention30.findall(stats30)
                    retention30 = str(retention30)
                    retention30 = retention30.strip('[\'')
                    retention30 = retention30.strip('\']')
                    retention30 = float(retention30) * 100
                    #print('%.2f'%retention30)
                    cpa30 = re_cpa30.findall(stats30)
                    cpa30 = str(cpa30)
                    cpa30 = cpa30.strip('[\'')
                    cpa30 = cpa30.strip('\']')
                    cpa30 = float(cpa30)
                    #print(cpa30)
                    cpm30 = float(cost30) / float(impression30) * 1000
                    #print(cpm30)        try:
                if (province == "常规直达链接") & (province_2 == "内容拉活"):
                    if gid == None:
                        dqlj = "snssdk2329://feed?cids={cid}&gd_label=click_schema_lhft_{qdh}&union_site=__UNION_SITE__".format(cid=cid, qdh=qdh)
                    else:
                        dqlj = "snssdk2329://aweme/push_detail?label=release&hot=feed&cold=feed&gids={gid}&cids={cid}&gd_label=click_schema_lhft_{qdh}&union_site=__UNION_SITE__".format(cid=cid, gid=gid, qdh=qdh)
                elif (province == "常规直达链接") & (province_2 == "金币拉活"):
                    dqlj = "snssdk2329://thirdlaunchab?ab_key=douyin_lite_innovation_redpack&fallback_schema=snssdk2329%3A%2F%2Ffeed&use_cache=0&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "常规直达链接") & (province_2 == "金币拉活"):
                    dqlj = "snssdk2329://thirdlaunchab?ab_key=douyin_lite_innovation_redpack&fallback_schema=snssdk2329%3A%2F%2Ffeed&use_cache=0&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "常规直达链接") & (province_2 == "生服拉活"):
                    dqlj = "snssdk2329://polaris/proxy?scene_key=resource_jblh&ug_activity_id=resource&gd_label=click_schema_lhft_{qdh}&union_site=__UNION_SITE__&block_popup_queue=1".format(qdh=qdh)
                elif (province == "常规直达链接") & (province_2 == "电商拉活——低价秒杀"):
                    dqlj = "snssdk2329://thirdlaunchab?ab_key=douyin_lite_lahuo_miaosha_v2&fallback_schema=snssdk2329%3A%2F%2Ffeed&is_material_half_screen=1&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "常规直达链接") & (province_2 == "电商拉活——抽奖（电商红包）"):
                    dqlj = "snssdk2329://thirdlaunchab?ab_key=douyin_lite_lahuo_choujiang_v2&fallback_schema=snssdk2329%3A%2F%2Ffeed&is_material_half_screen=1&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "电商人群") & (province_2 == "电商"):
                    dqlj = "snssdk2329://mall/xtab?enter_from=ds_lahuo_toufang&delivery_type=product_detail&delivery_value={pid}&delivery_extra_params=&force_refresh=1&enable_redirect_with_params=1&delivery_id=30411&gd_label=click_schema_lhft_{qdh}&ug_ecom_tag=1&needlaunchlog=true".format(pid=pid,qdh=qdh)
                elif (province == "强插实验") & (province_2 == "强插实验"):
                    if gid == None:
                        dqlj = "snssdk2329://feed?cids={cid}&gd_label=click_schema_lhft_{qdh}&union_site=__UNION_SITE__".format(cid=cid, qdh=qdh)
                    else:
                        dqlj = "snssdk2329://aweme/push_detail?label=release&hot=feed&cold=feed&gids={gid}&cids={cid}&gd_label=click_schema_lhft_{qdh}&union_site=__UNION_SITE__".format(cid=cid, gid=gid, qdh=qdh)
                elif (province == "激励人群") & (province_2 == "激励人群&三期——88元"):
                    dqlj = "snssdk2329://thirdlaunchab?ab_key=douyin_lite_innovation_88&fallback_schema=snssdk2329%3A%2F%2Ffeed&use_cache=0&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "激励人群") & (province_2 == "激励人群&三期——38元、常规金币"):
                    dqlj = "snssdk2329://thirdlaunchab?ab_key=douyin_lite_innovation_redpack&fallback_schema=snssdk2329%3A%2F%2Ffeed&use_cache=0&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "全量活") & (province_2 == "内容"):
                    if gid == None:
                        dqlj = "snssdk2329://feed?cids={cid}&gd_label=click_schema_lhft_{qdh}&union_site=__UNION_SITE__".format(cid=cid, qdh=qdh)
                    else:
                        dqlj = "snssdk2329://aweme/push_detail?label=release&hot=feed&cold=feed&gids={gid}&cids={cid}&gd_label=click_schema_lhft_{qdh}&union_site=__UNION_SITE__".format(cid=cid, gid=gid, qdh=qdh)
                elif (province == "全量活") & (province_2 == "生服、电商"):
                    dqlj = "snssdk2329://feed?cids={cid}&gd_label=click_schema_lhft_{qdh}&union_site=__UNION_SITE__".format(cid=cid, qdh=qdh)
                elif (province == "全量活") & (province_2 == "热点（自定义标签：高热ugc）"):
                    dqlj = "snssdk2329://aweme/push_detail?label=release&hot=feed&cold=feed&gids={gid}&cids={cid}&gd_label=click_schema_lhft_{qdh}&union_site=__UNION_SITE__".format(cid=cid, gid=gid, qdh=qdh)
                elif (province == "全量活") & (province_2 == "高价值游戏"):
                    dqlj = "snssdk2329://push_universe?cold_schema=snssdk2329%3A%2F%2Fmicrogame%3Fapp_id%3D{youxiid}%26bdp_log%3D%257B%2522launch_from%2522%253A%2522ug%2522%257D%26scene%3D024009%26version%3Dv2%26version_type%3Dcurrent%26bdpsum%3Dd120bde&hot_schema=snssdk2329%3A%2F%2Fmicrogame%3Fapp_id%3D{youxiid}%26bdp_log%3D%257B%2522launch_from%2522%253A%2522ug%2522%257D%26scene%3D024009%26version%3Dv2%26version_type%3Dcurrent%26bdpsum%3Dd120bde&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh,youxiid=youxiid)
                elif (province == "iaa短剧") & (province_2 == "iaa 短剧"):
                    dqlj = "snssdk2329://playlet?playlet_id={pid}&from=toufanglahuo&enter_method=toufanglahuo&gd_label=click_schema_lhft_{qdh}".format(pid=pid,qdh=qdh)
                elif (province == "生服人群") & (province_2 == "常规素材（非活动素材）"):
                    dqlj = "snssdk2329://aweme/push_detail?label=release&hot=feed&cold=feed&gids={gid}&cids={cid}&gd_label=click_schema_lhft_{qdh}&union_site=__UNION_SITE__".format(cid=cid, gid=gid, qdh=qdh)
                elif (province == "生服人群") & (province_2 == "活动素材"):
                    dqlj = "对应素材测试各活动直达链接"
                elif (province == "生服人群") & (province_2 == "闭眼抢"):
                    dqlj = "snssdk2329://webview?url=https%3A%2F%2Fapi.amemv.com%2Flife%2Fmagic%2Fredirect%3Ffaas_redirect_type%3Dbyq%26should_full_screen%3D1%26hide_nav_bar%3D1%26magic_source%3Dug%26enter_from_mofang%3Dug%26enter_from_merge%3Dug&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "ios测试") & (province_2 == "常规feed流"):
                    if gid == None:
                        dqlj = "snssdk2329://feed?gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                    else:
                        dqlj = "snssdk2329://aweme/push_detail?label=release&hot=feed&cold=feed&gids={gid}&gd_label=click_schema_lhft_{qdh}".format(gid=gid, qdh=qdh)
                elif (province == "素材测试") & (province_2 == "短剧"):
                    dqlj = "snssdk2329://thirdlaunchab?ab_key=2717927&fallback_schema=snssdk2329%3A%2F%2Ffeed%3F&gd_label=click_schema_lhft_{qdh}&aweme_id_list={gid}&gids={gid}&enter_method=ug_lahuo_chengjie_two".format(qdh=qdh,gid=gid)
                elif (province == "素材测试") & (province_2 == "小说"):
                    dqlj = "snssdk2329://thirdlaunchab?ab_key=2804862&fallback_schema=snssdk2329%3A%2F%2Ffeed%3F&gd_label=click_schema_lhft_{qdh}&book_id={bid}&enter_method=ug_lahuo_chengjie_two".format(qdh=qdh,bid=bid)
                elif (province == "素材测试") & (province_2 == "非激励素材"):
                    dqlj = "snssdk2329://thirdlaunchab?ab_key=2842921&fallback_schema=snssdk2329%3A%2F%2F&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "素材测试") & (province_2 == "一元秒杀"):
                    dqlj = "snssdk2329://thirdlaunchab?ab_key=douyin_lite_lahuo_miaosha&fallback_schema=snssdk2329%3A%2F%2Ffeed&is_material_half_screen=1&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "素材测试") & (province_2 == "抽奖"):
                    dqlj = "snssdk2329://thirdlaunchab?ab_key=douyin_lite_lahuo_choujiang&fallback_schema=snssdk2329%3A%2F%2Ffeed&is_material_half_screen=1&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "素材测试") & (province_2 == "激励素材"):
                    dqlj = "snssdk2329://thirdlaunchab?ab_key=2842783&fallback_schema=snssdk2329%3A%2F%2F&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "素材测试") & (province_2 == "抖券节"):
                    dqlj = "snssdk2329://thirdlaunchab?ab_key=douyin_lite_lahuo_douquanjie_v2&fallback_schema=snssdk2329%3A%2F%2Ffeed&is_material_half_screen=1&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "素材测试") & (province_2 == "周一尖叫日"):
                    dqlj = "snssdk2329://webview?url=https%3A%2F%2Fapi.amemv.com%2Fmagic%2Feco%2Fruntime%2Frelease%2F663f1616a286a405649889ab%3Fshould_full_screen%3D1%26hide_nav_bar%3D1%26auto_play_bgm%3D1%26container_bg_color%3D%2523fd0000%26loading_bg_color%3D%2523fd0000%26_pia_%3D1%26loader_name%3Dforest%26disable_all_bounces%3D1%26appType%3Ddouyin%26magic_page_no%3D1%26magic_source%3Dmp_default%26enter_from_mofang%3DUG%26enter_from_merge%3DUG%26&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "素材测试") & (province_2 == "日日有新"):
                    dqlj = "snssdk2329://webview?auto_play_bgm=1&allowMediaAutoPlay=1&hide_system_video_poste=1&url=aweme%3A%2F%2Fwebview%3Furl%3Dhttps%253A%252F%252Fapi.amemv.com%252Flife%252Fmagic%252Fredirect%253Ffaas_redirect_type%253Drryx%2526should_full_screen%253D1%2526hide_nav_bar%253D1%2526magic_source%253Dugtoufang%2526enter_from_mofang%253Dugtoufang%2526enter_from_merge%253Dugtoufang%2526disable_pop_gesture%253D1%2526&status_font_dark=1&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "素材测试") & (province_2 == "火锅季"):
                    dqlj = "snssdk2329://webview?url=https%3A%2F%2Fapi.amemv.com%2Fmagic%2Feco%2Fruntime%2Frelease%2F671d24b59e29bf6cee60f52a%3Fshould_full_screen%3D1%26hide_nav_bar%3D1%26auto_play_bgm%3D1%26container_bg_color%3D%2523d51218%26loading_bg_color%3D%2523d51218%26_pia_%3D1%26loader_name%3Dforest%26disable_all_bounces%3D1%26appType%3Ddouyin%26magic_page_no%3D1%26magic_source%3Dmu_opening_8ui1%26enter_from_mofang%3Dopening%26enter_from_merge%3Dopening%26"
                elif (province == "素材测试") & (province_2 == "冰雪季"):
                    dqlj = "snssdk2329://webview?url=https%3A%2F%2Fapi.amemv.com%2Fmagic%2Feco%2Fruntime%2Frelease%2F6715b1ceefada15dc6a777f2%3Fshould_full_screen%3D1%26hide_nav_bar%3D1%26auto_play_bgm%3D1%26container_bg_color%3D%25235EA1FF%26loading_bg_color%3D%25235EA1FF%26_pia_%3D1%26loader_name%3Dforest%26disable_all_bounces%3D1%26appType%3Ddouyin%26magic_page_no%3D1%26magic_source%3Dmu_ug_oj9o%26activity%3D6715b06b91eb53032dde2ce6%26enter_from_mofang%3Dug%26enter_from_merge%3Dug%26disable_pop_gesture%3D1%26"
                elif (province == "素材测试") & (province_2 == "今天值得抢"):
                    dqlj = "snssdk2329://webview?url=https%3A%2F%2Fapi.amemv.com%2Flife%2Fmagic%2Fredirect%3Ffaas_redirect_type%3Djrzdq_double_live%26should_full_screen%3D1%26hide_nav_bar%3D1%26magic_source%3Dug%26enter_from_mofang%3Dug%26enter_from_merge%3Dug"
                elif (province == "素材测试") & (province_2 == "上新/大牌日"):
                    dqlj = "sslocal://webview?url=https%3A%2F%2Fapi.amemv.com%2Fmagic%2Feco%2Fruntime%2Frelease%2F672c4b5ac82c3f928b7d62ad%3Fshould_full_screen%3D1%26hide_nav_bar%3D1%26auto_play_bgm%3D1%26container_bg_color%3D%2523fed5b7%26loading_bg_color%3D%2523fed5b7%26_pia_%3D1%26loader_name%3Dforest%26disable_all_bounces%3D1%26appType%3Ddouyin%26magic_page_no%3D1%26magic_source%3Dmp_default%26activity%3D672c4b3f2a00720330ad1ceb"
                elif (province == "原神拉活") & (province_2 == "原神"):
                    dqlj = "snssdk2329://user/profile/1736848482507527?enter_from=ug_daoliu&gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "中间页") & (province_2 == "内容拉活"):
                    dqlj = "snssdk2329://feed?gd_label=click_schema_lhft_{qdh}".format(qdh=qdh)
                elif (province == "中间页") & (province_2 == "金币拉活"):
                    dqlj = "snssdk2329://lynxview/?should_full_screen=1&prefix=incentive/react_lynx/aggregation&surl=https%3A%2F%2Flf-dy-sourcecdn-tos.bytegecko.com%2Fobj%2Fbyte-gurd-source%2Fincentive%2Freact_lynx%2Faggregation%2Faggregation-reactlynx%2Fpages%2FshoppingAggregation%2Ftemplate.js&retain_popup_type=POPUP_NORMAL&use_bdx=1&enter_from=ad-serving-popup&creator_id=28088003&gd_label=click_schema_lhft_{qdh}&union_site=__UNION_SITE__".format(qdh=qdh)
                elif (province == "中间页") & (province_2 == "生服&电商拉活"):
                    dqlj = "snssdk2329://polaris/proxy?scene_key=resource_jblh&ug_activity_id=resource&gd_label=click_schema_lhft_{qdh}&union_site=__UNION_SITE__&block_popup_queue=1".format(qdh=qdh)
                elif (province == "H5—中间页") & (province_2 == "电商（通投）"):
                    dqlj = "https://ugh5.cn/ug/app/armor/dynamich5?domain=novel_fm&biz=ecom&app_id=2329&ug_pid={pid}&channel={qdh}".format(qdh=qdh,pid=pid)
                elif (province == "H5—中间页") & (province_2 == "短剧"):
                    dqlj = "https://ugh5.cn/ug/app/armor/dynamich5?domain=novel_fm&biz=dy_short_video&app_id=2329&ug_pid={pid}&channel={qdh}&style_version=2".format(qdh=qdh,pid=pid)
                elif (province == "H5—中间页") & (province_2 == "小说"):
                    dqlj = "https://ugh5.cn/ug/app/armor/dynamich5?domain=novel_fm&biz=free_book&app_id=2329&ug_pid={bid}&channel={qdh}&style_version=3".format(qdh=qdh,bid=bid)


            except:
                return
            try:
                self.label_15.setText(f"素材预览: {flbq}")
            except:
                self.label_15.setText("素材预览")
            try:
                self.textEdit_5.setText(biaoqian)
            except:
                self.textEdit_5.setText("")
            try:
                #print(pid)
                self.textEdit.setText(pid)
            except:
                self.textEdit.setText("")
            try:
                #print(bid)
                self.textEdit_2.setText(bid)
            except:
                self.textEdit_2.setText("")
            try:
                #print(gid)
                self.textEdit_12.setText(gid)
            except:
                self.textEdit_12.setText("")
            try:
                shijian = shijian.strip('[\'')
                shijian = shijian.strip('\']')
                shijian = shijian.replace('\',','\n')
                shijian = shijian.replace(' \'', '')
                #print(shijian)
                timeStamp = int(shijian)
                #print(timeStamp)
                timeArray = time.localtime(timeStamp)
                otherStyleTime = time.strftime("%Y/%m/%d", timeArray)
                #print(otherStyleTime)
                self.textEdit_4.setText(otherStyleTime)
            except:
                self.textEdit_4.setText("")
            try:
                self.textEdit_7.setText(scm)
            except:
                self.textEdit_7.setText("")
            try:
                self.textEdit_8.setText(cyly)
            except:
                self.textEdit_8.setText("")
            try:
                self.textEdit_6.setText(image_url)
            except:
                self.textEdit_6.setText("")
            try:
                self.textEdit_9.setText(video_url)
            except:
                self.textEdit_9.setText("")

            try:
                self.textEdit_10.setText(dqlj)
            except:
                self.textEdit_10.setText("")



            try:
                item = QtWidgets.QTableWidgetItem(ad3)
                self.tableWidget.setItem(0,0,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(0, 0, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%cost3)
                self.tableWidget.setItem(0,1,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(0, 1, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%cpa3)
                self.tableWidget.setItem(0,2,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(0, 2, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%retention3+ "%")
                self.tableWidget.setItem(0,3,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(0, 3, item)
            try:
                item = QtWidgets.QTableWidgetItem(impression3)
                self.tableWidget.setItem(0,4,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(0, 4, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%cpm3)
                self.tableWidget.setItem(0,5,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(0, 5, item)
            try:
                item = QtWidgets.QTableWidgetItem(click3)
                self.tableWidget.setItem(0,6,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(0,6,item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%ctr3 + "%")
                self.tableWidget.setItem(0,7,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(0,7,item)
            try:
                item = QtWidgets.QTableWidgetItem(activation3)
                self.tableWidget.setItem(0,8,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(0,8,item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%cvr3 + "%")
                self.tableWidget.setItem(0,9,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(0,9,item)

            try:
                item = QtWidgets.QTableWidgetItem(ad7)
                self.tableWidget.setItem(1,0,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(1, 0, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f' % cost7)
                self.tableWidget.setItem(1, 1, item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(1, 1, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f' % cpa7)
                self.tableWidget.setItem(1, 2, item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(1, 2, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f' % retention7 + "%")
                self.tableWidget.setItem(1, 3, item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(1, 3, item)
            try:
                item = QtWidgets.QTableWidgetItem(impression7)
                self.tableWidget.setItem(1, 4, item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(1, 4, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f' % cpm7)
                self.tableWidget.setItem(1, 5, item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(1, 5, item)
            try:
                item = QtWidgets.QTableWidgetItem(click7)
                self.tableWidget.setItem(1, 6, item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(1, 6, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f' % ctr7 + "%")
                self.tableWidget.setItem(1, 7, item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(1, 7, item)
            try:
                item = QtWidgets.QTableWidgetItem(activation7)
                self.tableWidget.setItem(1, 8, item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(1, 8, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f' % cvr7 + "%")
                self.tableWidget.setItem(1, 9, item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(1, 9, item)

            try:
                item = QtWidgets.QTableWidgetItem(ad15)
                self.tableWidget.setItem(2,0,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(2, 0, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%cost15)
                self.tableWidget.setItem(2,1,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(2, 1, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%cpa15)
                self.tableWidget.setItem(2,2,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(2, 2, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%retention15+ "%")
                self.tableWidget.setItem(2,3,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(2, 3, item)
            try:
                item = QtWidgets.QTableWidgetItem(impression15)
                self.tableWidget.setItem(2,4,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(2, 4, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%cpm15)
                self.tableWidget.setItem(2,5,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(2, 5, item)
            try:
                item = QtWidgets.QTableWidgetItem(click15)
                self.tableWidget.setItem(2,6,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(2,6,item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%ctr15 + "%")
                self.tableWidget.setItem(2,7,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(2,7,item)
            try:
                item = QtWidgets.QTableWidgetItem(activation15)
                self.tableWidget.setItem(2,8,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(2,8,item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%cvr15 + "%")
                self.tableWidget.setItem(2,9,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(2,9,item)

            try:
                item = QtWidgets.QTableWidgetItem(ad30)
                self.tableWidget.setItem(3,0,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(3, 0, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%cost30)
                self.tableWidget.setItem(3,1,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(3, 1, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%cpa30)
                self.tableWidget.setItem(3,2,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(3, 2, item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%retention30+ "%")
                self.tableWidget.setItem(3,3,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(3, 3, item)
            try:
                item = QtWidgets.QTableWidgetItem(impression30)
                self.tableWidget.setItem(3,4,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(3,4,item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%cpm30)
                self.tableWidget.setItem(3,5,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(3,5,item)
            try:
                item = QtWidgets.QTableWidgetItem(click30)
                self.tableWidget.setItem(3,6,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(3,6,item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%ctr30 + "%")
                self.tableWidget.setItem(3,7,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(3,7,item)
            try:
                item = QtWidgets.QTableWidgetItem(activation30)
                self.tableWidget.setItem(3,8,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(3,8,item)
            try:
                item = QtWidgets.QTableWidgetItem('%.2f'%cvr30 + "%")
                self.tableWidget.setItem(3,9,item)
            except:
                item = QtWidgets.QTableWidgetItem("")
                self.tableWidget.setItem(3,9,item)

class MyPyQT_cookie(QtWidgets.QWidget,Ui_Formshezhi):
    def __init__(self):
        super(MyPyQT_cookie,self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(':/favicon.ico'))
    def open(self):
        config.read(config_file, encoding='utf-8')
        agent = str(config.get('settings', 'agent', fallback=0))
        cookie = str(config.get('settings', 'cookie', fallback=0))
        my_pyqt_cookie.textEdit.setText(agent)
        my_pyqt_cookie.textEdit_2.setText(cookie)
        my_pyqt_cookie.textEdit.setText(agent)
        my_pyqt_cookie.textEdit_2.setText(cookie)
        self.show()

    def baicun(self):
        try:
            # 将变量存储到shoplist.data文件中
            agent = self.textEdit.toPlainText()
            cookie = self.textEdit_2.toPlainText()
            config['settings']['agent'] = str(panduan(agent.strip()))
            config['settings']['cookie'] = str(panduan(cookie.strip()))
            with open(config_file, 'w') as configfile:
                config.write(configfile)
            self.close()
        except:
            return


    def guanbi(self):
        self.close()

class MyPyQT_guanyu(QtWidgets.QWidget,Ui_Formguanyu):
    def __init__(self):
        super(MyPyQT_guanyu,self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(':/favicon.ico'))
    def open(self):
        self.show()

class MyPyQT_weitongguo(QtWidgets.QWidget,Ui_Formweitongguo):
    def __init__(self):
        super(MyPyQT_weitongguo,self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(':/favicon.ico'))
    def open(self):
        self.show()

class MyPyQT_piliang(QtWidgets.QWidget,Ui_Formpiliang):
    def __init__(self):
        super(MyPyQT_piliang,self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(':/favicon.ico'))
    def open(self):
        self.show()

    def piliang(self):
        self.textEdit_2.setText("查询失败，请检查CID并重试")
        piliangsj = []
        piliangsj.insert(0, "CID\t")
        piliangsj.insert(1, "消耗\t")
        piliangsj.insert(2, "创建时间\t")
        piliangsj.insert(3, "素材来源\t")
        piliangsj.insert(4, "素材名\t")
        piliangsj.insert(5, "素材方向\t")
        piliangsj.insert(6, "在投计划数\t")
        piliangsj.insert(7, "点击率\t")
        piliangsj.insert(8, "转化率\n")
        cid = self.textEdit.toPlainText()
        cid = str(cid)
        cid = cid.strip('\n').replace('\n', ',')
        #print(cid)
        dataset = cid.split(',')
        #print(dataset)
        for index in range(len(dataset)):
            try:
                try:
                    cid = dataset[index]
                    cid = str(cid)
                    #print(cid)
                    agent = str(config.get('settings', 'agent', fallback=0))
                    cookie = str(config.get('settings', 'cookie', fallback=0))
                    cid = cid.replace('\n', '').replace('\r', '').replace(' ', '')
                    cid = cid[-32:]
                    # print(cid)
                    url = "https://usergrowth.com.cn/chameleon/api/creative/{cid}".format(cid=cid)
                    # print(url)
                    headers = {
                        'User-Agent': '{agent}'.format(agent=agent),
                        "Cookie": "{cookie}".format(cookie=cookie)
                    }

                    resp = requests.get(url, headers=headers)
                    #print(resp.text)
                except:
                    self.textEdit_2.setText("请重试")
                    return
                if resp.text == "Unauthorized":
                    self.textEdit_2.setText("Cookie已失效，\n请到设置中更新Cookie并重启软件")
                else:
                    try:
                        # 7
                        stats7 = re_stats7.findall(resp.text)
                        stats7 = str(stats7)
                        stats7 = stats7.replace('\']', ',\"]')
                        if stats7 == "[]":
                            cost7 = 0.00
                            ad7 = 0.00
                            ctr7 = 0.00
                            cvr7 = 0.00
                        else:
                            #print(stats7)
                            cost7 = re_cost7.findall(stats7)
                            cost7 = str(cost7)
                            cost7 = cost7.strip('[\'')
                            cost7 = cost7.strip('\']')
                            cost7 = float(cost7)

                            ad7 = re_ad7.findall(stats7)
                            ad7 = str(ad7)
                            ad7 = ad7.strip('[\'')
                            ad7 = ad7.strip('\']')
                            #print(ad7)

                            ctr7 = re_ctr7.findall(stats7)
                            ctr7 = str(ctr7)
                            ctr7 = ctr7.strip('[\'')
                            ctr7 = ctr7.strip('\']')
                            ctr7 = float(ctr7) * 100
                            #print('%.2f' % ctr7)

                            cvr7 = re_cvr7.findall(stats7)
                            cvr7 = str(cvr7)
                            cvr7 = cvr7.strip('[\'')
                            cvr7 = cvr7.strip('\']')
                            cvr7 = float(cvr7) * 100
                            #print('%.2f' % cvr7)

                        shijian = re_chuangjianshijian.findall(resp.text)
                        shijian = str(shijian)
                        #print(shijian)
                        shijian = shijian.strip('[\'')
                        shijian = shijian.strip('\']')
                        shijian = shijian.replace('\',', '\n')
                        shijian = shijian.replace(' \'', '')
                        #print(shijian)
                        timeStamp = int(shijian)
                        #print(timeStamp)
                        timeArray = time.localtime(timeStamp)
                        otherStyleTime = time.strftime("%Y/%m/%d", timeArray)
                        #print(otherStyleTime)
                        cyly = re_cyly.findall(resp.text)
                        cyly = str(cyly)
                        cyly = cyly.strip('[\'')
                        cyly = cyly.strip('\']')
                        #print(cyly)
                        scm = re_scm.findall(resp.text)
                        scm = str(scm)
                        scm = scm.strip('[\'')
                        scm = scm.strip('\']')
                        #print(scm)
                        biaoqian = re_biaoqian.findall(resp.text)
                        biaoqian = str(biaoqian)
                        biaoqian = biaoqian.strip('[\'')
                        biaoqian = biaoqian.strip('\']')
                        biaoqian = biaoqian.replace('\",\"', '\n')
                        # print(biaoqian)
                        flbq = re_flbq.findall(resp.text)
                        flbq = str(flbq)
                        flbq = flbq.strip('[\'')
                        flbq = flbq.strip('\']')
                        flbq = fenleibiaoqian(flbq, biaoqian)
                        #print(flbq)

                    except:
                        return

                #piliangsj = str(cost7) + "\t" + str(otherStyleTime) + "\t" + str(cyly) + "\t" + str(scm)
                piliangsj.insert(index*9+10,str(cid) + "\t")
                piliangsj.insert(index*9+11,str('%.2f'%cost7) + "\t")
                piliangsj.insert(index*9+12,str(otherStyleTime) + "\t")
                piliangsj.insert(index*9+13,str(cyly) + "\t")
                piliangsj.insert(index*9+14,str(scm) + "\t")
                piliangsj.insert(index*9+15,str(flbq) + "\t")
                piliangsj.insert(index*9+16,str(ad7) + "\t")
                piliangsj.insert(index*9+17,str('%.2f' % ctr7 + "%") + "\t")
                piliangsj.insert(index*9+18,str('%.2f' % cvr7 + "%") + "\n")
            except:
                return

        piliangsj = "".join(piliangsj)
        #print(piliangsj)
        self.textEdit_2.setText(piliangsj)


    def piliangfz(self):
        pc.copy(self.textEdit_2.toPlainText())


if __name__ == '__main__':
    socket.setdefaulttimeout(8)
    if dns_validation():
        print("验证通过，启动主程序...")
        app = QtWidgets.QApplication(sys.argv)
        my_pyqt_form = MyPyQT_Form()
        my_pyqt_cookie = MyPyQT_cookie()
        my_pyqt_guanyu = MyPyQT_guanyu()
        my_pyqt_piliang = MyPyQT_piliang()
        my_pyqt_form.show()
        re_pid1 = re.compile(r'(pid(.*?)")|(playlet_id(.*?)")')
        re_pid = re.compile(r'\d{19}')
        re_bid1 = re.compile(r'bid(.*?)"')
        re_bid = re.compile(r'\d{19}')
        re_gid1 = re.compile(r'gid_(.*?)"')
        re_gid = re.compile(r'\d{19}')
        re_youxiid1 = re.compile(r'youxi_(.*?)"')
        re_youxiid = re.compile(r'(?<=youxi_)[a-z0-9]{0,}')
        re_flbq = re.compile(r'(?<="category_tag":\[)(.*?)\]')
        re_scm = re.compile(r'"file_name":"(.*?)",')
        re_image_url = re.compile(r'"image_url":"(.*?)"')
        re_video_url = re.compile(r'"video_url":"(.*?)"')
        re_cyly = re.compile(r'"seo_keywords":\["(.*?)",')
        re_stats3 = re.compile(r'"lifetime_3d_ad_stats":\{(.*?)\}')
        re_cost3 = re.compile(r'"cost":(.*?),\"')
        re_impression3 = re.compile(r'"impression_cnt":(.*?),\"')
        re_click3 = re.compile(r'"click_cnt":(.*?),\"')
        re_activation3 = re.compile(r'"activation_cnt":(.*?),\"')
        re_ad3 = re.compile(r'"ad_cnt":(.*?),\"')
        re_ctr3 = re.compile(r'"ctr":(.*?),\"')
        re_cvr3 = re.compile(r'"cvr":(.*?),\"')
        re_retention3 = re.compile(r'"d1_retention_rate":(.*?),\"')
        re_cpa3 = re.compile(r'"cpa":(.*?),\"')
        re_stats7 = re.compile(r'"lifetime_7d_ad_stats":\{(.*?)\}')
        re_cost7 = re.compile(r'"cost":(.*?),\"')
        re_impression7 = re.compile(r'"impression_cnt":(.*?),\"')
        re_click7 = re.compile(r'"click_cnt":(.*?),\"')
        re_activation7 = re.compile(r'"activation_cnt":(.*?),\"')
        re_ad7 = re.compile(r'"ad_cnt":(.*?),\"')
        re_ctr7 = re.compile(r'"ctr":(.*?),\"')
        re_cvr7 = re.compile(r'"cvr":(.*?),\"')
        re_retention7 = re.compile(r'"d1_retention_rate":(.*?),\"')
        re_cpa7 = re.compile(r'"cpa":(.*?),\"')
        re_stats15 = re.compile(r'"lifetime_15d_ad_stats":\{(.*?)\}')
        re_cost15 = re.compile(r'"cost":(.*?),\"')
        re_impression15 = re.compile(r'"impression_cnt":(.*?),\"')
        re_click15 = re.compile(r'"click_cnt":(.*?),\"')
        re_activation15 = re.compile(r'"activation_cnt":(.*?),\"')
        re_ad15 = re.compile(r'"ad_cnt":(.*?),\"')
        re_ctr15 = re.compile(r'"ctr":(.*?),\"')
        re_cvr15 = re.compile(r'"cvr":(.*?),\"')
        re_retention15 = re.compile(r'"d1_retention_rate":(.*?),\"')
        re_cpa15 = re.compile(r'"cpa":(.*?),\"')
        re_stats30 = re.compile(r'"lifetime_30d_ad_stats":\{(.*?)\}')
        re_cost30 = re.compile(r'"cost":(.*?),\"')
        re_impression30 = re.compile(r'"impression_cnt":(.*?),\"')
        re_click30 = re.compile(r'"click_cnt":(.*?),\"')
        re_activation30 = re.compile(r'"activation_cnt":(.*?),\"')
        re_ad30 = re.compile(r'"ad_cnt":(.*?),\"')
        re_ctr30 = re.compile(r'"ctr":(.*?),\"')
        re_cvr30 = re.compile(r'"cvr":(.*?),\"')
        re_retention30 = re.compile(r'"d1_retention_rate":(.*?),\"')
        re_cpa30 = re.compile(r'"cpa":(.*?),\"')
        re_biaoqian = re.compile(r'common_hashtags":\["(.*?)"\],')
        re_chuangjianshijian = re.compile(r'create_timestamp":(.*?),\"')
        config = RawConfigParser()
        config.read(config_file, encoding='utf-8')
        agent = str(config.get('settings', 'agent', fallback=0))
        cookie = str(config.get('settings', 'cookie', fallback=0))
        my_pyqt_cookie.textEdit.setText(agent)
        my_pyqt_cookie.textEdit_2.setText(cookie)
        sys.exit(app.exec_())
    else:
        print("验证未通过")
        app = QtWidgets.QApplication(sys.argv)
        my_pyqt_weitongguo = MyPyQT_weitongguo()
        my_pyqt_weitongguo.show()
        sys.exit(app.exec_())