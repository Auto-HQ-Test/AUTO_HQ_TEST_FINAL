import pytest
import logging
from pathlib import Path
import sys
import datetime
import os
import json
from typing import Dict, Any, List, Optional
from gui_runner import ConfigManager


class AutoHQtestRunner:
    def __init__(self):
        self.test_modules: List[str] = []
        self.module_runner_options: Dict[str, dict] = {}

    def add_test_module(self, module_name:str) -> None:
        # Add a test module
        module_name = str(module_name)
        if module_name not in self.test_modules:
            self.test_modules.append(os.path.join(project_root, 'tests', module_name))
            print(f"Added test module: {module_name}")

    def add_test_modules_at(self, module_path:str) -> None:
        # Add all test modules that exist at a given directory
        module_path = str(module_path)
        for file in os.listdir(module_path):
            if file.startswith('test') and file.endswith(".py"):
                self.add_test_module(file)

    def run(self):
        """Run all modules listed at self.test_modules.
        Modules that aren't checked are skipped.
        """
        try:
            result = pytest.main(self.test_modules)
            return result
        except Exception as e:
            print(f"Runner encountered error: {str(e)}")
            raise

def setup_env():
    """Perform miscellaneous setup options to support runner instance."""
    project_root = str(Path(__file__).parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


if __name__ == "__main__":
    setup_env()
    project_root = str(Path(__file__).parent)
    config_manager = ConfigManager()
    runner = AutoHQtestRunner()
    runner.add_test_modules_at(os.path.join(project_root, "tests"))
    sys.exit(runner.run())