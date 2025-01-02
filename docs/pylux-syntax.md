# PyLux Language Reference

PyLux is the testing language powering LumenQA. It's designed to be intuitive, expressive, and optimized for browser automation.

## Language Overview

PyLux is:
- **Python-inspired** - Familiar syntax for Python developers
- **Async-first** - Built for concurrent execution
- **Type-safe** - Intelligent autocomplete and validation
- **Compiled** - LumenVM compiles to optimized bytecode

## Test Structure

### Basic Test

```pylux
test "Test description":
    # Test steps
    navigate "https://example.com"
    expect title "Example"
```

### Async Test

```pylux
async test "Async test":
    await navigate "https://example.com"
    await all:
        - expect element ".header" visible
        - expect element ".footer" visible
```

## Navigation

### Navigate to URL

```pylux
navigate "https://example.com"
navigate "https://example.com/page?param=value"
```

### Go Back/Forward

```pylux
back
forward
refresh
```

### Wait for Navigation

```pylux
navigate "https://example.com"
wait for navigation
```

## Selectors

PyLux supports multiple selector types:

### CSS Selectors

```pylux
click "#button-id"
click ".button-class"
click "button[type='submit']"
click "div > button:first-child"
```

### Text Content

```pylux
click "Button Text"
click "Sign In"
expect text "Welcome"
```

### XPath

```pylux
click xpath="//button[@id='submit']"
```

### Data Attributes

```pylux
click "[data-testid='submit-button']"
```

### Self-Healing Selectors

Use fallback strategies (LumenQA tries each in order):

```pylux
click "Submit" or button[type=submit] or #submit-btn
```

## Interactions

### Click

```pylux
click ".button"
click "Button Text"
double_click ".item"
right_click ".context-menu"
```

### Input

```pylux
# Type text
input #email => "test@example.com"
input "[name='username']" => "john_doe"

# Clear and type
clear #email
input #email => "new@example.com"

# Type slowly (for autocomplete)
input #search => "query" slowly

# Use secrets (not logged)
input #password => secret("PASSWORD")
```

### Keyboard

```pylux
press "Enter"
press "Escape"
press "Tab"
press "Control+A"
press "Command+S"  # macOS

# Type multiple keys
type "Hello World"
```

### Mouse

```pylux
hover ".menu-item"
drag ".draggable" to ".drop-zone"
scroll to ".footer"
scroll by 500  # pixels
```

### Select

```pylux
select #country => "United States"
select #role => option[value="admin"]
```

### Checkboxes & Radio

```pylux
check "#agree-terms"
uncheck "#newsletter"
select_radio "[name='plan']" value="premium"
```

## Assertions

### Element Visibility

```pylux
expect element ".header" visible
expect element ".loading" not_visible
expect element ".modal" hidden
```

### Text Content

```pylux
expect text "Welcome"
expect text contains "Hello"
expect element "h1" text = "Dashboard"
expect element ".count" text matches /\d+ items/
```

### Element States

```pylux
expect element "#submit" enabled
expect element "#disabled-btn" disabled
expect element "#checkbox" checked
expect element "#unchecked" not_checked
```

### Attributes

```pylux
expect element "img" has_attribute "src"
expect element "a" attribute "href" = "https://example.com"
expect element "input" has_value "test"
```

### URL

```pylux
expect url = "https://example.com/dashboard"
expect url contains "/dashboard"
expect url matches /\/user\/\d+/
```

### Count

```pylux
expect element ".item" count = 5
expect element ".product" count > 10
expect element ".error" count = 0
```

### Console

```pylux
expect console.errors count = 0
expect console.warnings count < 3
expect console.logs contains "API call successful"
```

### Network

```pylux
expect network.requests count > 5
expect network.request "/api/users" status = 200
```

## Waiting

### Implicit Waits

LumenQA automatically waits for elements to be:
- Present in DOM
- Visible
- Enabled
- Stable (not animating)

### Explicit Waits

```pylux
# Wait for element
wait for element ".async-content" visible
wait max 10s for element ".slow" visible

# Wait for condition
wait until element ".counter" text = "100"
wait until url contains "/success"

# Wait for time
wait 2s
wait 500ms
```

## Variables

### Set Variables

```pylux
set username = "john_doe"
set user_id = 123
set is_admin = true
```

### Use Variables

```pylux
input #username => username
navigate f"https://example.com/users/{user_id}"

if is_admin:
    expect element ".admin-panel" visible
```

### Store from Elements

```pylux
get element ".user-name" text => username
get element "#user-id" attribute "data-id" => user_id
```

## Control Flow

### Conditionals

```pylux
if element ".login-button" visible:
    click ".login-button"
else:
    expect text "Already logged in"
```

### Loops

```pylux
for item in [1, 2, 3, 4, 5]:
    click f".item-{item}"
    expect element f"#selected-{item}" visible
```

### Data-Driven Tests

```pylux
test "Login with multiple users" for each user in users.csv:
    navigate "https://app.com/login"
    input #email => user.email
    input #password => user.password
    click "Login"
    expect text f"Welcome, {user.name}"
```

## API Testing

### HTTP Requests

```pylux
# GET request
api GET "/api/users" => response
expect response.status = 200
expect response.body.length > 0

# POST request
api POST "/api/users" {
    name: "John Doe",
    email: "john@example.com"
} => response

expect response.status = 201
set user_id = response.body.id

# PUT request
api PUT f"/api/users/{user_id}" {
    name: "Jane Doe"
}

# DELETE request
api DELETE f"/api/users/{user_id}"
expect response.status = 204
```

### GraphQL

```pylux
gql query {
    user(id: "123") {
        name
        email
        posts {
            title
        }
    }
} => result

expect result.data.user.name = "John Doe"
```

## Mock API

```pylux
mock api "/api/products" returns {
    products: [
        {id: 1, name: "Product A"},
        {id: 2, name: "Product B"}
    ]
}

navigate "https://app.com/products"
expect element ".product-card" count = 2
```

## Async & Parallelism

### Async/Await

```pylux
async test "Async operations":
    await navigate "https://example.com"
    await click ".button"
    await expect text "Success"
```

### Parallel Execution

```pylux
async test "Parallel checks":
    await navigate "https://example.com"

    # All these run simultaneously
    await all:
        - expect element ".header" visible
        - expect element ".footer" visible
        - expect element ".sidebar" visible
        - screenshot "page-loaded"
```

### Sequential with Await

```pylux
async test "Sequential async":
    await navigate "https://example.com"
    await click ".load-data"
    await wait for element ".data-loaded" visible
    await screenshot "final-state"
```

## Screenshots & Videos

### Screenshots

```pylux
screenshot "homepage"
screenshot "error-state" full_page=true
screenshot element ".dialog"
```

### Videos

```pylux
start_recording
navigate "https://example.com"
click ".feature"
stop_recording "feature-demo"
```

## Custom Commands

### Define Reusable Commands

```pylux
command login_as(email, password):
    navigate "https://app.com/login"
    input #email => email
    input #password => password
    click "Login"
    wait for url contains "/dashboard"

# Use custom command
test "Admin dashboard":
    login_as("admin@example.com", secret("ADMIN_PASS"))
    expect element ".admin-panel" visible
```

## Comments

```pylux
# Single line comment

test "Example":
    # This is a comment
    navigate "https://example.com"

    # Multi-step explanation:
    # 1. Click the button
    # 2. Wait for modal
    # 3. Verify content
    click ".open-modal"
```

## Error Handling

### Try/Catch

```pylux
try:
    click ".optional-button"
catch:
    # Button doesn't exist, that's okay
    pass

try:
    expect text "Expected"
catch error:
    screenshot "error-state"
    fail f"Unexpected error: {error}"
```

## Best Practices

### Use Descriptive Test Names

```pylux
# Good
test "User can add product to cart and proceed to checkout"

# Bad
test "Test 1"
```

### Leverage Self-Healing Selectors

```pylux
# Good - multiple fallback strategies
click "Submit" or button[type=submit] or #submit-btn

# Less resilient
click "#submit-btn"
```

### Keep Tests Independent

```pylux
# Each test should set up its own state
test "Test 1":
    api POST "/api/setup-data"
    # test steps
    api DELETE "/api/cleanup"
```

### Use Page Objects

```pylux
# Define reusable components
command login_page.fill_credentials(email, password):
    input #email => email
    input #password => password

command login_page.submit():
    click "Login"

# Use in tests
test "Login":
    login_page.fill_credentials("user@test.com", "password")
    login_page.submit()
```

## Next Steps

- **[API Reference](api-reference.md)** - Complete command list
- **[Examples](../examples/)** - Real-world test examples
- **[Best Practices](guides/best-practices.md)** - Writing maintainable tests
