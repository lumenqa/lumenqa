"""
Generic test data for enterprise SAAS test suite
This is a demonstration suite showing LumenQA's capabilities
"""

TEST_CLASSES = {
    "TestAuthentication": [
        "test_01_login_with_valid_credentials",
        "test_02_login_with_invalid_credentials",
        "test_03_password_reset_flow",
        "test_04_two_factor_authentication",
        "test_05_session_timeout",
    ],
    "TestUserManagement": [
        "test_01_create_new_user",
        "test_02_edit_user_profile",
        "test_03_delete_user",
        "test_04_user_permissions",
        "test_05_bulk_user_operations",
    ],
    "TestDashboard": [
        "test_01_dashboard_loads_correctly",
        "test_02_widget_interactions",
        "test_03_data_refresh",
        "test_04_export_functionality",
    ],
    "TestReporting": [
        "test_01_generate_report",
        "test_02_filter_report_data",
        "test_03_export_report_pdf",
        "test_04_schedule_recurring_report",
    ],
    "TestIntegrations": [
        "test_01_api_authentication",
        "test_02_webhook_configuration",
        "test_03_third_party_sync",
    ],
    "TestSettings": [
        "test_01_update_system_settings",
        "test_02_configure_notifications",
        "test_03_manage_api_keys",
    ],
}

# Realistic test operations for each test type
TEST_OPERATIONS = {
    "pagination": [
        "Loading page",
        "Verifying pagination controls",
        "Navigating to page 2",
        "Checking page count",
        "Testing items per page selector",
    ],
    "create": [
        "Opening create form",
        "Filling required fields",
        "Validating input",
        "Submitting form",
        "Verifying creation success",
        "Checking database entry",
    ],
    "edit": [
        "Locating record",
        "Opening edit dialog",
        "Modifying fields",
        "Saving changes",
        "Verifying update",
    ],
    "delete": [
        "Selecting item",
        "Clicking delete action",
        "Confirming deletion",
        "Verifying removal from list",
    ],
    "search": [
        "Entering search term",
        "Triggering search",
        "Validating results",
        "Clearing search",
    ],
    "login": [
        "Navigate to login page",
        "Enter credentials",
        "Click login button",
        "Wait for redirect",
        "Verify dashboard loaded",
    ],
    "assign": [
        "Opening assignment modal",
        "Selecting items",
        "Confirming assignment",
        "Verifying association",
    ],
    "toggle": [
        "Locating toggle control",
        "Clicking toggle",
        "Verifying state change",
        "Checking persistence",
    ],
    "upload": [
        "Opening file picker",
        "Selecting file",
        "Starting upload",
        "Waiting for completion",
        "Verifying file processed",
    ],
}
