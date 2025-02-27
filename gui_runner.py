import sys
import os
import json
import pytest
from pathlib import Path
from typing import Dict, Any, List
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QCheckBox, 
                           QPushButton, QGroupBox, QTabWidget, QMessageBox,
                           QScrollArea, QTextEdit, QStatusBar, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtCore import QTextCodec
from PyQt5.QtGui import QFont

sys.stdout.reconfigure(encoding='utf-8')

class TestRunnerThread(QThread):
    """Thread-based test runner that manages test module execution."""
    finished = pyqtSignal(str)   # Emits test results
    error = pyqtSignal(str)       # Emits error messages
    progress = pyqtSignal(str)    # Emits progress updates

    def __init__(self):
        super().__init__()
        self.test_modules: List[str] = []
        self.project_root = str(Path(__file__).parent)
        
        if self.project_root not in sys.path:
            sys.path.insert(0, self.project_root)
            self.progress.emit(f"{self.project_root} added to sys.path")


    def add_test_module(self, module_name: str) -> None:
        module_name = str(module_name)
        module_path = os.path.join(self.project_root, 'tests', module_name)
        
        if module_path not in self.test_modules:
            self.test_modules.append(module_path)
            self.progress.emit(f"Added test module: {module_name}")


    def clear_modules(self):
        self.test_modules.clear()
        self.progress.emit("Cleared test modules")


    def run(self):
        if not self.test_modules:
            self.error.emit("No test modules specified")
            return

        try:
            self.progress.emit("Starting test execution...")
            result = pytest.main(self.test_modules)
            from utils.registry import TestRegistry
            test_logger = TestRegistry.get_logger()
            report = test_logger.flush()
            self.progress.emit("Test execution completed")
            self.finished.emit(report)
            
        except Exception as e:
            error_msg = f"Runner encountered error: {str(e)}"
            self.error.emit(error_msg)


class ConfigManager:
    """Manages configuration loading and saving."""
    DEFAULT_OPTIONS = {
        "submit": False,
        "email": False,
        "headless": True,
        "log": True,
        "run": True,
        "chrome": True
    }

    def __init__(self, config_path: str = "configs.json"):
        self.config_path = config_path
        self.config_data = {
            "modules": {},
            "basic": {
                "sender_email": "",
                "recipient_email": "",
                "sender_passkey": ""
            }
        }
        self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                self.config_data.update(loaded_config)
            return self.config_data
        except FileNotFoundError:
            print(f"No existing config file found at {self.config_path}")
            return self.config_data
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.config_data

    def _save_config(self) -> None:
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, indent=4, ensure_ascii=False, fp=f)
            print(f"Configuration saved successfully to {self.config_path}")
        except Exception as e:
            print(f"Error saving config: {e}")


class ConfigurationWindow(QMainWindow):
    """Main configuration window with integrated test runner."""
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        self.runner = None
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Test Configuration Manager")
        self.setGeometry(100, 100, 1000, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Add tabs
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        tab_widget.addTab(self.create_modules_tab(), "Module Settings")
        tab_widget.addTab(self.create_basic_tab(), "Basic Settings")
        
        # Reset button
        reset_button = QPushButton("Reset to Default")
        reset_button.clicked.connect(self.reset_to_default)
        main_layout.addWidget(reset_button)
        
        # Results area
        self.results_area = QTextEdit()
        self.results_area.setReadOnly(True)
        self.results_area.setMinimumHeight(200)
        main_layout.addWidget(self.results_area)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_config)
        button_layout.addWidget(save_button)
        
        self.run_button = QPushButton("Save and Run")
        self.run_button.clicked.connect(self.save_and_run)
        button_layout.addWidget(self.run_button)
        
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def create_modules_tab(self) -> QWidget:
        tab = QWidget()
        main_layout = QVBoxLayout(tab)
        
        description = QLabel("Configure settings for specific test modules.")
        description.setWordWrap(True)
        main_layout.addWidget(description)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        self.module_checkboxes = {}
        self.module_run_checkboxes = {}
        self.module_groups = {}
        
        modules_settings = self.config_manager.config_data["modules"]

        for module, settings in modules_settings.items():
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 5, 0, 5)
            
            # Module information
            metadata = settings.get('metadata', {})
            metadata_group = QGroupBox("Module Information")
            metadata_layout = QVBoxLayout()
            
            name_label = QLabel(f"Name: {metadata.get('name', 'Unnamed')}")
            desc_label = QLabel(f"Description: {metadata.get('description', 'No description')}")
            desc_label.setWordWrap(True)
            
            metadata_layout.addWidget(name_label)
            metadata_layout.addWidget(desc_label)
            metadata_group.setLayout(metadata_layout)
            container_layout.addWidget(metadata_group)
            
            # Options
            options = settings.get('options', {})
            options_group = QGroupBox("Options")
            options_layout = QVBoxLayout()
            
            run_checkbox = QCheckBox("Run")
            run_checkbox.setChecked(options.get('run', True))
            self.module_run_checkboxes[module] = run_checkbox
            options_layout.addWidget(run_checkbox)
            
            module_dict = {}
            for key, value in options.items():
                if key != 'run':
                    checkbox = QCheckBox(key.capitalize())
                    checkbox.setChecked(value)
                    module_dict[key] = checkbox
                    options_layout.addWidget(checkbox)
            
            self.module_checkboxes[module] = module_dict
            self.module_groups[module] = options_group
            
            options_group.setLayout(options_layout)
            container_layout.addWidget(options_group)
            
            run_checkbox.stateChanged.connect(
                lambda state, m=module: self.toggle_module_settings(m, state)
            )
            
            self.toggle_module_settings(module, run_checkbox.isChecked())
            
            scroll_layout.addWidget(container)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        return tab

    def create_basic_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        group_box = QGroupBox("Email Settings")
        group_layout = QVBoxLayout()
        description = QLabel("Configure email settings for test notifications and reports.")
        description.setWordWrap(True)
        group_layout.addWidget(description)

            # Add email enable checkbox
        self.email_checkbox = QCheckBox("Enable Email Notifications")
        self.email_checkbox.setChecked(self.config_manager.config_data["basic"].get("email", False))
        group_layout.addWidget(self.email_checkbox)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        group_layout.addWidget(line)
        # Email detail inputs
        self.basic_inputs = {}
        basic_settings = self.config_manager.config_data["basic"]
        
        for key, value in basic_settings.items():
            if key != "email":  # Skip email bool since we handle it with checkbox
                h_layout = QHBoxLayout()
                label = QLabel(key.replace('_', ' ').title() + ":")
                label.setMinimumWidth(120)
                
                input_field = QLineEdit()
                input_field.setText(value)
                if 'passkey' in key:
                    input_field.setEchoMode(QLineEdit.Password)
                
                h_layout.addWidget(label)
                h_layout.addWidget(input_field)
                self.basic_inputs[key] = input_field
                group_layout.addLayout(h_layout)
        
        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        layout.addStretch()
        return tab

    def toggle_module_settings(self, module: str, state: int):
        enabled = bool(state)
        group_box = self.module_groups[module]
        
        for checkbox in self.module_checkboxes[module].values():
            checkbox.setEnabled(enabled)
        
        if enabled:
            group_box.setStyleSheet("")
        else:
            group_box.setStyleSheet("QGroupBox { background-color: #f0f0f0; }")

    def update_config_from_ui(self):
        # Save module options
        for module, checkboxes in self.module_checkboxes.items():
            run_state = self.module_run_checkboxes[module].isChecked()
            self.config_manager.config_data["modules"][module]["options"]["run"] = run_state
            
            for key, checkbox in checkboxes.items():
                self.config_manager.config_data["modules"][module]["options"][key] = checkbox.isChecked()
        
        # Save emailing options
        self.config_manager.config_data["basic"]["email"] = self.email_checkbox.isChecked()
        
        # Save basic options
        for key, input_field in self.basic_inputs.items():
            self.config_manager.config_data["basic"][key] = input_field.text()

    def reset_to_default(self):
        for module_checkboxes in self.module_checkboxes.values():
            for key, checkbox in module_checkboxes.items():
                default_value = self.config_manager.DEFAULT_OPTIONS.get(key, False)
                checkbox.setChecked(default_value)
        
        for run_checkbox in self.module_run_checkboxes.values():
            run_checkbox.setChecked(True)
        
        QMessageBox.information(self, "Reset Complete", 
                              "Settings have been reset to default values.\n"
                              "Click 'Save' to keep these changes.")

    def save_config(self):
        self.update_config_from_ui()
        self.config_manager._save_config()
        QMessageBox.information(self, "Success", "Configuration saved successfully!")

    def save_and_run(self):
        self.update_config_from_ui()
        self.config_manager._save_config()
        
        self.disable_ui_controls()
        
        self.runner = TestRunnerThread()
        self.runner.finished.connect(self.display_results)
        self.runner.error.connect(self.display_error)
        self.runner.progress.connect(self.update_progress)
        
        self.runner.clear_modules()
        for module, checkboxes in self.module_checkboxes.items():
            if self.module_run_checkboxes[module].isChecked():
                self.runner.add_test_module(module)
        
        self.runner.start()

    def disable_ui_controls(self):
        self.run_button.setEnabled(False)
        self.status_bar.showMessage("Running tests...")

    def enable_ui_controls(self):
        self.run_button.setEnabled(True)
        self.status_bar.showMessage("Ready")

    def display_results(self, results: dict):
        self.results_area.setFontFamily("Malgun Gothic")  # Korean font
        self.results_area.setText(results)
        self.enable_ui_controls()
        self.status_bar.showMessage("Test execution completed")

    def display_error(self, error_msg: str):
        QMessageBox.critical(self, "Error", f"Test run failed: {error_msg}")
        self.enable_ui_controls()
        self.status_bar.showMessage("Test execution failed")

    def update_progress(self, message: str):
        self.status_bar.showMessage(message)

def main():
    app = QApplication(sys.argv)
    config_manager = ConfigManager("configs.json")
    window = ConfigurationWindow(config_manager)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()