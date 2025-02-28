import pytest
import asyncio
import random
from pathlib import Path
from playwright.async_api import async_playwright, expect
from utils.loggers import function_logging, module_logging

#####
### 구현 완료
#####

@function_logging
async def home_contactUs_KR(settings, test_logger):
        url = "https://www.fasoo.com/?lang=kr"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기

        async with async_playwright() as p:
            if pytest.browser_type == "chromium":
                try:
                    browser = await p.chromium.launch(
                        headless=settings.get_module_options(current_module)['headless'],
                        slow_mo=pytest.slow_mo
                    )
                except:
                    browser = await p.chromium.launch(
                        executable_path=pytest.executable_path,
                        headless=settings.get_module_options(current_module)['headless'],
                        slow_mo=pytest.slow_mo
                    )
            context = await browser.new_context(
                viewport={'width': pytest.width, 'height': pytest.height},
            )
            context.set_default_timeout(pytest.timeout_threshold)
            page = await context.new_page()
            await page.goto(url)
            await page.wait_for_load_state("networkidle")

            # 상단 배너에서 회사소개 > 문의하기로 문의 페이지 접근
            link = page.get_by_label("회사소개").get_by_role("link", name="회사소개")
            await link.hover()
            support = page.locator("#jet-mega-menu-item-613").get_by_role("link", name="문의하기")
            await expect(support).to_be_visible()
            await support.click()
            await page.wait_for_url("https://www.fasoo.com/contact-us")

            # 문의하기 내용 입력
            await page.get_by_placeholder("성명*").click()
            await page.get_by_placeholder("성명*").fill("hqtest")

            await page.get_by_placeholder("회사*").click()
            await page.get_by_placeholder("회사*").fill("hqtest")

            await page.get_by_placeholder("부서*").click()
            await page.get_by_placeholder("부서*").fill("hqtest")

            await page.get_by_placeholder("직급*").click()
            await page.get_by_placeholder("직급*").fill("hqtest")

            await page.get_by_placeholder("연락처*").click()
            await page.get_by_placeholder("연락처*").fill("01022222222")

            await page.get_by_placeholder("이메일*").click()
            await page.get_by_placeholder("이메일*").fill("nately@fasoo.com")

            # 랜덤 카테고리 선택
            categories = {0: "제품 문의", 
                        1:"클라우드 서비스 및 컨설팅 문의", 
                        2:"홍보 및 마케팅 문의", 
                        3:"채용 문의"}
            await page.get_by_label(categories[random.randint(0, 3)]).click()
            await page.get_by_label("채용 문의").check()

            # 문의 내용
            await page.get_by_label("문의 내용(유저수, 문의 제품 등을 포함해서 작성해 주시면 더욱 신속하게 상담이 진행됩니다.)*").click()
            await page.get_by_label("문의 내용(유저수, 문의 제품 등을 포함해서 작성해 주시면 더욱 신속하게 상담이 진행됩니다.)*").fill("hqtest")

            # 경로 선택
            paths = {0: "온/오프라인 행사",
                    1:"SNS(블로그/인스타그램/페이스북/유튜브)", 
                    2:"보도자료/기사", 
                    3:"Fasoo 뉴스레터", 
                    4:"광고", 5:"Fasoo 프로모션 (eDM)", 
                    6:"지인 소개", 7:""}
            path_idx = random.randint(0, 7)
            path_idx = 6
            path_text = paths[path_idx]
            
            await page.get_by_label(paths[path_idx], exact=True).check()
            if path_idx == 6:
                await page.locator("label").filter(has_text=path_text).get_by_role("textbox").click()
                await page.locator("label").filter(has_text=path_text).get_by_role("textbox").fill("hqtest")
            if path_idx == 7:
                await page.locator(".etc-text").click()
                await page.locator(".etc-text").fill("hqtest")
            await page.get_by_label("개인정보 수집 및 이용에 대해서 동의합니다").check()
            
            if settings.get_module_options(current_module)['submit']:
                await page.get_by_role("button", name="보내기").click()

    
@function_logging
async def home_contactUs_EN(settings, test_logger):
        url = "https://en.fasoo.com/"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
        
        async with async_playwright() as p:
            if pytest.browser_type == "chromium":
                try:
                    browser = await p.chromium.launch(
                        headless=settings.get_module_options(current_module)['headless'],
                        slow_mo=pytest.slow_mo
                    )
                except:
                    browser = await p.chromium.launch(
                        executable_path=pytest.executable_path,
                        headless=settings.get_module_options(current_module)['headless'],
                        slow_mo=pytest.slow_mo
                    )
            context = await browser.new_context(
                viewport={'width': pytest.width, 'height': pytest.height},
            )
            context.set_default_timeout(pytest.timeout_threshold)
            page = await context.new_page()
            await page.goto(url)
            await page.wait_for_load_state("networkidle")

            # 상단 배너에서 Company > Contact Us 로 접근
            banner_link = page.get_by_role("banner").get_by_role("link", name="Company")
            await banner_link.hover()
            link = page.get_by_role("banner").get_by_role("link", name="Contact Us")
            await expect(link).to_be_visible()
            await link.click()
            await page.wait_for_url("https://en.fasoo.com/about-us/contact-us")

            await page.locator("iframe[title=\"Form 0\"]").content_frame.get_by_placeholder("First Name *").click()
            await page.locator("iframe[title=\"Form 0\"]").content_frame.get_by_placeholder("First Name *").fill("hqtest")
            
            await page.locator("iframe[title=\"Form 0\"]").content_frame.get_by_placeholder("Last Name *").click()
            await page.locator("iframe[title=\"Form 0\"]").content_frame.get_by_placeholder("Last Name *").fill("hqtest")
            
            await page.locator("iframe[title=\"Form 0\"]").content_frame.get_by_placeholder("Business Email *").click()
            await page.locator("iframe[title=\"Form 0\"]").content_frame.get_by_placeholder("Business Email *").fill("hqtest@fasoo.com")

            await page.locator("iframe[title=\"Form 0\"]").content_frame.get_by_placeholder("Telephone Number *").click()
            await page.locator("iframe[title=\"Form 0\"]").content_frame.get_by_placeholder("Telephone Number *").fill("01022222222")
            
            await page.locator("iframe[title=\"Form 0\"]").content_frame.get_by_placeholder("Company *").click()
            await page.locator("iframe[title=\"Form 0\"]").content_frame.get_by_placeholder("Company *").fill("hqtest@gmail.com")
            
            await page.locator("iframe[title=\"Form 0\"]").content_frame.get_by_label("I would like to*").click()
            rdm = {0:"Request a Demo", 1:"Become a Partner", 2:"Make a General Inquiry"}
            await page.locator("iframe[title=\"Form 0\"]").content_frame.get_by_label("I would like to*").select_option(rdm[random.randint(0, 2)])

            await page.locator("iframe[title=\"Form 0\"]").content_frame.get_by_placeholder("Message *").click()
            await page.locator("iframe[title=\"Form 0\"]").content_frame.get_by_placeholder("Message *").fill("hqtest")

            if settings.get_module_options(current_module)['submit']:
                await page.get_by_role("button", name="submit").click()


@module_logging
@pytest.mark.asyncio
async def test_home_contactUs(settings, test_logger):
    """
    """
    current_module = Path(__file__).name # Get current module name
    # Check if module should run
    if not settings.should_run_module(current_module):
        pytest.skip("Module disabled in configuration")
    
    await home_contactUs_KR(settings, test_logger)
    await home_contactUs_EN(settings, test_logger)
        
