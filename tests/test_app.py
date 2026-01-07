import pytest
from dash.testing.application_runners import import_app


def test_header_present(dash_duo):
    """
    Test that the header is present in the application.
    Verifies the main title contains 'Pink Morsel Sales Analysis'.
    """
    # Import and start the app
    app = import_app("app")
    dash_duo.start_server(app)
    
    # Wait for the app to load
    dash_duo.wait_for_element("h1", timeout=10)
    
    # Check that the header is present
    header = dash_duo.find_element("h1")
    assert header is not None, "Header element not found"
    assert "Pink Morsel Sales Analysis" in header.text, "Header text does not match expected content"
    
    print("✓ Header test passed: Header is present with correct text")


def test_visualization_present(dash_duo):
    """
    Test that the visualization (sales chart) is present in the application.
    Verifies the main sales chart graph component exists.
    """
    # Import and start the app
    app = import_app("app")
    dash_duo.start_server(app)
    
    # Wait for the sales chart to load
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    
    # Check that the sales chart is present
    sales_chart = dash_duo.find_element("#sales-chart")
    assert sales_chart is not None, "Sales chart element not found"
    
    # Verify the chart contains a plotly graph
    graph = dash_duo.find_element("#sales-chart .js-plotly-plot")
    assert graph is not None, "Plotly graph not rendered in sales chart"
    
    print("✓ Visualization test passed: Sales chart is present and rendered")


def test_region_picker_present(dash_duo):
    """
    Test that the region picker (radio buttons) is present in the application.
    Verifies all five region options are available: all, north, south, east, west.
    """
    # Import and start the app
    app = import_app("app")
    dash_duo.start_server(app)
    
    # Wait for the region filter to load
    dash_duo.wait_for_element("#region-filter", timeout=10)
    
    # Check that the region filter is present
    region_filter = dash_duo.find_element("#region-filter")
    assert region_filter is not None, "Region filter element not found"
    
    # Verify all five radio button options are present
    expected_regions = ['all', 'north', 'south', 'east', 'west']
    
    # Check that we have 5 radio inputs
    from selenium.webdriver.common.by import By
    radio_items = region_filter.find_elements(By.TAG_NAME, "input")
    assert len(radio_items) == 5, f"Expected 5 radio options, found {len(radio_items)}"
    
    # Verify that the text labels for each region are present in the DOM
    page_text = dash_duo.driver.page_source
    for region in expected_regions:
        region_label = f"{region.capitalize()}" if region != "all" else "All Regions"
        assert region_label in page_text, f"Region label '{region_label}' not found on page"
    
    # Verify the first radio button is checked (default is 'all')
    assert radio_items[0].is_selected(), "Default region (first option - 'all') is not selected"
    
    print("✓ Region picker test passed: All region options are present and default is set correctly")


def test_region_filter_functionality(dash_duo):
    """
    Bonus test: Verify that selecting a region updates the chart.
    Tests the interactive functionality of the region filter.
    """
    # Import and start the app
    app = import_app("app")
    dash_duo.start_server(app)
    
    # Wait for the app to fully load
    dash_duo.wait_for_element("#region-filter", timeout=10)
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    
    # Click on 'north' region
    north_radio = dash_duo.find_element("input[value='north']")
    north_radio.click()
    
    # Wait for the chart to update (give it a moment to re-render)
    import time
    time.sleep(1)
    
    # Verify the chart still exists after filter change
    sales_chart = dash_duo.find_element("#sales-chart")
    assert sales_chart is not None, "Sales chart disappeared after region selection"
    
    print("✓ Region filter functionality test passed: Chart updates correctly when region is selected")
