import logging
import logging.handlers
import smtplib
import time
import functools
from functools import wraps
from email.message import EmailMessage
from datetime import datetime
import os
from typing import Union, Tuple, List, Callable, Optional
from pathlib import Path
from contextlib import contextmanager
from dataclasses import dataclass
from typing import List, Dict, Any
import json


class DebugLogger:
    """A simple logger that performs console prints for debugging during development.
    Intended to be used as a pytest fixture. 
    [DEPRECATED] This is no longer supported.
    """
    def __init__(self):
        self.logger = logging.getLogger('pytest_debug')
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers: # Only add handler if logger doesn't have handlers yet
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            self.logger.propagate = True # Ensure propagation is enabled
    
    def console(self, message: str):
        """Console print a debug message."""
        self.logger.info(message)

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List

@dataclass
class FunctionResult:
    """Records a single function's execution result"""
    function_name: str
    status: str
    duration: float
    error_message: Optional[str] = None
    screenshot_path: Optional[str] = None

@dataclass
class ModuleLog:
    """Represents a complete module execution including all function results"""
    module_name: str
    start_time: datetime
    settings: Dict[str, Any]
    function_results: List[FunctionResult] = field(default_factory=list)
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    status: str = None

class TestLogger:
    def __init__(self, log_directory: Path = Path('logs'), basic_settings: Dict[str, Any] = None):
        self.log_directory = log_directory
        self.basic_settings = basic_settings
        self.module_logs = {}
        self.session_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._logger = DebugLogger()

        if not os.path.exists(self.log_directory):
            os.mkdir(self.log_directory)

    def configure(self, basic_settings: Dict[str, Any]):
        """Update configuration after initialization"""
        self.basic_settings = basic_settings
    
    @property
    def basic_settings(self):
        return self._basic_settings

    @basic_settings.setter
    def basic_settings(self, value):
        print(f"Debug - basic_settings being set to: {value}")
        self._basic_settings = value
    
    def console(self, message: str):
        """Console print a debug message."""
        self._logger.console(message)
        
    def start_module(self, module_name: str, settings: Dict[str, Any]) -> ModuleLog:
        """Initialize module logging"""
        log = ModuleLog(
            module_name=module_name,
            start_time=datetime.now(),
            settings=settings
        )
        self.module_logs[module_name] = log
        return log
        
    def add_function_result(self, module_name: str, 
                          function_name: str, 
                          status: str,
                          duration: float,
                          error_message: Optional[str] = None,
                          screenshot_path: Optional[str] = None):
        """Add function result to its parent module log"""
        if module_name not in self.module_logs:
            raise ValueError(f"No active log found for module {module_name}")
            
        result = FunctionResult(
            function_name=function_name,
            status=status,
            duration=duration,
            error_message=error_message,
            screenshot_path=screenshot_path
        )
        self.module_logs[module_name].function_results.append(result)
        self._write_logs()  # Update log file after each function
        
    def end_module(self, module_name: str, success: bool):
        """Complete module logging"""
        log = self.module_logs[module_name]
        log.end_time = datetime.now()
        log.duration = (log.end_time - log.start_time).total_seconds()
        log.status = "Success" if success else "Failed"
        self._write_logs()
        
    def _write_logs(self):
        """Write all logs to a single file with hierarchical structure"""
        log_file = self.log_directory / f"{self.session_timestamp}.log"
        with open(log_file, 'w', encoding='utf-8') as f:
            for log in self.module_logs.values():
                f.write(f"Module: {log.module_name}\n")
                f.write(f"Status: {log.status}\n")
                f.write(f"Start Time: {log.start_time}\n")
                if log.end_time:
                    f.write(f"End Time: {log.end_time}\n")
                    f.write(f"Duration: {log.duration:.2f}s\n")
                f.write("Function Execution Results:\n")
                for func_result in log.function_results:
                    # Indented function results
                    result_line = f"    {func_result.function_name}, "
                    result_line += f"result: {func_result.status}, "
                    result_line += f"duration: {func_result.duration:.2f}s"
                    if func_result.error_message:
                        result_line += f", error: {func_result.error_message}"
                    if func_result.screenshot_path:
                        result_line += f", screenshot: {func_result.screenshot_path}"
                    f.write(result_line + "\n")
                f.write("-" * 50 + "\n\n")

    def flush(self) -> str:
        """Format test results for user display"""
        print(f"Basic settings in flush: {self._basic_settings}")
        # Create header
        current_date = datetime.now().strftime("%m/%d")
        title = f"금일 홈페이지 ({current_date})점검입니다"
        lines = [title]
        # Add each module's result
        for i in self.module_logs.items():
            print(i)
            
        for i, (module_name, log) in enumerate(self.module_logs.items(), 1):
            # Get Korean name from metadata stored during logging
            korean_name = log.settings.get('metadata', {}).get('name', module_name)
            korean_name = korean_name.encode('utf-8').decode('utf-8')
            
            # Determine status and format line
            if log.status == "Success":
                status_text = "이상 없음"
            else:
                log_path = self.log_directory / f"test_session_{self.session_timestamp}.log"
                status_text = f"오류!!! (상세 로그: {log_path})"
            
            # Format style
            result_line = f"{i}.{korean_name} - {status_text}"
            lines.append(result_line)
        report = "\n".join(lines)
        report = report.encode('utf-8').decode('utf-8')

        # Email results if configured true
        # self.console(self.basic_settings)
        # import pdb
        # breakpoint()

        if self.basic_settings['email']:
            try:
                sender_email = self.basic_settings['sender_email']
                recipient_email = self.basic_settings['recipient_email']
                password = self.basic_settings['sender_passkey']
                
                msg = EmailMessage()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = title
                msg.set_content(report)

                # Connect to Gmail's SMTP server
                with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                    print("Connecting to SMTP server...")
                    smtp.starttls()
                    print("Starting TLS...")
                    try:
                        smtp.login(sender_email, password)
                        print("Login successful")
                    except smtplib.SMTPAuthenticationError as auth_error:
                        print(f"Authentication failed: {auth_error}")
                        return report
                    try:
                        smtp.send_message(msg)
                        print("Log sent through email successfully")
                    except Exception as send_error:
                        print(f"Failed to send email: {send_error}")
            except Exception as e:
                print(f"Email error: {e}")
            return report

class LoggingContext:
    """Maintains logging state for module execution"""
    def __init__(self, enabled: bool, module_name: str):
        self.enabled = enabled
        self.module_name = module_name

class LoggingState:
    """Manages the current logging context"""
    _current_context: Optional[LoggingContext] = None

    @classmethod
    def get_current_context(cls) -> Optional[LoggingContext]:
        return cls._current_context

    @classmethod
    @contextmanager
    def module_context(cls, enabled: bool, module_name: str):
        previous_context = cls._current_context
        current_context = LoggingContext(enabled=enabled, module_name=module_name)
        cls._current_context = current_context
        try:
            yield current_context
        finally:
            cls._current_context = previous_context

def module_logging(func: Callable):
    """Module-level decorator that sets up logging context and handles module logging"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Get required fixtures
        settings = kwargs.get('settings') or next(
            (arg for arg in args if hasattr(arg, 'get_module_options')), 
            None
        )
        test_logger = kwargs.get('test_logger') or next(
            (arg for arg in args if hasattr(arg, 'start_module')),
            None
        )
        
        if not settings or not test_logger:
            return await func(*args, **kwargs)

        module_name = Path(func.__code__.co_filename).name
        module_settings = settings.get_module_all(module_name)

        logging_enabled = module_settings['options'].get('log', False)

        if not logging_enabled:
            return await func(*args, **kwargs)

        # Start module logging and establish context
        test_logger.start_module(module_name, module_settings)
        
        with LoggingState.module_context(logging_enabled, module_name):
            try:
                result = await func(*args, **kwargs)
                test_logger.end_module(module_name, True)
                return result
            except Exception as e:
                test_logger.end_module(module_name, False)
                raise
    return wrapper

def function_logging(func: Callable):
    """Function-level decorator that logs function execution within module context"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Check if we're in a logging context
        context = LoggingState.get_current_context()
        if not context or not context.enabled:
            return await func(*args, **kwargs)

        # Get logger
        test_logger = kwargs.get('test_logger') or next(
            (arg for arg in args if hasattr(arg, 'start_module')),
            None
        )
        
        if not test_logger:
            return await func(*args, **kwargs)

        start_time = time.time()
        screenshot_path = None  # You can add screenshot capture logic here if needed

        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            
            test_logger.add_function_result(
                module_name=context.module_name,
                function_name=func.__name__,
                status="Success",
                duration=duration,
                screenshot_path=screenshot_path
            )   
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            
            # You might want to capture screenshot on failure
            # screenshot_path = capture_failure_screenshot()
            
            test_logger.add_function_result(
                module_name=context.module_name,
                function_name=func.__name__,
                status="Failed",
                duration=duration,
                error_message=str(e),
                screenshot_path=screenshot_path
            )
            raise

    return wrapper