# coding: utf-8
#
"""
 主要流程是：
 0. 点亮屏幕，杀掉所有在运行程序
 1. 进入抖音，判断是否有广告，如有则跳过开屏广告
 2. 暂停视频自动播放
 3. 点赞，如果未登录进入第4步
 4. 进入登录界面
 5. 自动填充手机号，并发送获取验证码请求
 6. 进入短信APP，解析出短信验证码
 7. 进入抖音，自动输入验证码，跳转
 8. 跳过查看联系人界面
 9. 判断，如未点赞则点赞
"""
import time

import uiautomator2 as u2
import re

# 控件包名: 短信
START_SMS = "com.oneplus.mms"
# 控件包名: 抖音
START_TIK_TOK = "com.ss.android.ugc.aweme"
# 控件文字：跳过
SKIP_TEXT = "跳过"
# 控件文字: 验证码
AUTH_CODE = "验证码"
# 控件文字: 跳过广告
SKIP_AD_TEXT = "跳过广告"
# 控件文字：小视频界面-选中（已点赞）
SELECTED_TEXT = "已选中"
# 控件文字：小视频界面-未选中（未点赞）
UN_SELECTED_TEXT = "未选中"
# 控件文字: 一键登录
SPEED_LOGIN_TEXT = "一键登录"
# 控件id: 短信Item TextView id
SMS_CODE_ID = "com.oneplus.mms:id/value"
# 控件id: 收藏按钮的 id
FAVOR_ID = "com.ss.android.ugc.aweme:id/alx"
# 控件id: 任务状态栏 id
BACK_HOME_ID = "com.android.systemui:id/back"
# 控件id: 暂停视频 id
PAUSE_VIDEO_ID = "com.ss.android.ugc.aweme:id/b0q"
# 控件id: 获取短信验证码 id
GET_MSM_CODE_BTN_ID = "com.ss.android.ugc.aweme:id/b_l"
# 控件id: 清除按钮 id
CLEAR_PROCESSES_ID = "net.oneplus.launcher:id/clear_all_button"
# 控件id: 任务栏 id
BACKGROUND_PROCESSES_MANAGER_ID = "com.android.systemui:id/recent_apps"
# 本机电话号码
TEL_PHONE = "15696367893"

d = u2.connect()


def get_sms_code():
    """ 获取短信验证码并输入 """
    # 打开短信
    d.app_start(START_SMS)
    # 点进第一条短信
    d(text=AUTH_CODE).click()
    time.sleep(10)

    # 拿到验证码的text
    value = d(resourceId=SMS_CODE_ID)[1].get_text()
    print(value)
    count = re.compile("\\d{4}")
    auth_codes = count.finditer(value)
    auth_code = 0
    for i in auth_codes:
        auth_code = i.group()
        print(i.group())

    # 打开抖音
    d.app_start(START_TIK_TOK)
    # 键入验证码
    d.send_keys(auth_code, clear=True)


def login():
    """ 登录 """
    # 点击"其他账号 登录"
    d.click(0.574, 0.896)
    # 键入电话号码
    d.send_keys(TEL_PHONE, clear=True)
    # 点击"获取短信验证码"
    d(resourceId=GET_MSM_CODE_BTN_ID).click()
    # 拿到短信验证码
    get_sms_code()
    # 跳过查看联系人界面
    d(text=SKIP_TEXT).click()


def kill_all_processes():
    """ 杀死所有在运行程序 """
    d(resourceId=BACKGROUND_PROCESSES_MANAGER_ID).click()
    if d(resourceId=CLEAR_PROCESSES_ID).exists():
        d(resourceId=CLEAR_PROCESSES_ID).click()
        print("清除所有在运行程序")
    else:
        d(resourceId="com.android.systemui:id/back").click()
        print("后台没有程序在运行")


def judgement_is_liked():
    """ 这是一判断是否点赞，如未点赞，则点赞 """
    if d(descriptionContains=UN_SELECTED_TEXT).exists():
        d(resourceId=FAVOR_ID).click()
        print("未点赞，进行点赞")
    elif d(descriptionContains=SELECTED_TEXT).exists():
        print("已经登录并点赞过了")


def judgement_is_login():
    """ 判断是否出现登录界面，如出现则进行登录 """
    if d(text=SPEED_LOGIN_TEXT).exists():
        print("未登录，进行登录")
        login()
    else:
        print("已经登录")


def pause_video():
    """ 暂停视频 """
    d(resourceId=PAUSE_VIDEO_ID).click()


def skip_ad():
    """ 判断是否有广告，如有则点击跳过 """
    if d(text=SKIP_AD_TEXT).exists():
        d(text=SKIP_AD_TEXT).click()
        print("有广告，点击跳过")
    else:
        print("没有广告")


def main():
    # 唤醒屏幕
    d.screen_on()
    # 杀死所有程序
    kill_all_processes()
    # 打开抖音
    d.app_start(START_TIK_TOK)
    # 等待2秒
    time.sleep(3)
    # 跳过广告
    skip_ad()
    # 暂停视频
    pause_video()
    # 判断是否点赞，如未点赞，则点赞
    judgement_is_liked()
    # 判断是否登录，如未登录则登录
    judgement_is_login()
    # 再次判断是否已经点赞，如未点赞，则点赞
    judgement_is_liked()


if __name__ == '__main__':
    main()
