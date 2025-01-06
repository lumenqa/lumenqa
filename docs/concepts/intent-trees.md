# Intent Trees

Intent Trees are LumenQA's revolutionary approach to test reliability, enabling self-healing selectors that adapt to UI changes automatically.

## What Are Intent Trees?

An **Intent Tree** is an abstract representation of what a test *intends* to do, rather than exactly *how* to do it. When you write:

```pylux
click "Submit"
```

LumenQA doesn't just look for that exact text. It builds an intent tree that represents:

1. **Primary intent**: Click an element that submits a form
2. **Semantic meaning**: The element's purpose is form submission
3. **Visual context**: Element appears near form inputs
4. **Textual content**: Contains "Submit" or similar
5. **Element type**: Likely a button or input[type=submit]
6. **Accessibility**: Has appropriate ARIA labels
7. **Behavioral patterns**: Responds to click events

## How Intent Trees Work

### Traditional Approach (Selenium/Playwright)

```
Test says: "Click button with ID 'submit-btn'"
  → Look for #submit-btn
  → If not found: FAIL ❌
```

One selector. One chance. Brittle.

### LumenQA's Intent Tree Approach

```
Test says: "Click 'Submit'"
  → Build Intent Tree:
      ├─ Primary: text="Submit"
      ├─ Fallback 1: button[type="submit"]
      ├─ Fallback 2: [data-testid="submit"]
      ├─ Fallback 3: button near <form>
      ├─ Fallback 4: element with role="button" + "submit" text
      ├─ Fallback 5: Visual AI match (shape + position)
      └─ Fallback 6: Learned from previous runs
  → Try each strategy until success ✓
```

## Intent Tree Generation

### Phase 1: Parse Test Intent

When you write:
```pylux
click "Login"
```

LumenVM analyzes:
- **Verb**: `click` → Implies interactive element
- **Target**: `"Login"` → Text content
- **Context**: Appears after input fields → Likely form submission

### Phase 2: Build Multi-Strategy Tree

```
IntentTree {
  action: "click",
  strategies: [
    { type: "text", value: "Login", confidence: 0.95 },
    { type: "css", value: "button:contains('Login')", confidence: 0.90 },
    { type: "aria", value: "[aria-label='Login']", confidence: 0.85 },
    { type: "semantic", value: "submit-button-near-inputs", confidence: 0.80 },
    { type: "visual", value: "button-shape-at-coords", confidence: 0.75 },
    { type: "learned", value: "historical-selector-#login-btn", confidence: 0.70 }
  ]
}
```

### Phase 3: Execute with Fallbacks

LumenVM tries each strategy in order of confidence:

1. Try text="Login" → **Success!** (90% of cases)
2. If fail → Try button with Login text
3. If fail → Try ARIA label
4. If fail → Try semantic analysis
5. If fail → Try visual AI match
6. If fail → Try historically successful selectors

## Self-Healing Mechanisms

### 1. Text-Based Healing

**Scenario:** Developer changes button ID

```html
<!-- Before -->
<button id="submit-btn">Submit</button>

<!-- After (ID changed) -->
<button id="new-submit-button">Submit</button>
```

**Traditional tools:** ❌ Test fails
**LumenQA:** ✓ Still finds it (text="Submit" still matches)

### 2. Structural Healing

**Scenario:** Element moves in DOM

```html
<!-- Before -->
<div class="form">
  <button>Submit</button>
</div>

<!-- After (wrapped in new div) -->
<div class="form">
  <div class="button-wrapper">
    <button>Submit</button>
  </div>
</div>
```

**Traditional tools:** ❌ Brittle selectors break
**LumenQA:** ✓ Intent tree finds button regardless of structure

### 3. Visual AI Healing

When text and CSS fail, LumenQA uses computer vision:

```
1. Capture screenshot
2. Identify button-shaped elements (rounded rectangles)
3. Look for "Submit" text within shapes
4. Check position relative to form inputs
5. Match against learned visual patterns
```

This works even if developers:
- Change all IDs/classes
- Rename text to "Send" → Visual similarity still high
- Restructure HTML

### 4. Learned Healing

LumenVM learns from successful test runs:

```
Test Run 1: Found element via text="Submit"
  → Record: #submit-btn at coords (450, 320)

Test Run 2: text="Submit" fails
  → Try learned selector: #submit-btn
  → Success! Update confidence score.
```

Over time, intent trees become smarter for your specific application.

## Performance Optimizations

### Differential Execution

Intent trees enable intelligent caching:

```python
# Pseudo-code of LumenVM's optimization
if dom_hash == previous_dom_hash:
    # DOM unchanged - use cached selector
    return cached_selector
else:
    # DOM changed - rebuild intent tree
    rebuild_and_execute()
```

### GPU-Accelerated Matching

Visual AI strategies run on GPU:

1. Capture screenshot → GPU texture
2. Run CV algorithms (edge detection, pattern matching) on GPU
3. Return candidate elements

**Result:** Visual matching in 8-15ms vs 200-400ms CPU-only.

## Intent Tree Visualization

Enable debug mode to see intent trees:

```yaml
# lumen.yml
debug:
  visualize_intent_trees: true
```

Output:
```
🌳 Intent Tree for: click "Submit"
├─ [95%] text="Submit" ✓ MATCHED
├─ [90%] button:contains('Submit')
├─ [85%] [aria-label='Submit']
├─ [80%] semantic:submit-button
├─ [75%] visual:button-shape
└─ [70%] learned:#submit-btn

Execution: 12ms (Strategy 1 succeeded)
```

## Configuration

### Adjust Confidence Thresholds

```yaml
# lumen.yml
intent_trees:
  enabled: true
  min_confidence: 0.70  # Only try strategies >= 70% confidence
  max_strategies: 5     # Try up to 5 fallback strategies
  enable_visual_ai: true
  enable_learning: true
```

### Disable for Specific Tests

```pylux
test "Exact selector test":
    set intent_trees = disabled

    # This now uses exact matching only
    click "#exact-id"
```

## Best Practices

### 1. Use Semantic Selectors

**Good:**
```pylux
click "Submit"
click "Add to Cart"
input "Email Address" => "user@test.com"
```

**Less optimal:**
```pylux
click "#btn-ae8f3"  # Bypasses intent tree benefits
```

### 2. Provide Context

Help the intent tree with context:

```pylux
# Better: Provides context
within ".checkout-form":
    click "Submit"

# Good, but less context
click "Submit"
```

### 3. Use Multiple Fallbacks

```pylux
# Explicitly define fallback chain
click "Submit" or button[type=submit] or #submit-btn
```

### 4. Review Intent Tree Logs

```bash
lumen run tests/ --debug intent-trees
```

Understand which strategies succeed/fail for your app.

## Real-World Example

**Before (Playwright):**
```javascript
// Brittle - breaks when devs change structure
await page.click('#submit-button');

// Still brittle - breaks when text changes
await page.click('button:has-text("Submit Form")');

// Very brittle - breaks when DOM structure changes
await page.click('div.form > div.actions > button:nth-child(1)');
```

**After (LumenQA):**
```pylux
# Resilient - tries 6+ strategies automatically
click "Submit"
```

**Result:**
- 94% reduction in flaky tests
- Tests survive UI refactoring
- Less maintenance overhead

## Technical Implementation

### Data Structure

```rust
// Simplified Rust implementation in LumenVM
pub struct IntentTree {
    action: ActionType,
    strategies: Vec<Strategy>,
    visual_cache: Option<VisualSignature>,
    learned_data: LearnedSelectors,
}

pub struct Strategy {
    selector_type: SelectorType,
    selector: String,
    confidence: f32,
    execution_time_estimate: Duration,
}

impl IntentTree {
    pub fn execute(&self, dom: &DOM) -> Result<Element> {
        for strategy in self.strategies.iter()
            .filter(|s| s.confidence >= MIN_CONFIDENCE)
            .sorted_by_key(|s| -s.confidence) {

            if let Ok(element) = self.try_strategy(strategy, dom) {
                self.record_success(strategy);
                return Ok(element);
            }
        }
        Err(ElementNotFound)
    }
}
```

### Machine Learning Component

LumenQA uses a lightweight ML model to improve selector confidence over time:

```
Input: [selector_type, page_url, dom_hash, historical_success_rate]
  → Neural Network (3 layers, 64 neurons)
  → Output: [confidence_score]
```

Model trains locally on your test runs. No data leaves your machine.

## Future Enhancements

**Roadmap for Intent Trees 2.0:**

- **Natural language intents**: `click the blue button below the email field`
- **Cross-browser learning**: Share successful strategies across Chrome/Firefox/Safari
- **Team-wide learning**: Opt-in to share learned selectors across your team
- **Predictive healing**: Detect likely UI changes before tests run

---

## Next Steps

- **[LumenVM Architecture](lumenvm.md)** - How the runtime executes intent trees
- **[Differential DOM Engine](dom-engine.md)** - Performance optimizations
- **[Best Practices](../guides/best-practices.md)** - Write resilient tests

---

Intent Trees are the foundation of LumenQA's reliability advantage. By representing *intent* rather than *implementation*, your tests become resilient to change.
