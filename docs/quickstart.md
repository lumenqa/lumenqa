# Quick Start Guide

Get up and running with LumenQA in 5 minutes!

## Prerequisites

- Python 3.9+ installed
- LumenQA installed (`pip install lumenqa`)

## Your First Test

### Step 1: Initialize a Project

```bash
mkdir my-tests
cd my-tests
lumen init .
```

This creates:

```
my-tests/
├── lumen.yml
├── tests/
│   └── example.lux
└── .lumenignore
```

### Step 2: Write a Test

Edit `tests/example.lux`:

```pylux
test "Google search works":
    navigate "https://www.google.com"

    # Type search query
    input "[name='q']" => "LumenQA framework"

    # Submit search
    press "Enter"

    # Verify results appeared
    expect element "#search" visible
    expect text "results"
```

### Step 3: Run Your Test

```bash
lumen run tests/example.lux
```

**Output:**

```
🚀 LumenQA v0.9.4 - LumenVM Runtime
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Loading intent trees
✓ Compiling PyLux → bytecode
✓ Initializing GPU-accelerated DOM engine

Running: tests/example.lux

✓ Google search works (412ms)
  ├─ navigate → 156ms
  ├─ input[name='q'] → 18ms
  ├─ press "Enter" → 203ms
  └─ assertions → 35ms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 1 passed, 0 failed (412ms total)
📊 Performance: 7.1x faster than Playwright
```

Congratulations! You just ran your first LumenQA test.

## Understanding the Syntax

### Test Declaration

```pylux
test "Description of what this tests":
    # Test steps go here
```

### Navigation

```pylux
navigate "https://example.com"
```

### Interactions

```pylux
# Click elements
click "Button Text"
click "#button-id"
click ".button-class"

# Type into inputs
input #email => "test@example.com"
input "[name='password']" => "secret123"

# Other interactions
press "Enter"
hover ".menu-item"
select #country => "United States"
```

### Assertions

```pylux
# Check element visibility
expect element ".header" visible
expect element ".loading" not_visible

# Check text content
expect text "Welcome!"
expect element "h1" contains "Dashboard"

# Check URL
expect url = "https://example.com/dashboard"
expect url contains "/dashboard"

# Check attributes
expect element "#submit" enabled
expect element "input" has_value "test"
```

## More Examples

### Login Flow

```pylux
test "User can log in":
    navigate "https://app.example.com/login"

    input #email => "user@test.com"
    input #password => secret("PASSWORD")

    click "Sign In"

    expect url contains "/dashboard"
    expect text "Welcome back"
```

### Form Submission

```pylux
test "Contact form submission":
    navigate "https://example.com/contact"

    input #name => "John Doe"
    input #email => "john@example.com"
    textarea #message => "Hello from LumenQA!"

    click "Send"

    expect text "Message sent successfully"
```

### E-commerce

```pylux
test "Add product to cart":
    navigate "https://shop.example.com"

    # Search for product
    input "[name='search']" => "laptop"
    press "Enter"

    # Select first result
    click ".product-card:first"

    # Add to cart
    click "Add to Cart"

    # Verify cart updated
    expect element ".cart-count" text = "1"
```

## Running Multiple Tests

Create multiple test files:

```
tests/
├── login.lux
├── signup.lux
└── checkout.lux
```

Run all tests:

```bash
lumen run tests/
```

Run specific tests:

```bash
lumen run tests/login.lux tests/signup.lux
```

## Parallel Execution

Run tests in parallel (4 workers):

```bash
lumen run tests/ --parallel 4
```

Or configure in `lumen.yml`:

```yaml
parallelization: 4
```

## Different Browsers

Run in Firefox:

```bash
lumen run tests/ --browser firefox
```

Run in headed mode (see the browser):

```bash
lumen run tests/ --headed
```

## Configuration

Edit `lumen.yml` to customize:

```yaml
framework: lumenqa
version: 0.9.4

# Run 4 tests in parallel
parallelization: 4

# Test both browsers
browsers:
  - chrome
  - firefox

# See the browser window
headless: false

# Enable GPU acceleration
lumenvm:
  gpu_acceleration: true

# Take screenshots on failure
reporting:
  screenshots: on-failure
  videos: on-failure
```

## Next Steps

### Learn More

- **[PyLux Language Reference](pylux-syntax.md)** - Complete syntax guide
- **[API Reference](api-reference.md)** - All commands
- **[Best Practices](guides/best-practices.md)** - Write better tests

### Advanced Features

- **[Parallel Execution](guides/parallel-execution.md)** - Scale your tests
- **[CI/CD Integration](guides/ci-integration.md)** - Automate testing
- **[API Testing](guides/api-testing.md)** - Combine API + UI tests

### Migration

Already have tests in another framework?

- **[From Playwright](migration/from-playwright.md)**
- **[From Selenium](migration/from-selenium.md)**
- **[From Cypress](migration/from-cypress.md)**

Use our automated converter:

```bash
lumen convert --from playwright tests/
```

## Tips for Success

1. **Use descriptive test names** - Make it clear what's being tested
2. **Keep tests independent** - Each test should run in isolation
3. **Use self-healing selectors** - Leverage LumenQA's intent trees
4. **Enable GPU acceleration** - Get maximum performance
5. **Run tests in parallel** - Speed up your test suite

## Common Issues

### Element Not Found

LumenQA automatically waits for elements, but you can add explicit waits:

```pylux
wait for element ".slow-loading" visible
wait max 10s for element ".delayed" visible
```

### Flaky Tests

Use LumenQA's retry mechanism in `lumen.yml`:

```yaml
retries: 2  # Retry failed tests twice
```

### Slow Tests

Enable parallel execution:

```yaml
parallelization: auto  # Auto-detect CPU cores
```

## Getting Help

- 💬 [Discord Community](https://discord.gg/lumenqa)
- 📖 [Full Documentation](index.md)
- 🐛 [Report Issues](https://github.com/lumenqa/lumenqa/issues)
- 📧 support@lumenqa.dev

---

**Happy Testing!** 🚀
