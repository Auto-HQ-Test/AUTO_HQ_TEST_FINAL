from utils.option_loader import OptionLoader
from utils.loggers import DebugLogger, TestLogger
from utils.registry import TestRegistry
import pytest
import time
from pathlib import Path



@pytest.fixture(scope="session")
def settings() -> OptionLoader:
    """Session-level fixture providing access to test settings.
    
    This fixture initializes the OptionLoader which manages test configuration
    settings from configs.json. The configuration is loaded once at the start 
    of the test session and shared across all tests.        
    Raises:
        FileNotFoundError: If configs.json doesn't exist
        json.JSONDecodeError: If configs.json is not valid JSON
    """
    settings = OptionLoader() # Create OptionLoader object. Autoloads the last configs.json

    # Making basic settings to be globally assessible pytest values
    pytest.executable_path = settings.get_basic_setting()["executable_path"]
    pytest.browser_type = settings.get_basic_setting()["browser_type"]
    pytest.width = int(settings.get_basic_setting()["width"])
    pytest.height = int(settings.get_basic_setting()["height"])
    pytest.timeout_threshold = int(settings.get_basic_setting()["timeout_threshold"])
    pytest.slow_mo = int(settings.get_basic_setting()["slow_motion"])
    pytest.test_email = settings.get_basic_setting()["test_email"]
    pytest.test_phone = settings.get_basic_setting()["test_phone"]

    return settings


@pytest.fixture(scope="session")
def test_logger(settings):
    """Session-level fixture providing the test logger instance"""
    basic_settings = settings.get_basic_setting()
    test_logger_instance = TestLogger(basic_settings=basic_settings)
    TestRegistry.set_logger(test_logger_instance)
    # Configure the existing instance instead of creating new one
    test_logger_instance.configure(basic_settings)
    return test_logger_instance

