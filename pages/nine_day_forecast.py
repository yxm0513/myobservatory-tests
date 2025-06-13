import uiautomator2 as u2
from time import sleep
import re
from typing import Dict


class NineDayForecastPage:
    def __init__(self):
        self.d = u2.connect()
        self.app = "hko.MyObservatory_v1_0"
        self.d.app_stop(self.app)
        sleep(2)
        self.d.app_start(self.app)

    def skip_ad_with_retry(self, max_attempts=5):
        exit_btn_xpath = '//*[@resource-id="hko.MyObservatory_v1_0:id/exit_btn"]'

        for attempt in range(max_attempts):
            try:
                if self.d.xpath(exit_btn_xpath).exists:
                    print(f"clicking exit button, attempt {attempt + 1}")
                    self.d.xpath(exit_btn_xpath).click()
                    sleep(3)  # 等待页面响应
                    
                    # 验证是否成功跳过
                    if not self.d.xpath(exit_btn_xpath).exists:
                        return True
                    
            except Exception as e:
                print(f"click failed: {str(e)}")
        
        return False

    def open_9day_forecast(self):
        try:
            sleep(4)
            if not self.skip_ad_with_retry():
                raise Exception("failed to skip ad page")
            self.d.xpath("//android.widget.ImageButton").click()
            sleep(3) 
            #d.xpath("(//android.widget.FrameLayout)[20]").click()
            print("Forecast & Warning Services")
            self.d(text='Forecast & Warning Services').click()
            sleep(3)
            print("9-Day Forecast")
            self.d.xpath('(//*[@resource-id="hko.MyObservatory_v1_0:id/title"])[6]').click()
            #d(text='9-Day Forecast').click()
            sleep(3)
            self.d.screenshot(f"/tmp/1.png")
            
        except Exception as e:
            print(f"test failed: {str(e)}")

    def parse_weather_forecast(self, forecast_text: str) -> Dict[str, str]:

        # 初始化结果字典
        forecast = {
            'date': None,
            'forecast': None,
            'temp_range': None,
            'humidity': None,
            'rain_probability': None,
            'wind': None
        }
        lines = [line.strip() for line in forecast_text.split('\n') if line.strip()]
        
        try:
            forecast['date'] = lines[0]
            
            # 解析温度和湿度（从第二行开始）
            for line in lines[1:]:
                if 'Temperature will range between' in line:
                    temp_match = re.search(r'between (\d+) and (\d+) degree Celsius', line)
                    if temp_match:
                        forecast['temp_range'] = f"{temp_match.group(1)}-{temp_match.group(2)}°C"
                
                elif 'Relative Humidity will range between' in line:
                    humid_match = re.search(r'between (\d+) and (\d+) percent', line)
                    if humid_match:
                        forecast['humidity'] = f"{humid_match.group(1)}-{humid_match.group(2)}%"
                
                elif 'Probability of Significant Rain will be' in line:
                    forecast['rain_probability'] = line.split('will be')[-1].strip()
                
                elif re.match(r'^[A-Za-z]+ force \d+', line):
                    forecast['wind'] = line
                
                # 最后的天气预报描述
                elif not any(keyword in line for keyword in [
                    'Temperature', 'Humidity', 'Probability', 'force'
                ]):
                    forecast['forecast'] = line
            return forecast
        
        except (IndexError, AttributeError, AssertionError) as e:
            raise ValueError(f"Failed to parse forecast text: {str(e)}") from e


    def get_ninth_day_forecast(self):
        self.d(scrollable=True).scroll.toEnd(max_swipes=10)
        
        info = self.d.xpath("//android.widget.ListView/*[last()]").info['contentDescription']
        print(f"The 9th day info: {info}")
        return self.parse_weather_forecast(info)
        #22 June
        # Sunday

        # Temperature will range between 28 and 32 degree Celsius
        # Relative Humidity will range between 65 and 90 percent
        # Probability of Significant Rain will be Low
        # South force 3 to 4.
        # Hot with sunny periods and one or two showers.
