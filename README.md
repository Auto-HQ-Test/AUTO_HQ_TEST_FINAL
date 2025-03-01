# AutoHQTest 사용 설명서
AutoHQTEST는 파수 홈페이지의 종단 테스트를 자동화하고, 테스트 관리를 편리하게 돕는 지원 프로그램입니다. 
Microsoft Playwright와 pytest, PyQt5 라이브러리에 기반하여 작성되었습니다. 

**함수(function)**: AutoHQTest에서 실행 테스트의 가장 기본적인 단위입니다. 파이썬 함수로 구현됩니다. 
**모듈(module)**: 함수의 집합입니다. 
예시를 들자면, "수신 거부 페이지 테스트" 모듈에 포함된 함수는 "국문 홈페이지 수신 거부" 함수와 "영문 홈페이지 수신 거부" 함수로, 총 2개의 함수로 이루어진 모듈입니다. 
이중 최소 1개가 실패할 경우, 해당 모듈 전체가 실패했다고 간주됩니다.

테스트가 실패할 경우 테스트 재실행을 권하며 재실행해도 문제가 반복되는 경우, 육안으로 점검하여 실제 문제가 있는지 확인 후, 테스트 코드를 수정하는 것을 권합니다. 

### 1. 설치
https://github.com/Auto-HQ-Test/AUTO_HQ_TEST_FINAL/releases/tag/test 에서 최신 릴리즈의 autohqtest.bat을 다운받습니다. 

### 2. 테스트 실행하기
autohqtest.bat 파일은 프로그램 인스톨러이자, 테스트 실행 파일의 역할을 겸합니다. 
사용자의 컴퓨터에 GIT과 Python이 깔려 있지 않다면 자동으로 이 둘을 같이 설치합니다. 
만약 컴퓨터에 파이썬 구버전이 있다면, 구버전을 기반으로 동작하려다 작동 않는 문제가 있으므로,
가능하다면 설치된 파이썬을 3.11로 업데이트하거나, 혹은 아예 삭제하고 autohqtest.bat 파일이 직접 설치하게 해주세요. 

autohqtest.bat 파일은 실행할 때마다 최신 코드 파일을 다운로드합니다.

기본 설치 경로는: C:\Users\<PC 사용자 이름>\auto_hqtest 입니다. 
Ex. C:\Users\GS\auto_hqtest

autohqtest.bat 파일로 테스트 프로그램을 실행합니다.

### 2-1. 테스트 옵션 설정
테스트 프로그램이 시작되면, **Test Configuration Manager** 창이 나타납니다.

**Module Settings** 탭에서 각 모듈 별로 설정을 조정할 수 있습니다.
1. **Run**: 실행 여부를 조정합니다. 비활성화하면 해당 모듈은 테스트에서 제외됩니다.
2. **Submit**: 문의 기능 등, 실제 인사처에 문의를 보내는 내용일 때 "실제 문의를 접수하는지" 여부를 체크합니다. 비활성화하면 해당 모듈은 정상적인 문의 과정에서 실제 전송 버튼을 누르는 마지막 액션을 제외하고 테스트합니다. 
3. **Headless**: 브라우저 종단 테스트에서 실제 화면에 브라우저를 표시할지 혹은 보이지 않게 실행할지 결정합니다. 활성화된 상태에서 브라우저가 보이지 않게 실행합니다.
4. **Log**: 현재 종단 테스트에 대한 기록용 로그 파일을 생성할지 결정합니다. 로그는 /logs 폴더에 자동으로 생성됩니다.

**Basic Settings** 탭에서 종단 테스트 전체에 부여되는 세팅을 조정할 수 있습니다. 
1. **Enable Email Notification**: 자동으로 등록한 수신자 이메일로 테스트 결과를 발송합니다. 이 기능을 사용하려면 **Sender Email**, **Recipient Email**, **Sender Passkey** 항목에 적합한 값이 등록되어야 합니다. 
2. **Sender Email**: 발송자 이메일
3. **Recipient Email**: 수신자 이메일
4. **Sender Passkey**: 발송자 이메일의 Google App Password가 필요합니다. (참고 링크: https://support.google.com/accounts/answer/185833?hl=en)
[참고] Sender Email의 경우 Gmail을 사용하는 것을 추천합니다. 
5. **Executable Path**: Playwright가 Chromium Executable 경로를 인식하지 못했을 때 자동으로 참조되는 주소입니다. 현재 컴퓨터에서 playwright 폴더 내의 headless_shell.exe에 달하는 절대 경로를 입력하면 됩니다. 당장 오류가 발생하지 않는다면 기본 값을 유지해 주세요.
6. **Browser Type**: 어떤 브라우저로 테스트할지 결정합니다. 현재 기준(v1.0.0) Chromium 밖에 지원하지 않습니다.
7. **Width**: Headless하지 않게 테스트를 할 경우, 화면에 표시되는 브라우저 창의 가로폭을 결정합니다.
8. **Height**: Headless하지 않게 테스트를 할 경우, 화면에 표시되는 브라우저 창의 세로폭을 결정합니다.
9. **Slow Motion**: 각 모듈 테스트시 슬로우모션 효과를 넣습니다. 기본적으로 0으로 하되, 만약 Headless 옵션을 끄고 직접 테스트를 육안으로 관찰한다면 상황에 따라 1000~2000 정도의 수치를 부여하면 관찰하는데 도움이 됩니다.
10. **Timeout Threshold**: n 밀리초 이상 반응이 없으면 해당 모듈이 실패한 것으로 간주합니다. 기본값은 10초(10000)이며, 상황에 따라 조정할 수 있으나 네트워크 상황에 따라 웹사이트 로딩 속도가 달라지므로, 10000~20000 사이의 수치를 권장합니다.
[번외]
12. **Test Email**: 웹사이트에서 접수 기능을 테스트시 접수자의 메일에 자동으로 넣는 값입니다(2025 3.2 기준 작동하지 않는 기능이나 종단 테스트에 영향을 주지 않습니다.)
13. **Test Phone**: 웹사이트에서 접수 기능을 테스트시 접수자의 핸드폰 번호에 자동으로 넣는 값입니다(2025 3.2 기준 작동하지 않는 기능이나 종단 테스트에 영향을 주지 않습니다.)

설정을 마무리했으면 화면 하단에 **Save and Run** 버튼을 클릭합니다. 

### 2-2. 테스트 결과 확인
테스트가 완료되면 **Test Configuration Manager** 창 하단에 결과가 나타납니다. <br>
예시: <br>
금일 홈페이지 (03/02)점검입니다 <br>
1.문의하기 테스트 - 이상 없음 <br> 
2.마이크로사이트 테스트 - 이상 없음 <br>
3.수신 거부 페이지 테스트 - 이상 없음 <br>
4.신규 문의하기 랜딩 페이지 - 이상 없음 <br>

### 2-3. 로그 파일 확인
hqtest의 설치 경로에서 logs 파일 안에 자동으로 모든 모듈, 모든 함수 별로 테스트 로그가 저장됩니다 (log 옵션을 활성화했다면). 


### 4. 테스트를 추가, 편집하고 싶은 경우
/tests 폴더 내에 각 모듈 파일이 있습니다. 1 모듈 = 1 .py파일과 대응됩니다. pytest를 통해 인식하므로, .py파일 이름에는 'test_' prefix가 포함되어 있어야 합니다.
기본적인 모듈 파일의 구조는 /docs/new_test_template의 예시 파일과 그 주석을 참고하십시오. 


### 5. 옵션을 추가, 삭제하고 싶은 경우
새로운 옵션을 생성하기 위해서는 기본적으로 config.json에 원하는 옵션의 key, value pair를 작성하고, conftest.py 파일의 settings 함수를 함께 수정해야 합니다.
Module Setting의 경우, Boolean value만 가능하며, 추가적으로 settings를 수정할 필요가 없지만, 만약 Basic Settings를 추가한다면 settings에서 pytest.<varname>에 새롭게 할당해야 테스트 내에서 해당 옵션을 참조할 수 있습니다.
환경설정 값이 테스트 내에서 적용되는 프로세스에 관여하는 대표적인 파일들은 **config.json**, **conftest.py**, **option_loader.py**가 있습니다.


### Known bugs:
Playwright가 브라우저 테스트에 필요한 chromium executable 파일을 찾지 못하는 경우 (오류: playwright._impl._errors.Error: BrowserType.launch: Executable doesn't exist at C:\users...)
이 경우 autohqtest.bat 파일을 재실행해보시고, 안된다면 cmd에서 다음 명령어를 순차적으로 입력합니다.

```python
cd C:\Users\{{사용자 이름}}>\auto_hqtest\autohqtest_venv\Scripts
activate
# (파이썬 가상환경에 들어와서 (autohqtest_venv)가 보이면)
playwright install
```
명령어를 실행했는데도 문제가 지속되면 **Test Configuration Manager** 의 Basic Settings에서 옵션 **Executable Path** 에 등재된 경로에 실제로 headless_shell.exe 파일이 있는지 확인하고 경로가 잘못되었다면 headless_shell.exe가 있는 경로로 업데이트해주세요. 


### 참고:
작동되지 않는 테스트를 확인하거나, 새로운 테스트를 작성할 때 playwright Inspector를 사용하면 큰 도움이 됩니다.

autohqtest_venv 가상환경 내에서 

```python
set PWDEBUG=1
pytest .tests\test_cancelSubscription.py -s
```
test_cancelSubscription.py 모듈을 Playwright Inspector 내에서 실행할 수 있습니다.

더 자세한 내용은 공식 문서를 참조해주세요. 

https://playwright.dev/python/docs/debug
