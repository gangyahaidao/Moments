from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Demo(object):
    def __init__(self):
        # DXL4C18829004024       device product:JSN-AL00 model:JSN_AL00 device:HWJSN-H transport_id:1
        # 查看不同应用appActivity命令，手机上要先打开要查看的App：adb shell dumpsys window w|findstr \/|findstr name=
        self.desired_caps = {
            'platformName': 'Android',
            'deviceName': 'HWJSN-H',
            'appPackage': 'com.tencent.mm',
            'appActivity': '.ui.LauncherUI',
            'noReset': True
        }
        self.server = 'http://localhost:4723/wd/hub'
        self.driver = webdriver.Remote(self.server, self.desired_caps) # 启动微信App
        self.wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1) # 指定等待最长时间，和查询DOM频率

    def resolve_popup_windows(self):
        try:
            els = self.driver.find_elements_by_class_name('android.widget.Button')
            while True:
                for el in els:
                    print(el.text)
                    if el.text == u'允许':
                        self.driver.find_element_by_android_uiautomator('new UiSelector().text("允许")').click()
                    elif el.text == u'始终允许':
                        self.driver.find_element_by_android_uiautomator('new UiSelector().text("始终允许")').click()
                    elif el.text == u'确定':
                        self.driver.find_element_by_android_uiautomator('new UiSelector().text("确定")').click()
                    elif el.text == u'我知道了':
                        self.driver.find_element_by_android_uiautomator('new UiSelector().text("我知道了")').click()
                    elif el.text == u'是':
                        self.driver.find_element_by_android_uiautomator('new UiSelector().text("是")').click()
                    elif el.text == u'暂不设置':
                        self.driver.find_element_by_android_uiautomator('new UiSelector().text("暂不设置")').click()
        except:
            print('未检测到弹窗')

    def login(self):
        # 等待登录界面出现，并点击登录按钮
        login = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/fam')))  # 参数为一个元组
        login.click()

        # 输入用户名，并点击下一步
        phone = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/bhn')))
        phone.set_text('16673928888')
        next_step = self.driver.find_element_by_id('com.tencent.mm:id/e3i')
        next_step.click()

        # 处理消息弹框
        WebDriverWait(self.driver, timeout=3).until(lambda d: d.find_element_by_android_uiautomator('new UiSelector().text("我知道了")'))
        self.resolve_popup_windows()

        # 处理微信权限管理弹框
        WebDriverWait(self.driver, timeout=3).until(lambda d: d.find_element_by_android_uiautomator('new UiSelector().text("确定")'))
        self.resolve_popup_windows()

        # 输入密码
        form_input_password = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/fd2')))
        password = form_input_password.find_elements_by_id('com.tencent.mm:id/bhn')
        password.set_text('xxxxxx')

        #点击登录
        login_btn = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/e3i')))
        login_btn.click()

    def enter_first_group(self):
        self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/e3x')))
        items = self.driver.find_elements(By.ID, 'com.tencent.mm:id/e3x')
        print('输出界面会话名称')
        item1 = items[0]
        item1.click()

        # 点击群右上角
        right_up_conner = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cj')))
        right_up_conner.click()

        # 查找聊天记录框栏
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/f43')))
            items = self.driver.find_elements(By.ID, 'android:id/title') # 群人数较少执行流程
            print(len(items))
            if len(items) > 0:
                for item in items:
                    if item.text == '查找聊天记录':
                        item.click()
                        break
        except TimeoutException as e:
            print('超时，需要进行屏幕滑动')
            start_x = self.driver.get_window_size()["width"]
            start_y = self.driver.get_window_size()["height"]
            find_chat_history = False
            while not find_chat_history:
                items = self.driver.find_elements(By.ID, 'android:id/title')
                print(len(items))
                if len(items) > 0:
                    for item in items:
                        if item.text == '查找聊天记录':
                            item.click()
                            find_chat_history = True
                            break
                    try:
                        self.driver.swipe(start_x * 0.2, start_y * 0.5, start_x * 0.2, start_y * 0.3)  # 向上滑动
                    except Exception:
                        pass
                else:
                    try:
                        self.driver.swipe(start_x * 0.2, start_y * 0.5, start_x * 0.2, start_y * 0.3)  # 向上滑动
                    except Exception:
                        pass

        # 输入查找内容
        input_search = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/bhn')))
        input_search.set_text('收到')

        # 先查找f94，然后定位e3x的text属性为用户名，然后是g9g属性text为时间，最后是dvh的text属性表示回答的消息
        self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/f94')))
        items = self.driver.find_elements(By.ID, 'com.tencent.mm:id/f94')
        for item in items:
            nickname = item.find_element_by_id('com.tencent.mm:id/e3x')
            print('nickname', nickname.get_attribute('text'))
            time = item.find_element_by_id('com.tencent.mm:id/g9g')
            print('time', time.get_attribute('text'))
            message = item.find_element_by_id('com.tencent.mm:id/dvh')
            print('message', message.get_attribute('text'))


if __name__ == '__main__':
    weixin = Demo()
    #weixin.login() # 使用noReset参数，保留原始数据，不需重新登录

    # 点击进入第一个群
    weixin.enter_first_group()
