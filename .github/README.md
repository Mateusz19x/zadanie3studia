# GitHub Copilot Configuration for Mailer

Complete documentation of all GitHub Copilot customizations (Instructions, Skills, and Agents) for the Mailer project.

---

## 📋 Quick Navigation

- [Instructions](#instructions) – Global project standards
- [Skills](#skills) – Specialized knowledge packages
- [Agents](#agents) – Autonomous AI workflows
- [Usage Guide](#usage-guide) – How to use customizations
- [Best Practices](#best-practices) – Tips for effective use

---

## Instructions

### `copilot-instructions.md`

**Location**: Project root  
**Purpose**: Global standards and guidelines for the entire Mailer project  
**Scope**: Applies to all development activities

#### Coverage

1. **Python & Dependencies** – Version requirements, code style, type hints
2. **Code Structure** – Module size, naming conventions, documentation
3. **Testing** – Coverage requirements, test organization, frameworks
4. **Security** – Secrets management, input validation, error handling
5. **Git & Commits** – Commit format (JIRA), branching, PR requirements
6. **Architecture** – Project structure, design principles, MVC patterns
7. **Tools & Automation** – Scripts for formatting, linting, running tests
8. **AI Development** – Tips for using Copilot effectively
9. **Code Review Checklist** – Pre-review requirements
10. **Resources** – Documentation links and file references

#### Key Takeaways

- Python 3.9+, PEP 8, type hints mandatory
- 80% minimum test coverage
- JIRA-formatted commits required
- No secrets in code, use environment variables
- Follow SOLID principles and separation of concerns

#### When to Reference

- Before starting new work
- During code review
- When implementing new features
- When setting up development environment

---

## Skills

Skills are specialized knowledge packages for specific tasks. Invoke them with:

```
@copilot use [skill-name] skill
```

Or ask Copilot with keywords from the skill description.

---

### Skill 1: `git-commit-jira-format`

**Location**: `.github/skills/git-commit-jira-format/`  
**Description**: Standardized JIRA-formatted commit messages  
**Keywords**: commit, jira, message format, git history

#### What It Includes

- `SKILL.md` – Full workflow documentation
- `COMMIT_TEMPLATE.md` – Quick reference guide
- `git_commit_helper.py` – Interactive helper script

#### Workflow

```
PROJECT-### One-line summary

- Detailed point 1
- Detailed point 2
```

#### Usage Example

```bash
# Interactive helper
python .github/skills/git-commit-jira-format/git_commit_helper.py

# Or use git directly
git commit -m "LAB-003 Implement helper scripts

- Added cross-platform helper scripts
- Applied black formatting
- Fixed pylint issues"
```

#### When to Use

- ✅ Creating commits
- ✅ Improving commit history
- ✅ Linking commits to JIRA issues

---

### Skill 2: `email-validation`

**Location**: `.github/skills/email-validation/`  
**Description**: Email validation patterns and comprehensive testing  
**Keywords**: email, validation, regex, testing, validators

#### What It Includes

- `SKILL.md` – Validation patterns, test templates, common pitfalls
- `.promptyaml` – Skill configuration

#### Core Pattern

```python
class EmailValidator:
    PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @staticmethod
    def validate(email: str) -> bool:
        """Validate email format."""
        if not email or not isinstance(email, str):
            return False
        return bool(re.match(EmailValidator.PATTERN, email.strip()))
```

#### Test Template

```python
@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("invalid", False),
])
def test_email_validation(self, email, expected):
    assert EmailValidator.validate(email) == expected
```

#### When to Use

- ✅ Implementing email validation
- ✅ Writing validator tests
- ✅ Handling email format checks
- ✅ Handling validation edge cases

---

### Skill 3: `mailer-complete-testing`

**Location**: `.github/skills/mailer-complete-testing/`  
**Description**: Complete testing patterns for all Mailer components  
**Keywords**: testing, pytest, email, flask, validation, unit tests

#### What It Includes

- `SKILL.md` – Test templates for all components, coverage requirements, best practices

#### Components Covered

1. **Email Validation Testing** – Format checks, edge cases
2. **Email Sending Testing** – Single/bulk emails, error handling
3. **Subscribers Management Testing** – CRUD operations, statistics
4. **Flask API Testing** – Endpoint testing, status codes
5. **Integration Testing** – End-to-end workflows

#### Coverage Requirements

```
Overall: 80% minimum, 90% target
Functions: 100%
Branches: 80%
Lines: 85%
```

#### Running Tests

```bash
# Run all tests with coverage
pytest --cov --cov-report=html

# View coverage report
open htmlcov/index.html
```

#### When to Use

- ✅ Writing unit tests
- ✅ Testing new features
- ✅ Improving test coverage
- ✅ Setting up test structure
- ✅ Testing API endpoints

---

## Agents

Agents are autonomous AI units that execute multi-step workflows. Trigger them by asking Copilot with specific keywords.

---

### Agent 1: `Documentation Generator Agent`

**Location**: `.github/agents/docs-generator-agent.yaml`  
**Description**: Autonomous documentation generation for code modules  
**Workflow**: `.github/agents/docs-generator-workflow.md`

#### Capabilities

- Code analysis and structure extraction
- API documentation generation
- Usage example creation
- Markdown formatting and validation
- Example testing and verification

#### Trigger

Ask Copilot:
```
Generate API documentation for mailer.subscribers module
```

Or:
```
Create documentation for [module_name]
```

#### Workflow Phases

1. **Analysis** (10-15s) – Read and analyze code structure
2. **Context Gathering** (5-10s) – Collect usage patterns from tests
3. **Generation** (10-20s) – Create markdown documentation
4. **Examples** (15-30s) – Generate practical code examples
5. **Validation** (5-10s) – Verify completeness and correctness

#### Output

```
docs/
├── api/subscribers.md
├── examples/subscribers_usage.md
└── guides/subscriber_management.md
```

#### When to Use

- ✅ Creating API documentation
- ✅ Generating usage guides
- ✅ Creating examples
- ✅ Updating project documentation
- ✅ Preparing for releases

---

### Agent 2: `python-solution-coder` (Pre-existing)

**Location**: `.github/agents/` (framework provided)  
**Description**: Generates production-grade Python solutions with best practices  
**Trigger**: Request implementation of features from requirements.md

#### Capabilities

- Code generation with type hints
- Google-style docstrings
- Comprehensive error handling
- Test suite creation
- Best practices enforcement

#### When to Use

- ✅ Implementing new features
- ✅ Generating initial code structure
- ✅ Creating complete solutions with tests

---

## Usage Guide

### Basic Workflow

1. **Start with Instructions** (`copilot-instructions.md`)
   - Read project standards
   - Understand conventions
   - Review best practices

2. **Use Relevant Skill** for the task
   - Email validation? → `email-validation` skill
   - Need tests? → `mailer-complete-testing` skill
   - Creating commit? → `git-commit-jira-format` skill

3. **Invoke Skills with**
   ```
   @copilot use [skill-name] skill
   ```

4. **For Complex Tasks, Use Agents**
   ```
   Generate [something] for [module]
   ```

5. **Apply Standards** from Instructions throughout

### Example Scenarios

#### Scenario 1: Add New Subscriber Feature

```
1. Read: copilot-instructions.md (architecture, structure)
2. Use: email-validation skill (for email checks)
3. Use: mailer-complete-testing skill (for unit tests)
4. Reference: JIRA skill (for commit message)
5. Result: Complete feature with tests and documentation
```

#### Scenario 2: Generate API Documentation

```
1. Ask: "Generate API documentation for email_sender module"
2. Agent: docs-generator-agent executes 5-phase workflow
3. Result: Complete API docs with examples in docs/ folder
4. Use: git-commit-jira-format for commit
5. Done: Documentation is ready
```

#### Scenario 3: Write Email Validation Tests

```
1. Use: email-validation skill (for patterns)
2. Use: mailer-complete-testing skill (for test structure)
3. Apply: copilot-instructions.md (coverage requirements)
4. Result: Comprehensive test coverage
5. Use: Helper scripts to run tests
```

---

## Best Practices

### When Using Instructions

- ✅ Read the relevant section before starting
- ✅ Apply all guidelines during code review
- ✅ Reference specific sections in PRs
- ✅ Update instructions if standards change

### When Using Skills

- ✅ Read the skill documentation first
- ✅ Understand the patterns before applying
- ✅ Copy-paste templates and customize
- ✅ Refer to examples for clarification
- ✅ Cross-reference with Instructions

### When Using Agents

- ✅ Provide clear, specific requests
- ✅ Review generated output before use
- ✅ Test generated code thoroughly
- ✅ Adjust if output doesn't meet expectations
- ✅ Provide feedback for agent improvement

### General Tips

1. **Be Specific** – "Generate documentation for subscribers.py" not "Generate docs"
2. **Use Keywords** – Mention component/module names from skills
3. **Cross-Reference** – Link to Instructions when applicable
4. **Verify Output** – Always test generated code and documentation
5. **Keep Updated** – Update customizations as project evolves

---

## Integration Points

### With Development Workflow

```
[Start Task]
    ↓
[Read Instructions]
    ↓
[Use Skill(s)]
    ↓
[Apply Best Practices]
    ↓
[Code & Test]
    ↓
[Use Skill: git-commit-jira-format]
    ↓
[Commit & Push]
```

### With CI/CD Pipeline

```yaml
# Example GitHub Actions
- name: Check Against Instructions
  run: pylint *.py  # Enforces style from instructions

- name: Run Tests (per mailer-complete-testing)
  run: pytest --cov --cov-report=xml

- name: Generate Docs (using agent)
  run: copilot-run docs-generator-agent
```

### With Code Review

```
Reviewer checklist (from copilot-instructions.md):
- [ ] Follows naming conventions
- [ ] Type hints on all functions
- [ ] Docstrings present
- [ ] Tests pass (80%+ coverage)
- [ ] No secrets in code
- [ ] Commit follows JIRA format
```

---

## Customization & Extension

### Creating New Skills

To add a new skill:

1. Create directory: `.github/skills/[new-skill-name]/`
2. Add `SKILL.md` with documentation
3. Add `.promptyaml` with configuration
4. Include code templates and examples
5. Update this README with new skill info
6. Reference from Instructions if relevant

### Creating New Agents

To add a new agent:

1. Create `.github/agents/[agent-name].yaml`
2. Define capabilities and workflow
3. Create matching workflow documentation file
4. Update this README with agent info
5. Test with sample requests

---

## Support & Resources

### Quick Links

- **Project Instructions**: `copilot-instructions.md`
- **Implementation Guide**: `README_IMPLEMENTATION.md`
- **Main Project README**: `README.md`

### Skill Resources

| Skill | Full Docs | Templates | Examples |
|-------|-----------|-----------|----------|
| email-validation | SKILL.md | ✓ Validation class | ✓ Test patterns |
| mailer-complete-testing | SKILL.md | ✓ All components | ✓ Complete tests |
| git-commit-jira-format | SKILL.md | ✓ Examples | ✓ Real commits |

### Contact

For questions about customizations:
- Review the specific skill/agent documentation
- Check copilot-instructions.md for standards
- Refer to code examples in test files
- Ask Copilot for clarification using skill keywords

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-21 | Initial release with 3 skills and 2 agents |

---

## Quick Reference

### File Structure

```
.github/
├── copilot-instructions.md          # Main instructions
├── README.md                        # This file
├── agents/
│   ├── docs-generator-agent.yaml
│   └── docs-generator-workflow.md
└── skills/
    ├── email-validation/
    │   ├── SKILL.md
    │   └── .promptyaml
    ├── git-commit-jira-format/
    │   ├── SKILL.md
    │   ├── COMMIT_TEMPLATE.md
    │   └── git_commit_helper.py
    └── mailer-complete-testing/
        ├── SKILL.md
        └── .promptyaml
```

### Commands

```bash
# Format code (from instructions)
python helpers.py format

# Run tests (per mailer-complete-testing)
python helpers.py test

# Lint code (from instructions)
python helpers.py lint

# Helper for commits (git-commit-jira-format)
python .github/skills/git-commit-jira-format/git_commit_helper.py
```

---

**Last Updated**: 2026-06-21  
**Maintained By**: Development Team  
**Status**: Active & Ready for Use
