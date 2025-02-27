from typing import Optional
from utils.loggers import TestLogger

class TestRegistry:
    """
    A registry class that provides global access to a TestLogger instance.
    Used to share the logger between pytest fixtures and test modules.
    """
    _logger: Optional[TestLogger] = None

    @classmethod
    def set_logger(cls, logger: TestLogger) -> None:
        """
        Register the global TestLogger instance.
        """
        if not isinstance(logger, TestLogger):
            raise TypeError(f"Expected TestLogger instance, got {type(logger)}")
        cls._logger = logger

    @classmethod
    def get_logger(cls) -> TestLogger:
        """
        Return the global TestLogger instance.
        """
        if cls._logger is None:
            raise RuntimeError("TestLogger has not been initialized. Ensure it is set via TestRegistry.set_logger()")
        return cls._logger

    @classmethod
    def clear(cls) -> None:
        """Clear the stored TestLogger instance."""
        cls._logger = None