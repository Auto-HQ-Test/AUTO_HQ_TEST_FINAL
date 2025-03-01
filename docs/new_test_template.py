import pytest
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, expect
from utils.loggers import function_logging, module_logging

"""
가장 기본적인 모듈 파일입니다. function_component_1과 function_component_2, default_fasoo_function, 이렇게 3개의 함수로 이루어진 모듈 파일을 실행하는 상태입니다. 
@function_logging과 @module_logging 데코레이터를 통해 자동으로 각 단위 별로 로그를 기록합니다. 
만약 개발 중 cmd에 뭔가를 print하고 싶은데 print가 되지 않는다면 test_logger.console() 메서드를 사용하세요.

모든 함수에는 기본적으로 settings와 test_logger, 2개의 파라미터를 받습니다. 이것 이외에 주입되는 모든 외부 파라미터 (옵션 등)은 
크게 2가지 경로를 통해 사용할 수 있습니다.

1번: settings 오브젝트를 통한 참조.
2번: pytest global variable을 통한 참조.

1번의 경우, settings은 OptionLoader 객체입니다. config.json을 통째로 읽어들여서 접근할 수 있게 해주는 인터페이스 역할입니다. 
2번의 경우, conftest.py의 settings 함수에서 initialize되는, pytest global runtime에서 참조할 수 있는 변수입니다. 
비록 절대적이지 않으나, 
"개별 모듈마다 별개로 적용되며며, Bool값을 통한 사용자가 켜고 끄는 류의 옵션"은 대체적으로 settings를 통해 참조하고, 
"모든 모듈에서 동일하게 참고하는 str, int등 여러 타입의 값"은 pytest global variable의 형태로 주입하는 것을 권장합니다. 
"""

@function_logging
async def function_component_1(settings, test_logger):
    current_module = Path(__file__).name  # 현재 모듈 이름 가져오기
    if settings.get_module_options(current_module)['headless']: # 현재 모듈의 option 중 headless 항목의 값이 True인 경우
        test_logger.console("I am headless!")
    else:
        test_logger.console("I am not...")
    await asyncio.sleep(1)


@function_logging
async def function_component_2(settings, test_logger):
    await asyncio.sleep(1)
    assert True


@function_logging
async def default_fasoo_function(settings, test_logger):
    url = "https://www.fasoo.com/?lang=kr" # 최초 진입하는 웹 URL을 전달합니다.
    current_module = Path(__file__).name  # 현재 모듈 이름 가져옵니다. 

    async with async_playwright() as p:
        if pytest.browser_type == "chromium": 
            # 아래의 try-except 패턴은 이따금 pytest가 chromium의 executable을 읽지 못하는 버그에 대응하기 위해 존재합니다. 만약 자동으로 executable 경로를 찾지 못하면, basic settings에 등록한 값을 참고하여
            # 재시도합니다.
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
        # 아래부터 테스트 내용을 입력하면 됩니다. 


@module_logging
@pytest.mark.asyncio
async def test_main(settings, test_logger):
    current_module = Path(__file__).name # Get current module name
    # Check if module should run
    if not settings.should_run_module(current_module):
        pytest.skip("Module disabled in configuration")
    await function_component_1(settings, test_logger)
    await function_component_2(settings, test_logger)
    await default_fasoo_function(settings, test_logger)

