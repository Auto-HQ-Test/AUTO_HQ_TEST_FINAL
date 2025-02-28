import pytest
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, expect
from utils.loggers import function_logging, module_logging

#####
## 구현 완료
#####

@function_logging
async def wrapsody_contactUs_KR(settings, test_logger):

        url = "https://www.wrapsody.com/kr/"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
        browser_type = "chromium"
        width = 1920
        height = 1080
        accept_download = True
        
        async with async_playwright() as p:
            if browser_type == "chromium":
                browser = await p.chromium.launch(
                    # executable_path="C:/Users/GS/AppData/Local/ms-playwright/chromium_headless_shell-1155/chrome-win/headless_shell.exe",
                    headless=settings.get_module_options(current_module)['headless'],
                )
                context = await browser.new_context(
                    viewport={'width': width, 'height': height},
                    accept_downloads=accept_download,
                )
                context.set_default_timeout(20000)
                page = await context.new_page()
                await page.goto(url)
                await expect(page.get_by_role("link", name="문의하기")).to_be_visible()
                await page.get_by_role("link", name="문의하기").click()
                await page.get_by_placeholder("성명을 입력해주세요").click()
                await page.get_by_placeholder("성명을 입력해주세요").fill("hqtest")
                await page.get_by_placeholder("성명을 입력해주세요").press("Tab")
                await page.get_by_placeholder("회사를 입력해주세요").fill("hqtest")
                await page.get_by_placeholder("회사를 입력해주세요").press("Tab")
                await page.get_by_placeholder("부서 / 직급을 입력해주세요").fill("hqtest / hqtest")
                await page.get_by_placeholder("부서 / 직급을 입력해주세요").press("Tab")
                await page.get_by_placeholder("예) fasoo@fasoo.com").fill("hqtest@fasoo.com")
                await page.get_by_placeholder("예) fasoo@fasoo.com").press("Tab")
                await page.get_by_placeholder("연락처를 입력해주세요").fill("01022222222")
                await page.get_by_label("회사규모").select_option(" 500 - 1999")
                await page.get_by_label("질문 / 요청").click()
                await page.get_by_text("Fasoo 뉴스레터").click()
                await page.get_by_label("이용약관 및 개인정보처리방침 에 동의합니다").check()
                
                if settings.get_module_options(current_module)['submit']:
                    await page.get_by_role("button", name="제출하기").click()
                
    
@function_logging
async def wrapsody_contactUs_EN(settings, test_logger):
    
        url = "https://www.wrapsody.com/en/"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
        browser_type = "chromium"
        width = 1920
        height = 1080
        accept_download = True
        async with async_playwright() as p:
            if browser_type == "chromium":
                browser = await p.chromium.launch(
                    # executable_path="C:/Users/GS/AppData/Local/ms-playwright/chromium_headless_shell-1155/chrome-win/headless_shell.exe",
                    headless=settings.get_module_options(current_module)['headless'],
                )
                context = await browser.new_context(
                    viewport={'width': width, 'height': height},
                    accept_downloads=accept_download,
                )
                context.set_default_timeout(20000)
                page = await context.new_page()
                await page.goto(url)
                await expect(page.get_by_role("link", name="Contact Us").first).to_be_visible()
                await page.get_by_role("link", name="Contact Us").first.click()
                await page.get_by_label("First Name").click()
                await page.get_by_label("First Name").fill("hqtest")
                await page.get_by_label("Last Name").click()
                await page.get_by_label("Last Name").fill("hqtest")
                await page.get_by_label("Company Name").click()
                await page.get_by_label("Company Name").fill("hqtest")
                await page.get_by_label("Business Email").click()
                await page.get_by_label("Business Email").fill("hqtest@fasoo.com")
                await page.get_by_label("Business Email").press("Tab")
                await page.get_by_label("Country").click()
                await page.get_by_label("Country").fill("hqtest")
                await page.get_by_text("Company Size Select 1 - 49 50").click()
                await page.get_by_label("Company Size").select_option(" 2000+")
                await page.get_by_label("Questions / Requests").click()
                await page.get_by_label("Questions / Requests").fill("h")
                await page.get_by_text("I agree to the Terms of").click()
                
                if settings.get_module_options(current_module)['submit']:
                    await page.get_by_role("button", name="Send").click()
  

@function_logging
async def wrapsodyECO_contactUs_KR(settings, test_logger):
        url = "https://www.wrapsodyeco.com/kr/"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
        browser_type = "chromium"
        width = 1920
        height = 1080
        accept_download = True
        async with async_playwright() as p:
            if browser_type == "chromium":
                browser = await p.chromium.launch(
                    # executable_path="C:/Users/GS/AppData/Local/ms-playwright/chromium_headless_shell-1155/chrome-win/headless_shell.exe",
                    headless=settings.get_module_options(current_module)['headless'],
                )
                context = await browser.new_context(
                    viewport={'width': width, 'height': height},
                    accept_downloads=accept_download,
                )
                context.set_default_timeout(20000)
                page = await context.new_page()
                await page.goto(url)
                await expect(page.get_by_role("banner").get_by_role("link", name="문의하기")).to_be_visible()
                await page.get_by_role("banner").get_by_role("link", name="문의하기").click()
                await page.get_by_label("성명").click()
                await page.get_by_label("성명").fill("hqtest")
                await page.get_by_label("회사", exact=True).click()
                await page.get_by_label("회사", exact=True).fill("hqtest")
                await page.get_by_label("부서 / 직급").click()
                await page.get_by_label("부서 / 직급").click()
                await page.get_by_label("부서 / 직급").fill("hqtest / hqtest")
                await page.get_by_label("이메일").click()
                await page.get_by_label("이메일").fill("hqtest@fasoo.com")
                await page.get_by_label("연락처").click()
                await page.get_by_label("연락처").fill("01022222222")
                await page.get_by_label("연락처").press("Tab")
                await page.get_by_label("회사규모").select_option(" 500 - 1999")
                await page.get_by_label("메시지").click()
                await page.get_by_label("메시지").fill("hqtest")
                await page.get_by_label("Fasoo 프로모션 (eDM)").check()
                await page.get_by_label("Fasoo 뉴스레터").check()
                await page.get_by_label("이용약관 및 개인정보처리방침 에 동의합니다").check()

                if settings.get_module_options(current_module)['submit']:
                    await page.get_by_role("button", name="제출하기").click()
                    await expect(page.get_by_role("heading", name="문의가 접수 되었습니다")).to_be_visible()
                    await page.get_by_role("link", name="확인").click()
                

@function_logging
async def wrapsodyECO_contactUs_EN(settings, test_logger):

        url = "https://www.wrapsodyeco.com/en/"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
        browser_type = "chromium"
        width = 1920
        height = 1080
        accept_download = True
        async with async_playwright() as p:
            if browser_type == "chromium":
                browser = await p.chromium.launch(
                    # executable_path="C:/Users/GS/AppData/Local/ms-playwright/chromium_headless_shell-1155/chrome-win/headless_shell.exe",
                    headless=settings.get_module_options(current_module)['headless'],
                )
                context = await browser.new_context(
                    viewport={'width': width, 'height': height},
                    accept_downloads=accept_download,
                )
                context.set_default_timeout(20000)
                page = await context.new_page()
                await page.goto(url)
                await page.get_by_role("banner").get_by_role("link", name="Contact Us").click()
                await page.get_by_placeholder("Please enter your name").click()
                await page.get_by_placeholder("Please enter your name").fill("hqtest")
                await page.get_by_placeholder("Ex) fasoo@fasoo.com").click()
                await page.get_by_placeholder("Ex) fasoo@fasoo.com").fill("hqtest@fasoo.com")
                await page.get_by_placeholder("Please enter your company name").click()
                await page.get_by_placeholder("Please enter your company name").fill("hqtest")
                await page.get_by_label("Company Size").select_option(" 500")
                await page.get_by_label("Questions / Requests").click()
                await page.get_by_label("Questions / Requests").fill("hqtest")
                await page.get_by_text("I agree to the Terms of").click()

                if settings.get_module_options(current_module)['submit']:
                    await page.get_by_role("button", name="Submit").click()
                    await page.get_by_role("link", name="Confirm").click()
                
   

"""@module_logging
async def digitalPage_contactUs_KR(settings, test_logger):
 
        url = "https://home.digitalpage.me/kr/"
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
                await page.get_by_role("link", name="Support").click()
                await page.get_by_role("link", name="이메일 상담").click()
                await page.get_by_placeholder("이메일").click()
                await page.get_by_placeholder("이메일").fill("hqtest@fasoo.com")
                await page.get_by_placeholder("이메일").press("Tab")
                await page.get_by_placeholder("제목을 입력해 주세요.(30자 이내)").fill("hqtest")
                await page.get_by_placeholder("제목을 입력해 주세요.(30자 이내)").press("Tab")
                await page.get_by_placeholder("내용을 입력해주세요.(3000자 이내)").fill("hqtest")
                await page.get_by_placeholder("내용을 입력해주세요.(3000자 이내)").press("Tab")
                await page.get_by_text("이메일 수집에 동의합니다").click()
                
                if settings.get_module_options(current_module)['submit']:
                    await page.get_by_role("button", name="보내기").click()
                    await page.get_by_role("link", name="확인").click()

                

@module_logging
async def digitalPage_contactUs_EN(settings, test_logger):

        url = "https://home.digitalpage.me/en/"
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
                page.get_by_role("link", name="Support").click()
                page.get_by_role("link", name="Inquiry/Support").click()
                page.get_by_placeholder("Enter email here.").click()
                page.get_by_placeholder("Enter email here.").fill("hqtest@fasoo.com")
                page.get_by_placeholder("Enter email here.").press("Tab")
                page.get_by_placeholder("Enter title here.").fill("hqtest")
                page.get_by_placeholder("Enter title here.").press("Tab")
                page.get_by_placeholder("Enter content here.").fill("hqtest")
                page.get_by_text("I agree to the collection of").click()
                
                if settings.get_module_options(current_module)['submit']:
                    await page.get_by_role("button", name="Submit").click()
                    await page.get_by_role("link", name="Confirm").click()"""

   

@function_logging
async def mindSAT_contactUs_KR(settings, test_logger):
        url = "https://mind-sat.com/kr/"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
        browser_type = "chromium"
        width = 1920
        height = 1080
        accept_download = True
 
        async with async_playwright() as p:
            if browser_type == "chromium":
                browser = await p.chromium.launch(
                    # executable_path="C:/Users/GS/AppData/Local/ms-playwright/chromium_headless_shell-1155/chrome-win/headless_shell.exe",
                    headless=settings.get_module_options(current_module)['headless'],
                )
                context = await browser.new_context(
                    viewport={'width': width, 'height': height},
                    accept_downloads=accept_download,
                )
                context.set_default_timeout(20000)
                page = await context.new_page()
                await page.goto("https://mind-sat.com/kr/")
                await page.get_by_role("link", name="서비스 문의").first.click()
                await page.get_by_placeholder("성명을 입력해주세요").click()
                await page.get_by_placeholder("성명을 입력해주세요").fill("hqtest")
                await page.get_by_placeholder("회사를 입력해주세요").click()
                await page.get_by_placeholder("회사를 입력해주세요").fill("hqtest")
                await page.get_by_placeholder("부서 / 직급을 입력해주세요").click()
                await page.get_by_placeholder("부서 / 직급을 입력해주세요").fill("hqtest")
                await page.get_by_placeholder("ex) fasoo@fasoo.com").click()
                await page.get_by_placeholder("ex) fasoo@fasoo.com").fill("hqtest@fasoo.com")
                await page.get_by_placeholder("연락처를 입력해주세요").click()
                await page.get_by_placeholder("연락처를 입력해주세요").fill("01022222222")
                await page.get_by_label("회사규모").select_option(" 500 - 1999")
                await page.get_by_label("질문 / 요청").click()
                await page.get_by_label("질문 / 요청").fill("hqtest")
                await page.get_by_label("온/오프라인 행사").check()
                await page.get_by_label("Fasoo 프로모션 (eDM)").check()
                await page.get_by_label("개인정보처리방침 에 동의합니다").check()

                if settings.get_module_options(current_module)['submit']:
                    await page.get_by_role("button", name="보내기").click()
                    await page.get_by_role("link", name="확인").click()
                
   

@function_logging
async def mindSAT_contactUs_EN(settings, test_logger):
        url = "https://mind-sat.com/en/"
        current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
        browser_type = "chromium"
        width = 1920
        height = 1080
        accept_download = True
    
        async with async_playwright() as p:
            if browser_type == "chromium":
                browser = await p.chromium.launch(
                    # executable_path="C:/Users/GS/AppData/Local/ms-playwright/chromium_headless_shell-1155/chrome-win/headless_shell.exe",
                    headless=settings.get_module_options(current_module)['headless'],
                )
                context = await browser.new_context(
                    viewport={'width': width, 'height': height},
                    accept_downloads=accept_download,
                )
                context.set_default_timeout(20000)
                page = await context.new_page()
                await page.goto("https://mind-sat.com/en/")
                await page.get_by_role("link", name="Inquiry").click()
                await page.get_by_placeholder("Please enter your name").click()
                await page.get_by_placeholder("Please enter your name").fill("hqtest")
                await page.get_by_placeholder("ex) fasoo@fasoo.com").click()
                await page.get_by_placeholder("ex) fasoo@fasoo.com").fill("hqtest@fasoo.com")
                await page.get_by_placeholder("Please enter your company name").click()
                await page.get_by_placeholder("Please enter your company name").fill("hqtest")
                await page.get_by_label("Company Size").select_option(" 1")
                await page.get_by_label("Questions / Requests").click()
                await page.get_by_label("Questions / Requests").fill("hqtest")
                await page.get_by_text("I agree to the collection of").click()

                if settings.get_module_options(current_module)['submit']:
                    await page.get_by_role("button", name="Submit").click()
                    await page.get_by_role("link", name="Confirm").click()
               
    

"""@module_logging        
async def mktscreen_contactUs_KR(settings, test_logger):
        url = "https://mkt.fasoo.com/screen/"
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
                await page.get_by_role("button", name="바로 문의하기").click()
                await page.get_by_placeholder("이름*").click()
                await page.get_by_placeholder("이름*").fill("hqtest")
                await page.get_by_placeholder("이메일*").click()
                await page.get_by_placeholder("이메일*").fill("hqtest@fasoo.com")
                await page.get_by_placeholder("연락처*").click()
                await page.get_by_placeholder("연락처*").fill("01022222222")
                await page.get_by_placeholder("회사/소속*").click()
                await page.get_by_placeholder("회사/소속*").fill("hqtest / hqtest")
                await page.locator("#form-field-request_msg").select_option("재택 근무 시 VPN, VDI 화면 보안")

                if settings.get_module_options(current_module)['submit']:
                    await page.get_by_role("button", name="Submit").click()
                    await page.get_by_role("button", name="확인").click()
                
 

@module_logging
async def mktdid_contactUs_KR(settings, test_logger):
        url = "https://mkt.fasoo.com/did/"
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
                await page.get_by_role("button", name="바로 문의하기").click()
                await page.get_by_placeholder("이름*").click()
                await page.get_by_placeholder("이름*").fill("hqtest")
                await page.get_by_placeholder("이메일*").click()
                await page.get_by_placeholder("이메일*").fill("fasoo@hqtest")
                await page.get_by_placeholder("이메일*").click()
                await page.get_by_placeholder("이메일*").fill("hqtest@fasoo.com")
                await page.get_by_placeholder("연락처*").click()
                await page.get_by_placeholder("연락처*").fill("01022222222")
                await page.get_by_placeholder("회사/소속*").click()
                await page.get_by_placeholder("회사/소속*").fill("hqtest/hqtest")
                await page.locator("#form-field-request_msg").select_option("내부 데이터 활용 컴플라이언스")

                if settings.get_module_options(current_module)['submit']:
                    await page.get_by_role("button", name="Submit").click()
                    await page.get_by_role("button", name="확인").click()
                
  

@module_logging
async def mktcad_contactUs_KR(settings, test_logger):
        url = "https://mkt.fasoo.com/cad/"
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
                await page.get_by_role("button", name="바로 문의하기").click()
                await page.get_by_placeholder("이름*").click()
                await page.get_by_placeholder("이름*").fill("hqtest")
                await page.get_by_placeholder("이메일*").click()
                await page.get_by_placeholder("이메일*").fill("hqtest@fasoo.com")
                await page.get_by_placeholder("연락처*").click()
                await page.get_by_placeholder("연락처*").fill("01022222222")
                await page.get_by_placeholder("회사/소속*").click()
                await page.get_by_placeholder("회사/소속*").fill("hqtest/hqtest")
                await page.locator("#form-field-request_msg").select_option("도면 보안")

                if settings.get_module_options(current_module)['submit']:
                    await page.get_by_role("button", name="Submit").click()
                    await page.get_by_role("button", name="확인").click()
"""

@module_logging
@pytest.mark.asyncio
async def test_home_contactUs(settings, test_logger):
    """
    """
    current_module = Path(__file__).name # Get current module name
    # Check if module should run
    if not settings.should_run_module(current_module):
        pytest.skip("Module disabled in configuration")
    
    await wrapsody_contactUs_KR(settings, test_logger)
    await wrapsody_contactUs_EN(settings, test_logger)

    await wrapsodyECO_contactUs_KR(settings, test_logger)
    await wrapsodyECO_contactUs_EN(settings, test_logger)

    await mindSAT_contactUs_KR(settings, test_logger)
    await mindSAT_contactUs_EN(settings, test_logger)

    

    """   await digitalPage_contactUs_KR(settings, test_logger)
    await digitalPage_contactUs_EN(settings, test_logger)

    await mktscreen_contactUs_KR(settings, test_logger)

    await mktdid_contactUs_KR(settings, test_logger)

    await mktcad_contactUs_KR(settings, test_logger)"""