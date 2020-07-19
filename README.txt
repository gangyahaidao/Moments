一些操作API说明：
1.参考文档地址：https://www.selenium.dev/documentation/en/webdriver/waits/
2.定位元素：
    1.定位一个元素：
        cheese = driver.find_element(By.ID, "cheese")  返回WebElement类型结果
        cheddar = cheese.find_elements_by_id("cheddar")
        cheddar = driver.find_element_by_css_selector("#cheese #cheddar") 一步到位方式
    2.定位多个元素
        mucho_cheese = driver.find_elements_by_css_selector("#cheese li")
    3.可以通过class、css、id、name attr、link text、partial link text、tag name、xpath定位元素
    4.还可以通过Appium的屏幕录制来进行选定xpath

3.绑定元素动作
    1.输入
        driver.find_element(By.NAME, "name").send_keys('Charles')
    2.拖动
        source = driver.find_element(By.ID, "source")
        target = driver.find_element(By.ID, "target")
        ActionChains(driver).drag_and_drop(source, target).perform()
    3.点击
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
4.延迟等待
    1.WebDriverWait(driver).until(document_initialised)
    2.el = WebDriverWait(driver).until(lambda d: d.find_element_by_tag_name("p"))
    3.WebDriverWait(driver, timeout=3).until(some_condition)
    4.wait = WebDriverWait(driver, 10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div")))
    5.driver.implicitly_wait(10)
5.页面弹框
    1.等待弹框出现，并获取文本，点击OK按钮关闭
        alert = wait.until(expected_conditions.alert_is_present())
        text = alert.text
        alert.accept()
    2.等待弹框出现，点击取消按钮
        wait.until(expected_conditions.alert_is_present())
        alert = driver.switch_to.alert
        text = alert.text
        alert.dismiss()
    3.输入弹框
        wait.until(expected_conditions.alert_is_present())
        alert = Alert(driver)
        alert.send_keys("Selenium")
        alert.accept()