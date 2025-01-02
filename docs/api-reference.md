# API Reference

Complete reference for all LumenQA/PyLux commands and methods.

## Navigation Commands

### `navigate(url: string)`
Navigate to a URL.

```pylux
navigate "https://example.com"
```

### `back()`
Go back in browser history.

### `forward()`
Go forward in browser history.

### `refresh()`
Refresh the current page.

## Interaction Commands

### `click(selector: string)`
Click an element.

```pylux
click ".button"
click "Button Text"
```

**Options:**
- `force=true` - Click even if element is hidden
- `timeout=10s` - Custom timeout

### `double_click(selector: string)`
Double-click an element.

### `right_click(selector: string)`
Right-click (context menu).

### `input(selector: string, value: string)`
Type text into an input field.

```pylux
input #email => "test@example.com"
```

**Options:**
- `slowly=true` - Type character by character
- `clear=true` - Clear field first (default: true)

### `clear(selector: string)`
Clear an input field.

### `press(key: string)`
Press a keyboard key.

```pylux
press "Enter"
press "Escape"
press "Control+C"
```

### `hover(selector: string)`
Hover over an element.

### `drag(from: string, to: string)`
Drag and drop.

```pylux
drag ".item" to ".drop-zone"
```

### `scroll(target: string | number)`
Scroll to element or by pixels.

```pylux
scroll to ".footer"
scroll by 500
```

### `select(selector: string, value: string)`
Select option from dropdown.

```pylux
select #country => "United States"
```

### `check(selector: string)`
Check a checkbox.

### `uncheck(selector: string)`
Uncheck a checkbox.

## Assertion Commands

### `expect element(selector: string) state`
Assert element state.

**States:**
- `visible` - Element is visible
- `hidden` / `not_visible` - Element is not visible
- `enabled` - Element is enabled
- `disabled` - Element is disabled
- `checked` - Checkbox is checked
- `not_checked` - Checkbox is unchecked

```pylux
expect element ".button" visible
expect element "#disabled" disabled
```

### `expect text(content: string)`
Assert text exists on page.

```pylux
expect text "Welcome"
expect text contains "Hello"
```

### `expect url`
Assert URL matches condition.

```pylux
expect url = "https://example.com"
expect url contains "/dashboard"
expect url matches /\/user\/\d+/
```

### `expect element count`
Assert number of elements.

```pylux
expect element ".item" count = 5
expect element ".error" count = 0
```

### `expect console`
Assert console state.

```pylux
expect console.errors count = 0
expect console.warnings count < 3
```

## Wait Commands

### `wait for element(selector: string) state`
Wait for element to reach state.

```pylux
wait for element ".loading" visible
wait for element ".data" visible
```

**Options:**
- `max 10s` - Maximum wait time

### `wait until condition`
Wait until condition is true.

```pylux
wait until url contains "/success"
wait until element ".counter" text = "100"
```

### `wait(duration: string)`
Wait for specific time.

```pylux
wait 2s
wait 500ms
```

## Variable Commands

### `set variable = value`
Set a variable.

```pylux
set username = "john_doe"
set count = 42
```

### `get element property => variable`
Store element property in variable.

```pylux
get element ".name" text => username
get element "#id" attribute "data-id" => user_id
```

## API Commands

### `api METHOD(url: string, body?: object) => variable`
Make HTTP request.

```pylux
api GET "/api/users" => response
api POST "/api/users" {name: "John"} => response
api PUT "/api/users/123" {name: "Jane"}
api DELETE "/api/users/123"
```

**Response properties:**
- `response.status` - HTTP status code
- `response.body` - Response body (parsed JSON)
- `response.headers` - Response headers

### `gql query => variable`
Execute GraphQL query.

```pylux
gql query {
    user(id: "123") {
        name
        email
    }
} => result
```

### `mock api(url: string) returns data`
Mock API endpoint.

```pylux
mock api "/api/data" returns {items: []}
```

## Screenshot/Video Commands

### `screenshot(name: string)`
Take a screenshot.

```pylux
screenshot "homepage"
screenshot "error" full_page=true
screenshot element ".modal"
```

### `start_recording()`
Start video recording.

### `stop_recording(name: string)`
Stop and save video.

```pylux
start_recording
# test steps
stop_recording "test-flow"
```

## Control Flow

### `if condition:`
Conditional execution.

```pylux
if element ".logout" visible:
    click ".logout"
else:
    navigate "/login"
```

### `for item in collection:`
Loop over collection.

```pylux
for i in [1, 2, 3]:
    click f".item-{i}"
```

### `try: ... catch:`
Error handling.

```pylux
try:
    click ".optional"
catch:
    pass
```

## Custom Commands

### `command name(params):`
Define reusable command.

```pylux
command login_as(email, password):
    navigate "/login"
    input #email => email
    input #password => password
    click "Login"
```

## Async Commands

### `async test`
Define async test.

```pylux
async test "Parallel operations":
    await navigate "https://example.com"
```

### `await all:`
Execute in parallel.

```pylux
await all:
    - expect element ".header" visible
    - expect element ".footer" visible
```

## Special Functions

### `secret(name: string)`
Access secret environment variable (not logged).

```pylux
input #password => secret("PASSWORD")
```

### `f"string {variable}"`
String interpolation.

```pylux
navigate f"https://example.com/user/{user_id}"
```

## Selectors

### CSS Selectors
```pylux
".class"
"#id"
"tag[attribute='value']"
"parent > child"
```

### Text Selectors
```pylux
"Button Text"
"Sign In"
```

### XPath
```pylux
xpath="//button[@id='submit']"
```

### Combined Selectors
```pylux
"Text" or #id or .class
```

## Configuration (lumen.yml)

### Basic Structure

```yaml
framework: lumenqa
version: 0.9.4

parallelization: 4
browsers:
  - chrome
  - firefox
headless: true

lumenvm:
  gpu_acceleration: true
  intent_trees: enabled

reporting:
  type: lumencloud
  screenshots: on-failure
```

### Available Options

**Execution:**
- `parallelization: auto|off|number`
- `retries: number`
- `timeout: duration`

**Browsers:**
- `browsers: [chrome, firefox, safari, edge]`
- `headless: boolean`

**LumenVM:**
- `gpu_acceleration: boolean`
- `intent_trees: enabled|disabled`
- `dom_caching: normal|aggressive`

**Reporting:**
- `type: lumencloud|json|html|junit`
- `screenshots: always|on-failure|never`
- `videos: always|on-failure|never`

## CLI Commands

### `lumen init [path]`
Initialize new project.

```bash
lumen init my-tests
```

### `lumen run <file>`
Run tests.

```bash
lumen run tests/login.lux
lumen run tests/ --parallel 4
lumen run tests/ --browser firefox --headed
```

**Options:**
- `--parallel, -p <number>` - Parallel workers
- `--browser, -b <name>` - Browser to use
- `--headless/--headed` - Headless mode

### `lumen convert`
Convert tests from other frameworks.

```bash
lumen convert --from playwright tests/
lumen convert --from selenium tests/
```

### `lumen doctor`
System health check.

### `lumen --version`
Show version information.

---

For more detailed examples, see:
- **[PyLux Syntax Guide](pylux-syntax.md)**
- **[Examples](../examples/)**
- **[Best Practices](guides/best-practices.md)**
