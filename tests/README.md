# Test Suite Documentation

## Overview
This test suite validates the core functionality of the Soul Foods Pink Morsel Sales Visualizer Dash application.

## Test Framework
- **Framework**: Pytest with Dash testing plugin
- **Browser Automation**: Selenium WebDriver with ChromeDriver (headless mode)
- **Configuration**: `tests/conftest.py` handles ChromeDriver setup automatically

## Test Cases

### 1. test_header_present
**Purpose**: Verify that the application header is displayed correctly.

**Test Steps**:
1. Start the Dash application
2. Wait for the H1 element to load
3. Verify the header contains "Pink Morsel Sales Analysis"

**Expected Result**: Header is present with correct text

**Status**: ✓ PASSED

---

### 2. test_visualization_present
**Purpose**: Verify that the main sales chart visualization is rendered.

**Test Steps**:
1. Start the Dash application
2. Wait for the sales-chart element to load
3. Verify the chart contains a plotly graph component

**Expected Result**: Sales chart is present and rendered with Plotly

**Status**: ✓ PASSED

---

### 3. test_region_picker_present
**Purpose**: Verify that the region filter radio buttons are present and functional.

**Test Steps**:
1. Start the Dash application
2. Wait for the region-filter element to load
3. Verify all five radio button options exist (all, north, south, east, west)
4. Verify the default selection is 'all'

**Expected Result**: All region filter radio buttons are present with correct default

**Status**: ✓ PASSED

---

## Running the Tests

### Run all three required tests:
```bash
.venv\Scripts\python.exe -m pytest tests/test_app.py::test_header_present tests/test_app.py::test_visualization_present tests/test_app.py::test_region_picker_present -v
```

### Run all tests in the file:
```bash
.venv\Scripts\python.exe -m pytest tests/test_app.py -v
```

### Run with detailed output:
```bash
.venv\Scripts\python.exe -m pytest tests/test_app.py -v -s
```

## Test Environment
- **Python**: 3.13.7
- **Pytest**: 9.0.2
- **Dash**: 3.3.0
- **Selenium**: 4.2.0
- **Chrome**: Run in headless mode (no GUI)
- **Operating System**: Windows

## Dependencies
All testing dependencies are installed via:
```bash
pip install dash[testing] webdriver-manager
```

## Test Results Summary
- **Total Tests**: 3
- **Passed**: 3
- **Failed**: 0
- **Success Rate**: 100%

## Notes
- Tests run in headless Chrome browser mode for CI/CD compatibility
- ChromeDriver is automatically downloaded and managed via webdriver-manager
- Each test starts a fresh Dash server instance on a unique port
- Tests validate both presence and functionality of UI components
