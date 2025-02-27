import pytest
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, expect
from utils.loggers import function_logging, module_logging


@function_logging
async def function_component_1(settings, test_logger):
    await asyncio.sleep(1)
    assert True

    
@function_logging
async def function_component_2(settings, test_logger):
    await asyncio.sleep(1)
    assert True

@module_logging
@pytest.mark.asyncio
async def test_main(settings, test_logger):
    """
    """
    current_module = Path(__file__).name # Get current module name
    # Check if module should run
    if not settings.should_run_module(current_module):
        pytest.skip("Module disabled in configuration")
    await function_component_1(settings, test_logger)
    await function_component_2(settings, test_logger)
