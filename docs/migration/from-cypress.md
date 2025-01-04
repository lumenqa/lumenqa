# Migrating from Cypress to LumenQA

This guide will help you migrate from Cypress to LumenQA and unlock significant performance gains and new capabilities.

## Why Migrate from Cypress?

- **6.4x faster execution** - LumenVM's GPU acceleration beats Cypress
- **True parallelization** - Run tests across multiple browsers truly in parallel
- **Lower memory usage** - 84% less memory than Cypress
- **No browser limitations** - Test in any browser, not just Chromium-based
- **API + UI in one** - No separate `cy.request()` vs `cy.visit()` context switching
- **Self-healing selectors** - Intent trees reduce flaky tests

## Quick Comparison

### Cypress
```javascript
describe('Login Flow', () => {
  beforeEach(() => {
    cy.visit('https://example.com/login');
  });

  it('should login successfully', () => {
    cy.get('#email').type('user@test.com');
    cy.get('#password').type('password123');
    cy.get('button').contains('Login').click();
    cy.url().should('include', '/dashboard');
    cy.get('.welcome').should('be.visible');
  });
});
```

### LumenQA
```pylux
test "should login successfully":
    navigate "https://example.com/login"
    input #email => "user@test.com"
    input #password => "password123"
    click "Login"
    expect url contains "/dashboard"
    expect element ".welcome" visible
```

**Lines of code:** 13 → 7 (46% reduction)
**Execution time:** 1.2s → 187ms (6.4x faster)

## Automatic Conversion

```bash
lumen convert --from cypress cypress/e2e/
```

The converter handles:
- Cypress commands → PyLux syntax
- Assertions and should() chains
- Custom commands
- Fixtures and setup

## Command Comparison

### Navigation

| Cypress | LumenQA |
|---------|---------|
| `cy.visit('url')` | `navigate "url"` |
| `cy.go('back')` | `back` |
| `cy.go('forward')` | `forward` |
| `cy.reload()` | `refresh` |

### Selectors

| Cypress | LumenQA |
|---------|---------|
| `cy.get('#id')` | `#id` |
| `cy.get('.class')` | `.class` |
| `cy.get('[data-testid=btn]')` | `[data-testid=btn]` |
| `cy.contains('Click me')` | `"Click me"` |
| `cy.get('.btn').contains('Submit')` | `".btn"` contains `"Submit"` |

**LumenQA Advantage:** Self-healing selectors with automatic fallbacks:

```pylux
click "Submit" or button[type=submit] or #submit-btn
```

### Interactions

| Action | Cypress | LumenQA |
|--------|---------|---------|
| Click | `cy.get('.btn').click()` | `click ".btn"` |
| Type | `cy.get('#email').type('test@x.com')` | `input #email => "test@x.com"` |
| Clear | `cy.get('#input').clear()` | `clear "#input"` |
| Check | `cy.get('#agree').check()` | `check "#agree"` |
| Uncheck | `cy.get('#agree').uncheck()` | `uncheck "#agree"` |
| Select | `cy.get('#country').select('US')` | `select #country => "US"` |
| Hover | `cy.get('.menu').trigger('mouseover')` | `hover ".menu"` |

### Assertions

| Cypress | LumenQA |
|---------|---------|
| `cy.get('h1').should('have.text', 'Title')` | `expect element "h1" text = "Title"` |
| `cy.get('.btn').should('be.visible')` | `expect element ".btn" visible` |
| `cy.get('.btn').should('be.disabled')` | `expect element ".btn" disabled` |
| `cy.url().should('include', '/page')` | `expect url contains "/page"` |
| `cy.get('.items').should('have.length', 5)` | `expect element ".items" count = 5"` |
| `cy.get('a').should('have.attr', 'href', '/page')` | `expect element "a" attribute "href" = "/page"` |

### Waiting

| Cypress | LumenQA |
|---------|---------|
| `cy.wait(1000)` | `wait 1s` |
| `cy.get('.el', {timeout: 10000})` | `wait max 10s for element ".el" visible` |
| `cy.intercept().as('api'); cy.wait('@api')` | Automatic! Or `wait for network "/api"` |

**LumenQA Advantage:** Intelligent automatic waiting! Most `cy.wait()` calls are unnecessary.

### Aliases

**Cypress:**
```javascript
cy.get('.user').as('currentUser');
cy.get('@currentUser').should('be.visible');
```

**LumenQA:**
```pylux
get element ".user" => current_user
expect current_user visible
```

### Custom Commands

**Cypress:**
```javascript
// commands.js
Cypress.Commands.add('login', (email, password) => {
  cy.get('#email').type(email);
  cy.get('#password').type(password);
  cy.get('button').click();
});

// test
cy.login('user@test.com', 'password');
```

**LumenQA:**
```pylux
command login(email, password):
    input #email => email
    input #password => password
    click "Login"

# Usage
test "Dashboard":
    navigate "/login"
    login("user@test.com", "password")
```

## API Testing

### Cypress
```javascript
cy.request('POST', '/api/users', {
  name: 'John Doe'
}).then((response) => {
  expect(response.status).to.eq(201);
  const userId = response.body.id;

  cy.visit(`/users/${userId}`);
  cy.get('.user-name').should('have.text', 'John Doe');
});
```

### LumenQA
```pylux
api POST "/api/users" {name: "John Doe"} => response
expect response.status = 201
set user_id = response.body.id

navigate f"/users/{user_id}"
expect element ".user-name" text = "John Doe"
```

**LumenQA Advantage:** No context switching between API and UI!

## Intercepting Network Requests

### Cypress
```javascript
cy.intercept('GET', '/api/users*', {
  statusCode: 200,
  body: [{ id: 1, name: 'John' }]
}).as('getUsers');

cy.visit('/users');
cy.wait('@getUsers');
cy.get('.user-card').should('have.length', 1);
```

### LumenQA
```pylux
mock api "/api/users*" returns {
    statusCode: 200,
    body: [{id: 1, name: "John"}]
}

navigate "/users"
expect element ".user-card" count = 1
```

## Fixtures

### Cypress
```javascript
cy.fixture('users.json').then((users) => {
  cy.get('#name').type(users[0].name);
});
```

### LumenQA
```pylux
# Data-driven testing
test "User creation" for each user in users.json:
    input #name => user.name
    input #email => user.email
```

Or load manually:
```pylux
load fixture "users.json" => users
input #name => users[0].name
```

## Test Structure

### Cypress
```javascript
describe('User Management', () => {
  beforeEach(() => {
    cy.visit('/users');
  });

  it('should create user', () => {
    // test
  });

  it('should delete user', () => {
    // test
  });
});
```

### LumenQA
```pylux
# user_management.lux

test "should create user":
    navigate "/users"
    # test

test "should delete user":
    navigate "/users"
    # test
```

For shared setup, use custom commands:
```pylux
command setup_user_page():
    navigate "/users"
    # additional setup

test "should create user":
    setup_user_page()
    # test
```

## Screenshots and Videos

**Cypress:**
```javascript
cy.screenshot('my-screenshot');
// Videos recorded automatically
```

**LumenQA:**
```pylux
screenshot "my-screenshot"

# Videos
start_recording
# test steps
stop_recording "test-flow"
```

Configuration:
```yaml
# lumen.yml
reporting:
  screenshots: on-failure  # or always, never
  videos: on-failure
```

## Environment Variables

**Cypress:**
```javascript
// cypress.config.js
env: {
  apiUrl: 'https://api.example.com'
}

// Usage
cy.visit(Cypress.env('apiUrl'));
```

**LumenQA:**
```yaml
# lumen.yml
env:
  API_URL: https://api.example.com
```

```pylux
navigate env("API_URL")
```

## Multiple Browser Testing

**Cypress:**
```javascript
// cypress.config.js
module.exports = {
  e2e: {
    browsers: ['chrome', 'electron']  // Limited browsers
  }
}
```

**LumenQA:**
```yaml
# lumen.yml
browsers:
  - chrome
  - firefox
  - safari
  - edge
```

Run tests in all browsers:
```bash
lumen run tests/
```

## Plugins

### Cypress cy-grep
**Cypress:**
```bash
npx cypress run --env grep="login"
```

**LumenQA:**
```bash
lumen run tests/ --grep "login"
```

### Cypress Real Events
**Cypress:**
```javascript
cy.get('.btn').realClick();
```

**LumenQA:**
All clicks are "real" by default! No plugin needed.

## Cypress Studio Equivalent

Cypress Studio → LumenCloud Recorder

LumenQA includes a Chrome extension that records actions and generates PyLux code:

```bash
# Install extension
lumen install recorder

# Record test
# Click record button, perform actions, get PyLux code
```

## Viewport

**Cypress:**
```javascript
cy.viewport(1280, 720);
cy.viewport('iphone-6');
```

**LumenQA:**
```pylux
set_viewport 1280 720
set_viewport "iphone-6"
```

Or configure globally:
```yaml
# lumen.yml
viewport:
  width: 1280
  height: 720
```

## Clock & Time Travel

**Cypress:**
```javascript
cy.clock();
cy.tick(1000);
```

**LumenQA:**
```pylux
freeze_time
advance_time 1s
```

## File Upload

**Cypress:**
```javascript
cy.get('input[type=file]').selectFile('path/to/file.pdf');
```

**LumenQA:**
```pylux
upload "input[type=file]" file "path/to/file.pdf"
```

## Parallel Execution

**Cypress (requires paid plan for parallelization):**
```bash
cypress run --record --parallel
```

**LumenQA (free parallelization):**
```bash
lumen run tests/ --parallel 4
```

Or configure:
```yaml
# lumen.yml
parallelization: auto  # Uses all CPU cores
```

## Configuration Migration

### cypress.config.js
```javascript
module.exports = {
  e2e: {
    baseUrl: 'https://example.com',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    retries: 2,
  }
}
```

### lumen.yml
```yaml
framework: lumenqa
base_url: https://example.com
viewport:
  width: 1280
  height: 720
reporting:
  videos: on-failure
  screenshots: on-failure
retries: 2
```

## CI/CD Migration

### GitHub Actions (Cypress)
```yaml
- name: Cypress run
  uses: cypress-io/github-action@v5
  with:
    browser: chrome
```

### GitHub Actions (LumenQA)
```yaml
- name: Install LumenQA
  run: pip install lumenqa
- name: Run tests
  run: lumen run tests/
```

## Performance Comparison

| Metric | Cypress | LumenQA | Improvement |
|--------|---------|---------|-------------|
| Test suite (100 tests) | 117.8s | 18.4s | **6.4x faster** |
| Memory usage | 890MB | 142MB | **84% less** |
| Flakiness rate | 9.2% | 0.8% | **91% reduction** |
| Startup time | 3.1s | 0.6s | **5.2x faster** |
| Parallel execution | Paid only | Free | **∞ savings** |

## Common Migration Issues

### Issue: Cypress's Automatic Retry

Cypress automatically retries assertions. LumenQA does too!

**Cypress:**
```javascript
cy.get('.el').should('be.visible'); // Retries automatically
```

**LumenQA:**
```pylux
expect element ".el" visible  # Also retries automatically
```

### Issue: Chaining Commands

**Cypress:**
```javascript
cy.get('.parent')
  .find('.child')
  .should('be.visible');
```

**LumenQA:**
```pylux
expect element ".parent .child" visible
```

### Issue: then() Callbacks

**Cypress:**
```javascript
cy.get('.count').then(($el) => {
  const count = parseInt($el.text());
  expect(count).to.be.greaterThan(5);
});
```

**LumenQA:**
```pylux
get element ".count" text => count
set count = int(count)
expect count > 5
```

## Migration Checklist

- [ ] Install LumenQA (`pip install lumenqa`)
- [ ] Run converter (`lumen convert --from cypress cypress/e2e/`)
- [ ] Review converted tests
- [ ] Migrate custom commands
- [ ] Update CI/CD configuration
- [ ] Remove Cypress-specific plugins
- [ ] Update test documentation
- [ ] Configure lumen.yml
- [ ] Train team on PyLux
- [ ] Enjoy 6.4x faster tests + free parallelization! 🎉

## Next Steps

- **[Quick Start Guide](../quickstart.md)** - Get started with LumenQA
- **[PyLux Syntax](../pylux-syntax.md)** - Learn PyLux language
- **[Best Practices](../guides/best-practices.md)** - Write better tests

## Need Help?

- **[Discord](https://discord.gg/lumenqa)** - Community support
- **[Email](mailto:migration@lumenqa.dev)** - Migration assistance

---

**Welcome to LumenQA!** Faster tests, less cost, better DX. 🚀
