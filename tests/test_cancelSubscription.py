import pytest
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, expect
from utils.loggers import function_logging, module_logging

#####
### 구현 완료
#####

@function_logging
async def cancelSubscription_KR(settings, test_logger):
        url = "https://www.fasoo.com/unsubscribe"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
        browser_type = "chromium"
        width = 1920
        height = 1080
        accept_download = True
    
        async with async_playwright() as p:
            if browser_type == "chromium":
                browser = await p.chromium.launch(
                    executable_path="C:/Users/GS/AppData/Local/ms-playwright/chromium_headless_shell-1155/chrome-win/headless_shell.exe",
                    headless=settings.get_module_options(current_module)['headless'], 
                )
                context = await browser.new_context(
                    viewport={'width': width, 'height': height},
                    accept_downloads=accept_download,
                )
                context.set_default_timeout(20000)
                page = await context.new_page()
                await page.goto(url)
                await expect(page.get_by_text("수신거부 신청 Fasoo")).to_be_visible()
                await page.locator("#form-field-email").click()
                await page.locator("#form-field-email").fill("hqtest@fasoo.com")
                await page.get_by_role("button", name="수신거부 신청").click()


@function_logging
async def cancelSubscription_EN(settings, test_logger):
        url = "https://en.fasoo.com/unsubscribe"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
        browser_type = "chromium"
        width = 1920
        height = 1080
        accept_download = True

        async with async_playwright() as p:
            if browser_type == "chromium":
                browser = await p.chromium.launch(
                    executable_path="C:/Users/GS/AppData/Local/ms-playwright/chromium_headless_shell-1155/chrome-win/headless_shell.exe",
                    headless=settings.get_module_options(current_module)['headless'],    
                )
                context = await browser.new_context(
                    viewport={'width': width, 'height': height},
                    accept_downloads=accept_download,
                )
                context.set_default_timeout(20000)
                page = await context.new_page()
                await page.goto(url)
                await expect(page.get_by_text("Unsubscribe Request This is")).to_be_visible()
                await page.locator("#form-field-amex").click()
                await page.locator("#form-field-amex").fill("hqtest@fasoo.com")
                await page.get_by_role("button", name="Unsubscribe Request​").click()

@module_logging
@pytest.mark.asyncio
async def test_cancelSubscription(settings, test_logger):
    """Test both components"""

    current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
    if not settings.should_run_module(current_module):  # 설정에 따라 모듈 실행 여부 확인
        pytest.skip("Module disabled in configuration")

    
    await cancelSubscription_KR(settings, test_logger)
    await cancelSubscription_EN(settings, test_logger)
    
    