# @Author: 郭盖
# @FileName: tanchishe.py
# @DateTime: 2022/12/11 15:53
# @SoftWare:  PyCharm
import multiprocessing
import requests
import time
#谷歌浏览器中
# CSRF，ID在你要领取的直播奖励界面点进去进去F12再F5刷新看到网络中有一个链接(https://api.bilibili.com/x/activity/mission/single_task?csrf=xx&id=xx)可以看到
csrf = ""
id = ""
cookie = ""
# 奖励领取资格查询
def isCan():
    """
    :return:!0有资格
            0无资格
    """
    url = f"https://api.bilibili.com/x/activity/mission/single_task?csrf={csrf}&id={id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "cookie": cookie,
    }
    res = requests.get(url, headers=headers).json()
    flage = res['data']['task_info']['receive_id']
    # print(res['data']['task_info'])
    if flage>0:
        return res['data']['task_info']
    else:
        return 0
# print(isCan())
def getaword():
    info=isCan()
    url = "https://api.bilibili.com/x/activity/mission/task/reward/receive"
    headers = {
        "User-Agent": "",
        "cookie": cookie,
    }
    data = {
        "csrf": csrf,
        "receive_from": "missionLandingPage",
        "receive_id": info['receive_id'],
        "group_id": info['group_list'][0]['group_id'],
        "task_id": info['id'],
        "act_id": info['act_id'],
    }
    print(data)
    # data={
    #     "csrf":CSRF,
    #     "receive_from":"missionLandingPage",
    #     "receive_id":685407,
    #     "group_id":0,
    #     "task_id":2253,
    #     "act_id":586,
    # }
    res=requests.post(url,headers=headers,data=data).json()
    print(res)
    # pass


if __name__ == '__main__':
    result=None
    while(True):
        result=isCan()
        if(result!=0):
            print("已经获取到资格")
            break
        time_str=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(time_str+":等待领取资格")
        time.sleep(1)
    time1 = time.perf_counter()
    #线程数
    pool = multiprocessing.Pool(10)
    #一共跑几次
    task_number = 100
    for i in range(task_number):
        pool.apply_async(func=getaword, args=())
    pool.close()
    pool.join()
    time2 = time.perf_counter()
    times = time2 - time1
    print(times / task_number)  # 每次请求用时
