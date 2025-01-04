# Migrating from Selenium to LumenQA

Welcome! This guide will help you transition from Selenium to LumenQA and unlock massive performance improvements.

## Why Migrate from Selenium?

- **14.2x faster execution** - No more WebDriver overhead
- **No more WebDriver management** - LumenVM handles everything
- **Automatic waits** - Say goodbye to explicit waits and `time.sleep()`
- **Self-healing selectors** - Tests don't break when UI changes slightly
- **Modern syntax** - PyLux is cleaner than Selenium's verbose API

## Quick Comparison

### Selenium
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://example.com/login')

email = driver.find_element(By.ID, 'email')
email.send_keys('user@test.com')

password = driver.find_element(By.ID, 'password')
password.send_keys('password123')

login_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.login'))
)
login_btn.click()

WebDriverWait(driver, 10).until(
    EC.url_contains('/dashboard')
)

assert 'dashboard' in driver.current_url
driver.quit()
```

### LumenQA
```pylux
test "login flow":
    navigate "https://example.com/login"
    input #email => "user@test.com"
    input #password => "password123"
    click "Login"
    expect url contains "/dashboard"
```

**Lines of code:** 23 → 6 (74% reduction)
**Execution time:** 2.6s → 183ms (14.2x faster)

## Automatic Conversion

```bash
lumen convert --from selenium tests/
```

The converter handles:
- WebDriver initialization
- Element locators
- Waits and timeouts
- Assertions
- Test structure

## Element Location

| Selenium | LumenQA |
|----------|---------|
| `driver.find_element(By.ID, 'btn')` | `#btn` |
| `driver.find_element(By.CLASS_NAME, 'btn')` | `.btn` |
| `driver.find_element(By.CSS_SELECTOR, '.btn')` | `.btn` |
| `driver.find_element(By.NAME, 'username')` | `[name=username]` |
| `driver.find_element(By.LINK_TEXT, 'Click')` | `"Click"` |
| `driver.find_element(By.XPATH, '//button')` | `xpath="//button"` |

**LumenQA Advantage:** No more `find_element()` calls! Just use the selector directly.

## Common Actions

### Navigation

| Action | Selenium | LumenQA |
|--------|----------|---------|
| Open URL | `driver.get('url')` | `navigate "url"` |
| Go back | `driver.back()` | `back` |
| Go forward | `driver.forward()` | `forward` |
| Refresh | `driver.refresh()` | `refresh` |
| Get current URL | `url = driver.current_url` | `get current_url => url` |

### Clicking

**Selenium:**
```python
element = driver.find_element(By.CSS_SELECTOR, '.button')
element.click()
```

**LumenQA:**
```pylux
click ".button"
```

### Typing Text

**Selenium:**
```python
element = driver.find_element(By.ID, 'email')
element.clear()
element.send_keys('user@test.com')
```

**LumenQA:**
```pylux
input #email => "user@test.com"
```

### Dropdowns

**Selenium:**
```python
from selenium.webdriver.support.ui import Select

select = Select(driver.find_element(By.ID, 'country'))
select.select_by_visible_text('United States')
```

**LumenQA:**
```pylux
select #country => "United States"
```

### Checkboxes

**Selenium:**
```python
checkbox = driver.find_element(By.ID, 'agree')
if not checkbox.is_selected():
    checkbox.click()
```

**LumenQA:**
```pylux
check "#agree"
```

## Waits Migration

This is where LumenQA really shines!

### Implicit Waits

**Selenium:**
```python
driver.implicitly_wait(10)
```

**LumenQA:**
```yaml
# lumen.yml
waits:
  implicit: 10s
```

But honestly, you probably don't need this. LumenQA waits intelligently by default!

### Explicit Waits

**Selenium:**
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.visibility_of_element_located((By.ID, 'result')))
```

**LumenQA:**
```pylux
# Usually not needed - automatic!
# But if you want explicit:
wait for element "#result" visible
```

### Common Wait Conditions

| Selenium EC | LumenQA |
|-------------|---------|
| `EC.visibility_of_element_located()` | `wait for element "..." visible` |
| `EC.element_to_be_clickable()` | Automatic! |
| `EC.presence_of_element_located()` | Automatic! |
| `EC.text_to_be_present_in_element()` | `wait until element "..." text = "..."` |
| `EC.url_contains()` | `wait until url contains "..."` |

### Sleeping (DON'T DO THIS!)

**Selenium:**
```python
import time
time.sleep(5)  # 😱 Bad practice!
```

**LumenQA:**
```pylux
# LumenQA waits intelligently - you rarely need this
# But if you must:
wait 5s
```

## Assertions

### Selenium (with unittest)
```python
self.assertIn('dashboard', driver.current_url)
self.assertEqual(element.text, 'Welcome')
self.assertTrue(element.is_displayed())
```

### LumenQA
```pylux
expect url contains "/dashboard"
expect element "h1" text = "Welcome"
expect element ".header" visible
```

## Page Object Pattern

### Selenium
```python
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_input = (By.ID, 'email')
        self.password_input = (By.ID, 'password')
        self.login_button = (By.CSS_SELECTOR, 'button.login')

    def login(self, email, password):
        self.driver.find_element(*self.email_input).send_keys(email)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

# Usage
page = LoginPage(driver)
page.login('user@test.com', 'password')
```

### LumenQA
```pylux
command login_page.login(email, password):
    input #email => email
    input #password => password
    click "Login"

# Usage
test "Login":
    navigate "/login"
    login_page.login("user@test.com", "password")
```

## Multiple Windows/Tabs

**Selenium:**
```python
# Open new tab
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get('https://example.com/new-page')

# Switch back
driver.switch_to.window(driver.window_handles[0])
```

**LumenQA:**
```pylux
# Open in new tab
new_tab navigate "https://example.com/new-page"

# Work in new tab automatically

# Switch back to main tab
switch_to tab 0
```

## JavaScript Execution

**Selenium:**
```python
driver.execute_script("window.scrollTo(0, 500)")
result = driver.execute_script("return document.title")
```

**LumenQA:**
```pylux
scroll by 500
get document_title => result
```

For custom JavaScript:
```pylux
execute_script "window.scrollTo(0, 500)"
```

## Screenshots

**Selenium:**
```python
driver.save_screenshot('screenshot.png')
```

**LumenQA:**
```pylux
screenshot "screenshot"
```

## Handling Alerts

**Selenium:**
```python
alert = driver.switch_to.alert
alert_text = alert.text
alert.accept()  # or alert.dismiss()
```

**LumenQA:**
```pylux
get alert.text => alert_text
accept alert  # or dismiss alert
```

## Test Structure Migration

### Selenium with unittest
```python
import unittest
from selenium import webdriver

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_successful_login(self):
        self.driver.get('https://example.com/login')
        # test code

    def test_failed_login(self):
        self.driver.get('https://example.com/login')
        # test code

if __name__ == '__main__':
    unittest.main()
```

### LumenQA
```pylux
# login_tests.lux

test "successful login":
    navigate "https://example.com/login"
    # test code

test "failed login":
    navigate "https://example.com/login"
    # test code
```

**No setup/teardown needed!** LumenQA handles browser lifecycle automatically.

## Running Tests

**Selenium:**
```bash
python -m pytest tests/
# or
python -m unittest discover tests/
```

**LumenQA:**
```bash
lumen run tests/
```

## Configuration

### Selenium
```python
# conftest.py or test setup
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)
```

### LumenQA
```yaml
# lumen.yml
browsers:
  - chrome
headless: true
```

## Parallel Execution

**Selenium (with pytest-xdist):**
```bash
pip install pytest-xdist
pytest -n 4  # 4 workers
```

**LumenQA:**
```bash
lumen run tests/ --parallel 4
```

Or configure once in `lumen.yml`:
```yaml
parallelization: 4
```

## Common Migration Patterns

### Pattern 1: Login Before Each Test

**Selenium:**
```python
class TestDashboard(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://example.com/login')
        self.driver.find_element(By.ID, 'email').send_keys('user@test.com')
        self.driver.find_element(By.ID, 'password').send_keys('password')
        self.driver.find_element(By.CSS_SELECTOR, 'button').click()

    def test_dashboard_loads(self):
        # test code
```

**LumenQA:**
```pylux
command login():
    navigate "/login"
    input #email => "user@test.com"
    input #password => "password"
    click "Login"

test "dashboard loads":
    login()
    # test code
```

### Pattern 2: Database Setup

**Selenium:**
```python
def setUp(self):
    # Create test data
    cursor.execute("INSERT INTO users ...")
    self.driver = webdriver.Chrome()
```

**LumenQA:**
```pylux
test "user management":
    # Setup via API (faster than DB)
    api POST "/api/users" {name: "Test User"} => response
    set user_id = response.body.id

    # Test UI
    navigate f"/users/{user_id}"
    expect text "Test User"

    # Cleanup
    api DELETE f"/api/users/{user_id}"
```

### Pattern 3: Dynamic Waits

**Selenium:**
```python
def wait_for_ajax():
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return jQuery.active == 0")
    )
```

**LumenQA:**
```pylux
# Usually automatic, but if needed:
wait until execute_script("return jQuery.active") = 0
```

## CI/CD Migration

### Jenkins (Selenium)
```groovy
stage('Test') {
    steps {
        sh 'pip install selenium'
        sh 'python -m pytest tests/'
    }
}
```

### Jenkins (LumenQA)
```groovy
stage('Test') {
    steps {
        sh 'pip install lumenqa'
        sh 'lumen run tests/'
    }
}
```

## Performance Comparison

| Metric | Selenium | LumenQA | Improvement |
|--------|----------|---------|-------------|
| Test suite (100 tests) | 261.4s | 18.4s | **14.2x faster** |
| Memory usage | 680MB | 142MB | **79% less** |
| Flakiness rate | 18.7% | 0.8% | **96% reduction** |
| Setup time | 8.3s | 0.6s | **13.8x faster** |

## Troubleshooting

### "NoSuchElementException" in Selenium

**Selenium:** Add explicit waits everywhere

**LumenQA:** Already handled! But if you see issues:
```pylux
wait for element ".element" visible
```

### "StaleElementReferenceException"

**Selenium:** Re-find the element

**LumenQA:** Doesn't happen! Intent trees handle element staleness automatically.

### WebDriver version mismatches

**Selenium:** Download correct chromedriver version

**LumenQA:** Never an issue. LumenVM manages everything.

## Migration Checklist

- [ ] Install LumenQA (`pip install lumenqa`)
- [ ] Run converter (`lumen convert --from selenium tests/`)
- [ ] Remove WebDriver initialization code
- [ ] Remove explicit waits (LumenQA handles it)
- [ ] Simplify assertions
- [ ] Update CI/CD pipelines
- [ ] Update documentation
- [ ] Remove `time.sleep()` calls (please!)
- [ ] Train team on PyLux
- [ ] Enjoy 14.2x faster tests! 🎉

## Next Steps

- **[Quick Start Guide](../quickstart.md)** - Get started with LumenQA
- **[PyLux Syntax](../pylux-syntax.md)** - Learn the language
- **[Best Practices](../guides/best-practices.md)** - Write better tests

## Need Help?

- **[Discord](https://discord.gg/lumenqa)** - Community support
- **[Email](mailto:migration@lumenqa.dev)** - Professional migration help

---

**Welcome to the future of test automation!** No more WebDriver headaches. 🚀
