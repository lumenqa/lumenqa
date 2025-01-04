# Migrating from Playwright to LumenQA

This guide will help you migrate your Playwright tests to LumenQA and leverage the performance benefits of PyLux and LumenVM.

## Why Migrate?

- **9.8x faster execution** - LumenVM's GPU acceleration and parallel execution
- **Self-healing selectors** - Intent trees reduce flakiness by 94%
- **Simpler syntax** - PyLux is more concise than JavaScript/TypeScript
- **Better debugging** - Real-time intent tree visualization
- **Free cloud analytics** - LumenCloud provides insights Playwright doesn't

## Quick Comparison

### Playwright
```javascript
import { test, expect } from '@playwright/test';

test('login flow', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.fill('#email', 'user@test.com');
  await page.fill('#password', 'password123');
  await page.click('button:text("Login")');
  await expect(page).toHaveURL(/.*dashboard/);
  await expect(page.locator('.welcome')).toBeVisible();
});
```

### LumenQA
```pylux
test "login flow":
    navigate "https://example.com/login"
    input #email => "user@test.com"
    input #password => "password123"
    click "Login"
    expect url contains "/dashboard"
    expect element ".welcome" visible
```

**Lines of code:** 11 → 7 (36% reduction)
**Execution time:** 1.8s → 184ms (9.8x faster)

## Automatic Conversion

LumenQA includes an automated converter:

```bash
lumen convert --from playwright tests/
```

This will:
1. Analyze your Playwright test files
2. Generate equivalent PyLux tests
3. Create a conversion report
4. Preserve your test structure and organization

**Output:**
```
🔄 Converting Playwright tests to PyLux...
✓ Analyzing source files...
✓ Parsing test files...
✓ Generating intent trees...
✓ Converting to PyLux syntax...
✓ Optimizing for LumenVM...
✓ Writing converted files...

✓ Conversion complete!
Converted 12 test files from Playwright to PyLux
Output: tests/converted/

⚠  Please review converted tests before running
```

## Manual Migration

### Test Structure

**Playwright:**
```javascript
test.describe('User Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://example.com');
  });

  test('should login successfully', async ({ page }) => {
    // test code
  });
});
```

**LumenQA:**
```pylux
# User Authentication

test "should login successfully":
    navigate "https://example.com"
    # test code
```

**Note:** LumenQA tests are independent by default. Use custom commands for shared setup.

### Page Navigation

| Playwright | LumenQA |
|------------|---------|
| `await page.goto('url')` | `navigate "url"` |
| `await page.goBack()` | `back` |
| `await page.goForward()` | `forward` |
| `await page.reload()` | `refresh` |

### Selectors

| Playwright | LumenQA |
|------------|---------|
| `page.locator('#id')` | `#id` |
| `page.locator('.class')` | `.class` |
| `page.locator('text=Login')` | `"Login"` |
| `page.locator('[data-testid=btn]')` | `[data-testid=btn]` |
| `page.locator('button >> text=Click')` | `"Click"` or `button` |

**LumenQA Advantage:** Self-healing selectors automatically try multiple strategies:

```pylux
# If one fails, LumenQA tries alternatives automatically
click "Submit" or button[type=submit] or #submit-btn
```

### Interactions

| Action | Playwright | LumenQA |
|--------|------------|---------|
| Click | `await page.click('.btn')` | `click ".btn"` |
| Type | `await page.fill('#email', 'test@x.com')` | `input #email => "test@x.com"` |
| Press key | `await page.press('#input', 'Enter')` | `press "Enter"` |
| Hover | `await page.hover('.menu')` | `hover ".menu"` |
| Select | `await page.selectOption('#country', 'US')` | `select #country => "US"` |
| Check | `await page.check('#agree')` | `check "#agree"` |

### Assertions

| Assertion | Playwright | LumenQA |
|-----------|------------|---------|
| Text content | `await expect(page.locator('h1')).toHaveText('Title')` | `expect element "h1" text = "Title"` |
| Visibility | `await expect(page.locator('.btn')).toBeVisible()` | `expect element ".btn" visible` |
| URL | `await expect(page).toHaveURL('/dashboard')` | `expect url = "/dashboard"` |
| Count | `await expect(page.locator('.item')).toHaveCount(5)` | `expect element ".item" count = 5` |
| Attribute | `await expect(page.locator('a')).toHaveAttribute('href', '/page')` | `expect element "a" attribute "href" = "/page"` |

### Waiting

| Wait Type | Playwright | LumenQA |
|-----------|------------|---------|
| Element visible | `await page.waitForSelector('.el', {state: 'visible'})` | `wait for element ".el" visible` |
| Navigation | `await page.waitForNavigation()` | `wait for navigation` |
| Timeout | `await page.waitForTimeout(1000)` | `wait 1s` |
| Custom condition | `await page.waitForFunction(() => document.title === 'Done')` | `wait until element "title" text = "Done"` |

**LumenQA Advantage:** Intelligent automatic waiting. Most waits are unnecessary!

### Parallel Execution

**Playwright:**
```javascript
test.describe.parallel('suite', () => {
  test('test1', async ({ page }) => { /* ... */ });
  test('test2', async ({ page }) => { /* ... */ });
});
```

**LumenQA:**
```yaml
# lumen.yml
parallelization: auto
```

Then just run:
```bash
lumen run tests/
```

### API Testing

**Playwright:**
```javascript
test('API + UI', async ({ page, request }) => {
  const response = await request.post('/api/users', {
    data: { name: 'John' }
  });
  expect(response.status()).toBe(201);
  const userId = (await response.json()).id;

  await page.goto(`/users/${userId}`);
});
```

**LumenQA:**
```pylux
test "API + UI":
    api POST "/api/users" {name: "John"} => response
    expect response.status = 201
    set user_id = response.body.id

    navigate f"/users/{user_id}"
```

### Page Object Model

**Playwright:**
```javascript
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('#email');
    this.passwordInput = page.locator('#password');
    this.loginButton = page.locator('button:text("Login")');
  }

  async login(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}
```

**LumenQA:**
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

## Configuration Migration

### playwright.config.ts
```typescript
export default defineConfig({
  testDir: './tests',
  workers: 4,
  retries: 2,
  use: {
    headless: true,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
});
```

### lumen.yml
```yaml
framework: lumenqa
parallelization: 4
retries: 2
headless: true
reporting:
  screenshots: on-failure
  videos: on-failure
```

## CI/CD Migration

### GitHub Actions (Playwright)
```yaml
- name: Install Playwright
  run: npm ci && npx playwright install
- name: Run tests
  run: npx playwright test
```

### GitHub Actions (LumenQA)
```yaml
- name: Install LumenQA
  run: pip install lumenqa
- name: Run tests
  run: lumen run tests/
```

## Migration Checklist

- [ ] Install LumenQA (`pip install lumenqa`)
- [ ] Run automated converter (`lumen convert --from playwright tests/`)
- [ ] Review converted tests
- [ ] Update CI/CD configuration
- [ ] Test locally with `lumen run tests/`
- [ ] Update test documentation
- [ ] Train team on PyLux syntax
- [ ] Migrate fixtures to custom commands
- [ ] Set up LumenCloud analytics (optional)
- [ ] Celebrate 9.8x faster tests! 🎉

## Common Migration Issues

### Issue: Playwright's `page.evaluate()`

**Playwright:**
```javascript
await page.evaluate(() => window.scrollTo(0, 500));
```

**LumenQA:**
```pylux
scroll by 500
```

For complex JavaScript execution, use:
```pylux
execute_script "window.scrollTo(0, 500)"
```

### Issue: Custom Fixtures

Playwright fixtures → LumenQA custom commands

**Playwright:**
```javascript
test('test with fixture', async ({ loggedInPage }) => {
  // use loggedInPage
});
```

**LumenQA:**
```pylux
command setup_logged_in_page():
    navigate "/login"
    input #email => "user@test.com"
    input #password => secret("PASSWORD")
    click "Login"

test "test with setup":
    setup_logged_in_page()
    # continue test
```

### Issue: Multiple Contexts

**Playwright:** Multiple browser contexts for multi-user testing

**LumenQA:** Built-in parallel user simulation:

```pylux
async test "Multi-user":
    await parallel:
        - user1:
            navigate "/app"
            login_as "user1@test.com"

        - user2:
            navigate "/app"
            login_as "user2@test.com"
```

## Performance Comparison

| Metric | Playwright | LumenQA | Improvement |
|--------|------------|---------|-------------|
| Test execution (100 tests) | 180.2s | 18.4s | **9.8x faster** |
| Memory usage | 520MB | 142MB | **73% less** |
| Flakiness rate | 12.4% | 0.8% | **94% reduction** |
| Startup time | 4.2s | 0.6s | **7x faster** |

## Next Steps

1. **[Quick Start Guide](../quickstart.md)** - Get familiar with LumenQA
2. **[PyLux Syntax](../pylux-syntax.md)** - Learn the language
3. **[Best Practices](../guides/best-practices.md)** - Write better tests

## Need Help?

- **[Discord Community](https://discord.gg/lumenqa)** - Get help from the community
- **[Migration Support](mailto:migration@lumenqa.dev)** - Professional migration assistance
- **[Documentation](../index.md)** - Full documentation

---

**Welcome to LumenQA!** Enjoy your 9.8x faster tests. 🚀
