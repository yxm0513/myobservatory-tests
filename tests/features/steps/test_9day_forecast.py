from pytest_bdd import given, when, then, scenario
from pages.nine_day_forecast import NineDayForecastPage
import allure
from io import BytesIO

driver = NineDayForecastPage()
@scenario('../features/9day_forecast.feature', 'Verify 9th day forecast is displayed')
def test_9day_forecast():
    pass

@given("the MyObservatory app is launched")
def launch_app():
    driver.open_9day_forecast()

@when("I navigate to the 9-Day Forecast screen")
def navigate_to_forecast():
    driver.open_9day_forecast()

@then("I should see the weather forecast for the 9th day")
def verify_9th_day_forecast():
    forecast = driver.get_ninth_day_forecast()
    
    with allure.step("Verify 9th day forecast data"):
        assert forecast['date'], "Date is not displayed"
        assert forecast['forecast'], "Weather forecast is not displayed"
        assert forecast['temp_range'], "Temperature range is not displayed"
        assert forecast['humidity'], "Humidity is not displayed"
    
    pil_img = driver.d.screenshot(format='pillow')  # 确保返回PIL对象

    # 转换为bytes
    img_bytes = BytesIO()
    pil_img.save(img_bytes, format='PNG')  # 保存为PNG格式的bytes
    allure.attach(
        img_bytes.getvalue(),
        name="9day_forecast_screenshot",
        attachment_type=allure.attachment_type.PNG
    )
