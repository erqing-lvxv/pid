import requests
import pickle as p
import test
import os
import re
import sys
import pyperclip as pc

session = requests.session()
session.cookies.set("uid_tt_ss","e3e4503137de87daaded0b5067ab2079",path="/",domain="usergrowth.com.cn")
session.cookies.set("uid_tt","e3e4503137de87daaded0b5067ab2079",path="/",domain="usergrowth.com.cn")
session.cookies.set("store-region-src","uid",path="/",domain="usergrowth.com.cn")
session.cookies.set("store-region","cn-ah",path="/",domain="usergrowth.com.cn")
session.cookies.set("ssid_ucp_v1","1.0.0-KDUyZGMxZjdiNWVlMmNmMTFiZGE1NjdmNjU4ZWQyNDQzZjllMWYxNzgKFwjg3oCL0s2gBBD64tWyBhiDETgBQOoHGgJscSIgZTNiZjZhMjdiMGMwNjQ2ZGU2NzA0MzI2NzBmNzAwYjU",path="/",domain="usergrowth.com.cn")
session.cookies.set("sid_ucp_v1","1.0.0-KDUyZGMxZjdiNWVlMmNmMTFiZGE1NjdmNjU4ZWQyNDQzZjllMWYxNzgKFwjg3oCL0s2gBBD64tWyBhiDETgBQOoHGgJscSIgZTNiZjZhMjdiMGMwNjQ2ZGU2NzA0MzI2NzBmNzAwYjU",path="/",domain="usergrowth.com.cn")
session.cookies.set("sid_tt","e3bf6a27b0c0646de670432670f700b5",path="/",domain="usergrowth.com.cn")
session.cookies.set("sid_guard","e3bf6a27b0c0646de670432670f700b5%7C1716875642%7C5184000%7CSat%2C+27-Jul-2024+05%3A54%3A02+GMT",path="/",domain="usergrowth.com.cn")
session.cookies.set("sessionid_ss","e3bf6a27b0c0646de670432670f700b5",path="/",domain="usergrowth.com.cn")
session.cookies.set("sessionid","e3bf6a27b0c0646de670432670f700b5",path="/",domain="usergrowth.com.cn")
session.cookies.set("passport_csrf_token_default","e27ebdd24f94800fc2d72dc3b2b30486",path="/",domain="usergrowth.com.cn")
session.cookies.set("passport_csrf_token","e27ebdd24f94800fc2d72dc3b2b30486",path="/",domain="usergrowth.com.cn")
session.cookies.set("n_mh","9-mIeuD4wZnlYrrOvfzG3MuT6aQmCUtmr8FxV8Kl8xY",path="/",domain="usergrowth.com.cn")
session.cookies.set("chameleon-token","f4cbdac6-541d-4a1f-b5ee-b633c3ca5e4d",path="/",domain="usergrowth.com.cn")
session.cookies.set("ccid","6b93451cae020d601cf6a5fe823c7b10",path="/",domain="usergrowth.com.cn")
session.cookies.set("business_account_token","dU3caAYL5H1fpZ46_NMLIO3VKLS_OW9by1wSClLdY9j-C9I%3D",path="/",domain="usergrowth.com.cn")
session.cookies.set("bigfish_customer_token","RN5Cbc5xcYDa6DyuHVOMPDmtwDPmlbU%3D",path="/",domain="usergrowth.com.cn")
session.cookies.set("bigfish_csrf_token","a58484e7-3034-410c-91d0-3d68a0a16836",path="/",domain="usergrowth.com.cn")

url="https://usergrowth.com.cn/activation_data"

resp = session.get(url=url)
print(resp.text)
print("本次请求使用的cookie：",resp.request.headers.get("Cookie"))
print("会话现有cookie：",session.cookies)