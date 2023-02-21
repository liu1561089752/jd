#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
cron: 0 6 * * *
new Env('东东农场互助');
活动入口: 京东 > 免费水果
脚本功能为: 天天红包互助
'''

import requests
import json
import time
import re
import random
import os

# UA常量
UA = {
    "XiaoMi": '''jdapp;android;11.4.4;;;appBuild/98651;ef/1;ep/{,,,,"ciphertype":5,"version":"1.2.0","appname":"com.jingdong.app.mall"};jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 11; M2006J10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046141 Mobile Safari/537.36''',
    "huawei": '''jdapp;android;11.4.4;;;appBuild/98655;;ep/{,,,,"ciphertype":5,"version":"1.2.0","appname":"com.jingdong.app.mall"};jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 10; TEL-AN10 Build/HONORTEL-AN10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046141 Mobile Safari/537.36'''
}
JD_cks = os.environ.get("JD_COOKIE")
cookies = JD_cks.split("&")
message = ""

# 获取账号信息
def get_User_Info(ck, ua):

    '''
    nickName = "暗夜神魂"
    levelName = "注册用户"
    isPlusVip = "0" str 0不是plus，1是plus
    beanCount = "1012" str
    '''

    nickName = ""
    levelName = ""
    isPlusVip = ""
    beanNum = ""

    url = "https://me-api.jd.com/user_new/info/GetJDUserInfoUnion"
    headers = {
        "cookie": ck,
        "User-Agent": ua,
        "referer": 'https://home.m.jd.com/',
    }
    res_text = requests.get(url=url, headers=headers).text
    try:
        res_json = json.loads(res_text)
        if res_json["retcode"] == "1001":
            # print("登录过期，ck失效")
            return "登录过期，ck失效"
        elif res_json["retcode"] == "0":  # 请求返回数据正确，请求成功
            nickName = res_json["data"]["userInfo"]["baseInfo"]["nickname"]
            levelName = res_json["data"]["userInfo"]["baseInfo"]["levelName"]
            if res_json["data"]["userInfo"]["isPlusVip"] == "0":
                isPlusVip = "普通用户"
            else:
                isPlusVip = "PLUS会员"
            beanNum = res_json["data"]["assetInfo"]["beanNum"]
            data = {
                "nickName": nickName,
                "levelName": levelName,
                "isPlusVip": isPlusVip,
                "beanNum": beanNum
            }
            return data
        else:
            time.sleep(2)
            print(res_text)
    except:
        return False

#收集互助码
def collect_Share_Code(ck,ua):

    url = "https://api.m.jd.com/client.action?functionId=friendListInitForFarm&body={'version':19,'channel':1,'babelChannel':'45'}&appid=wh5&client=android&clientVersion=11.4.4"
    headers = {
        "Host": "api.m.jd.com",
        "User-Agent": ua,
        "Referer": "https://h5.m.jd.com/",
        "Origin": "https://h5.m.jd.com",
        "X-Requested-With": "com.jingdong.app.mall",
        "cookie": ck,
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-encoding": "gzip,deflate,br",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "accept": "*/*"
    }
    res_text = requests.get(url=url, headers=headers).text
    res_json = json.loads(res_text)
    shareCodes = dict()
    with open(file='hzm.txt',mode="r",encoding="utf-8") as f:
        oldcode = f.read()
    friends = res_json["friends"]
    print(friends)
    for friend in friends:
        code = friend["nickName"]
        shareCodes[code] = friend["shareCode"]

    print("share",shareCodes)
    if oldcode != str(shareCodes):
            print(1,oldcode)
            print(shareCodes)
            with open(file='hzm.txt', mode="w",encoding="utf-8") as f:
                f.write(str(shareCodes))

#接受好友邀请
def award_Invite_Friend_For_Farm(ck,ua,shareCode):

    url = 'https://api.m.jd.com/client.action?functionId=initForFarm&body={"imageUrl":"","nickName":"","shareCode":"'+shareCode+'-inviteFriend","version":4,"channel":2}&appid=wh5'
    headers = {
        "Host": "api.m.jd.com",
        "accept": "*/*",
        "Origin": "https://carry.m.jd.com",
        "accept-encoding": "gzip,deflate,br",
        "User-Agent": ua,
        "Referer": "https://carry.m.jd.com/",
        "cookie": ck
    }
    res_text = requests.get(url=url,headers=headers).text
    res_json = json.loads(res_text)
    if res_json["helpResult"]["code"] == "0":
        return "成功！"
    elif res_json["helpResult"]["code"] == "17":
        return "接收邀请成为好友结果失败,对方已是您的好友"
    else:
        print(res_text)

#定义通用请求
def task_Request(ck,ua,functionId,body):

    url = "https://api.m.jd.com/client.action?functionId="+functionId+"&body="+body+"&appid=signed_wh5&client=android&clientVersion=11.4.4"
    headers = {
        "Host": "api.m.jd.com",
        "User-Agent": ua,
        "Referer": "https://h5.m.jd.com/",
        "Origin": "https://h5.m.jd.com",
        "X-Requested-With": "com.jingdong.app.mall",
        "cookie": ck,
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-encoding": "gzip,deflate,br",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "accept": "*/*"
    }
    res_text = requests.get(url=url,headers=headers).text
    try:
        res_json = json.loads(res_text)
        return res_json
    except:
        time.sleep(3)
        print("通用请求错误 ❌")

#定义天天红包通用请求
def task_Red_Paket_Request(ck,ua,functionId,body):

    url = "https://api.m.jd.com/client.action?functionId="+functionId+"&body="+body+"&appid=wh5"
    headers = {
        "Host": "api.m.jd.com",
        "User-Agent": ua,
        "Referer": "https://carry.m.jd.com/",
        "Origin": "https://carry.m.jd.com",
        "X-Requested-With": "com.jingdong.app.mall",
        "cookie": ck,
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-encoding": "gzip,deflate,br",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "accept": "*/*"
    }
    res_text = requests.get(url=url,headers=headers).text
    try:
        res_json = json.loads(res_text)
        return res_json
    except:
        print("❌")

# 天天红包首页数据
def everyday_Red_Paket(ck,ua):

    #天天红包首页数据
    res = task_Red_Paket_Request(ck=ck,ua=ua,functionId="initForTurntableFarm",body='{"version":4,"channel":1}')
    tasks = res["turntableBrowserAds"]
    times = res["remainLotteryTimes"]
    if times == 0:
        print("天天红包抽奖早就完成啦")
        return
    with open(file='hzm.txt', mode="r", encoding="utf-8") as f:
        oldcode = f.read()
    oldcode = json.loads(oldcode)
    for shareCode in oldcode:
        everyday_Red_Packet_help(ck=ck,ua=ua,shareCode=shareCode)
        time.sleep(0.5)

#天天红包内部账号互助
def everyday_Red_Packet_help(ck,ua,shareCode):
    body = '{"shareCode":"'+shareCode+'-3","version":19,"channel":1,"babelChannel":0}'
    res = task_Request(ck=ck,ua=ua,functionId="initForFarm",body=body)
    if res["helpResult"]["code"] == "0":
        print("天天红包助力成功")
    else:
        print(res)

for i in range(len(cookies)):

    redOverPacket = "    过期红包    \n"
    ck = cookies[i]
    if "jd_5871bb8e56dca" in ck:
        ua = UA["huawei"]
    else:
        ua = UA["XiaoMi"]
    resget_User_Info = get_User_Info(ck=ck, ua=ua)
    if resget_User_Info == "登录过期，ck失效":
        pattern = re.compile(r''';pt_pin=(.+);''')
        userName = re.findall(pattern=pattern, string=ck)[0]
        print("【京东账号" + str(i + 1) + " " + userName + "】 ck失效")
        message = message + "【京东账号" + str(i + 1) + " " + userName + "】 ck失效\n"
        continue
    elif resget_User_Info == False:
        userInfo = "【账号" + str(i + 1) + "】 " + resget_User_Info["nickName"] + "\n查询失败，请检查ck"
    else:
        if resget_User_Info["isPlusVip"] == "普通用户":
            userInfo = "【账号" + str(i+1) + "】 " + resget_User_Info["nickName"] + "\n" + "【账号信息】" + "  普通会员" + "\n" + "【当前京豆】" + resget_User_Info["beanNum"] + "豆(≈" +str(int(resget_User_Info["beanNum"])/100) + "元)"
            print(userInfo)
            message = message + userInfo + "\n"
        else:
            userInfo = "【账号" + str(i+1) + "】 " + resget_User_Info["nickName"] + "\n" + "【账号信息】" +  "  Plus会员" + "\n" + "【当前京豆】" + resget_User_Info["beanNum"] + "豆(≈" +str(int(resget_User_Info["beanNum"])/100) + "元)"
            print(userInfo)
            message = message + userInfo + "\n"

    everyday_Red_Paket(ck=ck, ua=ua)
    time.sleep(2)