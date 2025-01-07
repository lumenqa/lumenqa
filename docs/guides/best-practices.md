# Best Practices

Write maintainable, fast, and reliable tests with these LumenQA best practices.

## Test Design

### 1. Use Descriptive Test Names

**Good:**
```pylux
test "User can complete checkout with valid credit card"
test "Login fails when password is incorrect"
test "Dashboard displays recent activity for logged-in users"
```

**Bad:**
```pylux
test "Test 1"
test "Login test"
test "Check dashboard"
```

### 2. Keep Tests Independent

Each test should run in isolation:

```pylux
test "Create product":
    # Setup
    api POST "/api/products" {name: "Widget"}

    # Test
    navigate "/products"
    expect text "Widget"

    # Cleanup
    api DELETE "/api/products/widget"
```

### 3. Use Semantic Selectors

**Leverage self-healing selectors:**

```pylux
# Good - uses text, works across UI changes
click "Add to Cart"
input "Email Address" => "user@test.com"

# Less ideal - brittle CSS selectors
click "#btn-ae8f3"
input "[data-qa-id='email-input-2']" => "user@test.com"
```

## Performance

### 4. Enable Parallel Execution

```yaml
# lumen.yml
parallelization: auto
```

### 5. Use API for Setup/Teardown

**Slow:**
```pylux
test "Edit user profile":
    # Slow - creates user via UI
    navigate "/signup"
    # ... 20 lines of form filling ...
```

**Fast:**
```pylux
test "Edit user profile":
    # Fast - creates user via API
    api POST "/api/users" {name: "Test", email: "test@ex.com"} => user

    navigate f"/users/{user.body.id}/edit"
    # ... test actual edit functionality ...
```

### 6. Minimize Waits

Let LumenQA wait automatically:

```pylux
# Good - automatic intelligent waiting
click ".submit"
expect text "Success"

# Unnecessary
click ".submit"
wait 2s  # Don't do this!
expect text "Success"
```

## Reliability

### 7. Leverage Intent Trees

```pylux
# Self-healing with fallbacks
click "Submit" or button[type=submit] or #submit-btn
```

### 8. Use Retry Configuration

```yaml
# lumen.yml
retries: 2  # Retry failed tests
```

### 9. Avoid Fixed Delays

```pylux
# Bad
wait 5s

# Good - wait for condition
wait for element ".data" visible
wait until element ".counter" text = "100"
```

## Organization

### 10. Use Custom Commands for Reusable Logic

```pylux
# Define once
command login_as(email):
    navigate "/login"
    input #email => email
    input #password => secret("PASSWORD")
    click "Login"
    wait for url contains "/dashboard"

# Use everywhere
test "View profile":
    login_as("user@test.com")
    navigate "/profile"
    # ...
```

### 11. Group Related Tests

```
tests/
├── auth/
│   ├── login.lux
│   ├── signup.lux
│   └── password-reset.lux
├── products/
│   ├── create.lux
│   ├── edit.lux
│   └── delete.lux
└── checkout/
    ├── cart.lux
    └── payment.lux
```

## Assertions

### 12. Make Assertions Specific

```pylux
# Good - specific
expect element ".success-message" text = "Order #12345 confirmed"

# Bad - vague
expect text "confirmed"
```

### 13. Verify State, Not Just Presence

```pylux
# Good
expect element "#submit" enabled
expect element ".item" count = 5

# Incomplete
expect element "#submit" visible
```

## Security

### 14. Use Secrets for Sensitive Data

```pylux
# Good
input #password => secret("PASSWORD")
api POST "/login" {password: secret("API_KEY")}

# Bad - credentials visible in logs
input #password => "supersecret123"
```

### 15. Clean Up Test Data

```pylux
test "User management":
    api POST "/api/users" {name: "Test"} => user

    # ... test code ...

    # Always cleanup
    api DELETE f"/api/users/{user.body.id}"
```

## Debugging

### 16. Use Screenshots on Failure

```yaml
# lumen.yml
reporting:
  screenshots: on-failure
  videos: on-failure
```

### 17. Enable Debug Mode When Needed

```bash
lumen run tests/ --debug intent-trees
lumen run tests/ --debug dom-cache
```

## CI/CD

### 18. Cache Dependencies

```yaml
# .github/workflows/test.yml
- uses: actions/cache@v3
  with:
    path: ~/.lumen
    key: lumen-${{ hashFiles('lumen.yml') }}
```

### 19. Run Critical Tests First

```bash
# Run smoke tests first
lumen run tests/smoke/ --fail-fast

# Then full suite
lumen run tests/
```

## Antipatterns to Avoid

### ❌ Sleeping Instead of Waiting

```pylux
# Bad
click ".load-data"
wait 3s
expect element ".data" visible

# Good
click ".load-data"
wait for element ".data" visible
```

### ❌ Overly Specific Selectors

```pylux
# Bad - breaks easily
click "div.container > div.row:nth-child(3) > button.btn"

# Good - resilient
click "Submit" or button[type=submit]
```

### ❌ Testing Implementation Details

```pylux
# Bad - testing CSS classes (implementation)
expect element ".flex.justify-center.p-4" visible

# Good - testing user-visible behavior
expect text "Welcome Dashboard"
```

### ❌ Huge Monolithic Tests

```pylux
# Bad - 200 line test that does everything
test "Complete user journey":
    # signup
    # ... 50 lines ...
    # create profile
    # ... 50 lines ...
    # make purchase
    # ... 50 lines ...

# Good - split into focused tests
test "User signup"
test "Create profile"
test "Make purchase"
```

---

## Quick Reference

✅ **DO:**
- Use descriptive names
- Keep tests independent
- Leverage self-healing selectors
- Use API for setup
- Enable parallelization
- Use custom commands
- Screenshot on failure

❌ **DON'T:**
- Use fixed waits
- Hardcode credentials
- Test implementation details
- Create monolithic tests
- Use overly-specific selectors
- Forget cleanup

---

Follow these practices and your test suite will be fast, reliable, and maintainable!
