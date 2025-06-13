import uiautomator2 as u2
from time import sleep

def skip_ad_with_retry(d, max_attempts=5):
    exit_btn_xpath = '//*[@resource-id="hko.MyObservatory_v1_0:id/exit_btn"]'

    for attempt in range(max_attempts):
        try:
            if d.xpath(exit_btn_xpath).exists:
                print(f"clicking exit button, attempt {attempt + 1}")
                d.xpath(exit_btn_xpath).click()
                sleep(3) 
                if not d.xpath(exit_btn_xpath).exists:
                    return True
                
        except Exception as e:
            print(f"click failed: {str(e)}")
            return False
    
    return False  # 超过最大尝试次数

def test_forecast():
    d = u2.connect()
    package_name = "hko.MyObservatory_v1_0"
    d.app_stop(package_name)
    #d.shell(f"pm clear {package_name}")
    sleep(2)
    try:
        d.app_start(package_name)
        sleep(10)
        
        if not skip_ad_with_retry(d):
            raise Exception("无法跳过广告页")
        d.xpath("//android.widget.ImageButton").click()
        sleep(3) 
        #d.xpath("(//android.widget.FrameLayout)[20]").click()
        print("Forecast & Warning Services")
        d(text='Forecast & Warning Services').click()
        sleep(3)
        print("9-Day Forecast")
        d.xpath('(//*[@resource-id="hko.MyObservatory_v1_0:id/title"])[6]').click()
        #d(text='9-Day Forecast').click()
        sleep(3)
        d.screenshot(f"/tmp/1.png")
        d(scrollable=True).scroll.toEnd(max_swipes=10)

        # items = d.xpath("//android.widget.ListView/*").all()
        # for i, item in enumerate(items):
        #     print(f"第{i+1}项:", item.info)
        
        info = d.xpath("//android.widget.ListView/*[last()]").info['contentDescription']
        print(f"The 9th day info: {info}")
    except:
        pass
        #d.app_stop("hko.MyObservatory_v1_0")

test_forecast()
