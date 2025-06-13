import os
from datetime import datetime
import logging
from typing import Optional
import uiautomator2 as u2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def take_screenshot(driver: u2.Device, test_name: str, screenshot_dir: str = "screenshots") -> Optional[str]:
    """
    Takes a screenshot and saves it to the specified directory
    
    Args:
        driver: uiautomator2 device instance
        test_name: Name of the test for filename
        screenshot_dir: Directory to save screenshots
    
    Returns:
        Path to the saved screenshot or None if failed
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # Generate timestamp and filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_test_name = "".join(
            c if c.isalnum() else "_" for c in test_name
        )[:50]  # Limit filename length
        filename = f"{safe_test_name}_{timestamp}.png"
        filepath = os.path.join(screenshot_dir, filename)
        
        # Take screenshot
        driver.screenshot(filepath)
        
        logger.info(f"Screenshot saved to: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Failed to take screenshot: {str(e)}")
        return None


def create_allure_environment_file(env_vars: dict, filepath: str = "allure-results/environment.properties"):
    """
    Creates environment.properties file for Allure report
    
    Args:
        env_vars: Dictionary of environment variables to include
        filepath: Path to save the environment file
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
    except Exception as e:
        logger.error(f"Failed to create Allure environment file: {str(e)}")
