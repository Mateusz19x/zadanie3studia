# Workflow: Documentation Generation Agent

Detailed workflow for the autonomous documentation generator agent.

---

## Trigger Event

User request:
```
Generate API documentation for mailer.subscribers module
```

---

## Phase 1: Analysis (10-15 seconds)

### Step 1.1: Code Reading
1. Read `subscribers.py`
2. Identify all classes and functions
3. Extract class hierarchy and relationships
4. Note module-level variables and constants

### Step 1.2: Structure Analysis
1. Analyze class structure:
   - Subscriber (dataclass)
   - SubscriberManager (main class)
2. Extract public methods
3. Identify private/internal methods
4. Map dependencies

### Step 1.3: Documentation Extraction
1. Extract docstrings (Google format)
2. Parse type hints
3. Gather parameter information
4. Collect return type information
5. Identify raised exceptions

### Output
```
Module Structure:
- Subscriber (dataclass)
  - email: str
  - name: str
  - subscribed: bool = True
  
- SubscriberManager (class)
  - Methods: add_subscriber, remove_subscriber, get_all_subscribers, etc.
```

---

## Phase 2: Context Gathering (5-10 seconds)

### Step 2.1: Test Analysis
1. Read `test_subscribers.py`
2. Extract usage patterns from tests
3. Identify test cases:
   - Happy path scenarios
   - Error cases
   - Edge cases
4. Gather test fixtures

### Step 2.2: Dependency Analysis
1. Check imports
2. Identify external dependencies
3. Map internal dependencies
4. Note Flask integration points

### Step 2.3: Project Context
1. Read `README_IMPLEMENTATION.md`
2. Extract project goals
3. Gather design principles
4. Note architectural patterns

### Output
```
Usage Patterns:
- manager = SubscriberManager()
- manager.add_subscriber("john@example.com", "John")
- manager.get_all_subscribers()

Error Cases:
- ValueError on invalid email
- ValueError on duplicate
- Validation requirements
```

---

## Phase 3: Generation (10-20 seconds)

### Step 3.1: Structure Creation
Create documentation outline:
```
1. Module Overview
2. Classes
   2.1 Subscriber
   2.2 SubscriberManager
3. Functions
   3.1 Public API
   3.2 Private Helpers
4. Exceptions
5. Constants
```

### Step 3.2: Docstring Conversion
Convert Google-format docstrings to Markdown:

```python
# From:
def add_subscriber(self, email: str, name: str) -> bool:
    """Add a new subscriber.
    
    Args:
        email: Email address.
        name: Full name.
        
    Returns:
        True if added, False if already exists.
        
    Raises:
        ValueError: If email invalid.
    """

# To Markdown:
### `add_subscriber(email: str, name: str) -> bool`

Add a new subscriber.

**Parameters:**
- `email` (str): Email address
- `name` (str): Full name

**Returns:** bool - True if added, False if already exists

**Raises:** ValueError - If email invalid
```

### Step 3.3: Type Hints Integration
1. Show types in function signatures
2. Link to type definitions
3. Document return types
4. Note Optional types

### Step 3.4: API Reference Table
```markdown
| Method | Parameters | Returns | Raises |
|--------|-----------|---------|--------|
| add_subscriber | email, name | bool | ValueError |
| remove_subscriber | email | bool | - |
| get_subscriber | email | Subscriber\|None | - |
```

### Output
Formatted `api-reference.md` file with complete API documentation

---

## Phase 4: Examples Generation (15-30 seconds)

### Step 4.1: Basic Usage
```python
# Initialize manager
from mailer import SubscriberManager

manager = SubscriberManager()

# Add subscriber
manager.add_subscriber("john@example.com", "John Doe")

# Get all
subscribers = manager.get_all_subscribers()
print(f"Total: {len(subscribers)}")
```

### Step 4.2: Advanced Patterns
```python
# Get active subscribers only
active = manager.get_active_subscribers()

# Unsubscribe (soft delete)
manager.unsubscribe("john@example.com")

# Resubscribe
manager.resubscribe("john@example.com")

# Statistics
count = manager.get_active_subscriber_count()
```

### Step 4.3: Error Handling
```python
try:
    manager.add_subscriber("invalid-email", "User")
except ValueError as e:
    print(f"Error: {e}")

try:
    manager.add_subscriber("user@example.com", "")
except ValueError as e:
    print(f"Name required: {e}")
```

### Step 4.4: Complete Working Example
```python
"""Complete subscriber management workflow."""
from mailer import SubscriberManager

def main():
    manager = SubscriberManager()
    
    # Add subscribers
    emails = [
        ("alice@example.com", "Alice"),
        ("bob@example.com", "Bob"),
        ("charlie@example.com", "Charlie"),
    ]
    
    for email, name in emails:
        try:
            success = manager.add_subscriber(email, name)
            if success:
                print(f"✓ Added {name}")
        except ValueError as e:
            print(f"✗ Failed: {e}")
    
    # List all
    print(f"\nTotal subscribers: {manager.get_subscriber_count()}")
    
    # Unsubscribe one
    manager.unsubscribe("bob@example.com")
    print(f"Active: {manager.get_active_subscriber_count()}")
    
    # List active
    for sub in manager.get_active_subscribers():
        print(f"- {sub.name} ({sub.email})")

if __name__ == "__main__":
    main()
```

### Output
4-5 complete, tested, working examples

---

## Phase 5: Validation (5-10 seconds)

### Step 5.1: Markdown Validation
- [ ] Valid markdown syntax
- [ ] Proper heading hierarchy
- [ ] Code blocks properly formatted
- [ ] Tables formatted correctly

### Step 5.2: Completeness Check
- [ ] All public methods documented
- [ ] All parameters described
- [ ] All return types documented
- [ ] All exceptions listed
- [ ] Type hints included
- [ ] Examples provided

### Step 5.3: Code Example Testing
```bash
# Run examples to verify they work
pytest --doctest-modules docs/
```

### Step 5.4: Link Verification
- [ ] No broken internal links
- [ ] Cross-references valid
- [ ] Section anchors working

### Step 5.5: Content Review
- [ ] Technical accuracy
- [ ] Completeness of coverage
- [ ] Clarity and readability
- [ ] Consistency with project standards

### Output
Validation report:
```
✓ 15/15 methods documented
✓ 42/42 parameters described
✓ All examples tested
✓ Markdown valid
✓ Ready for publication
```

---

## Final Output Structure

```
docs/
├── api/
│   └── subscribers.md          # API reference
├── examples/
│   └── subscribers_usage.md    # Usage examples
├── guides/
│   └── subscriber_management.md # How-to guide
└── CHANGELOG.md               # Updated
```

---

## Success Criteria

- ✅ All public functions documented
- ✅ All parameters described with types
- ✅ Type hints shown in examples
- ✅ Minimum 5 complete examples provided
- ✅ All markdown syntax valid
- ✅ All code examples tested and working
- ✅ Generated within 60 seconds
- ✅ Ready for immediate publication

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing docstrings | Use code analysis to infer from implementation |
| Unclear type hints | Review test file for usage patterns |
| Broken examples | Test with actual code before documenting |
| Missing sections | Check project standards for required sections |

---

## Integration with CI/CD

```yaml
# GitHub Actions workflow
- name: Generate Docs
  run: |
    copilot run docs-generator-agent "Generate documentation"
    git add docs/
    git commit -m "Docs: auto-generated documentation"
```

---

**Agent Version**: 1.0  
**Last Updated**: 2026-06-21  
**Status**: Ready for deployment
