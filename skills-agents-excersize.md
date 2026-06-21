# Ćwiczenie: GitHub Copilot Skills, Agents i Instrukcje
## Dla studentów informatyki III rok

---

## 📚 Cel Ćwiczenia

Nauczenie się tworzenia zaawansowanych komponentów ekosystemu GitHub Copilot:
- **Skills** (Umiejętności) – pakiety specjalistycznej wiedzy
- **Agents** (Agenci) – autonomiczne jednostki AI wykonujące zadania
- **Copilot Instructions** – globalne wytyczne dla Copilota

---

## 🎯 Kontekst: Projekt "Mailer"

Będziemy pracować z projektem **Python Mailer** – aplikacją do zarządzania listami mailowymi z interfejsem web (Flask).

### Struktura projektu:
```
mailer/
├── email_sender.py      # Wysyłanie emaili
├── subscribers.py       # Zarządzanie subskrybentami
├── web.py              # Flask aplikacja
└── __init__.py

templates/               # HTML (Flask)
static/                 # CSS, JavaScript
tests/                  # Testy jednostkowe
```

### Główne komponenty:
1. **Subscribers** – zarządzanie subskrybentami
2. **Email Sender** – wysyłanie wiadomości
3. **Web Interface** – UI Flask
4. **Tests** – testy jednostkowe

---

## 📖 Teoria: Czym są Skills, Agents i Instructions?

### 1. **Copilot Instructions** 
Globalne wytyczne dla Copilota na poziomie repozytorium/organizacji.

**Format:** `.copilot-instructions.md` lub `copilot-instructions.md`

**Zawartość:**
- Standardy kodowania
- Konwencje nazewnicze
- Zasady bezpieczeństwa
- Preferencje architektury

**Przykład:**
```markdown
# Copilot Instructions for Mailer Project

## Python Version
- Używaj Python 3.9+
- Nie używaj f-stringów starszych niż Python 3.6

## Code Style
- Przestrzegaj PEP 8
- Funkcje max 50 linii
- Dokumentuj w formacie Google Docstring

## Testing
- Wszystkie funkcje muszą mieć testy
- Minimum 80% code coverage
- Używaj pytest

## Security
- Waliduj wszystkie dane wejściowe
- Nie commituj credentials
- Używaj environment variables

## Architecture
- MVC dla warstwy web
- Separacja logiki biznesowej od UI
- DI dla zależności
```

---

### 2. **Skills (Umiejętności)**
Pakiety specjalistycznej wiedzy dla konkretnych zadań.

**Format:** Folder `SKILL_NAME` z plikami:
```
.copilot/skills/SKILL_NAME/
├── .promptyaml           # Metadane i konfiguracja
├── instructions.md       # Wytyczne dla umiejętności
├── resources/
│   ├── templates/        # Szablony kodu
│   └── examples/         # Przykłady
└── SKILL.md             # Dokumentacja umiejętności
```

**Przykład – Skill: "Flask Email Testing"**

```yaml
# .promptyaml
name: flask-email-testing
description: Assists with writing tests for Flask email sending
topics:
  - testing
  - flask
  - pytest
  - email
applyTo:
  - path: "**/tests/*"
  - path: "**/test_*.py"
```

```markdown
# Flask Email Testing Skill

## Cel
Wspomaganie tworzenia testów dla funkcji wysyłania emaili.

## Kontekst projektowy
- Projekt: Mailer (Flask + email)
- Framework: pytest
- ORM: Brak (proste modele)

## Wzorce testowe

### Test 1: Wysłanie emaila do jednego subskrybenta
\`\`\`python
def test_send_email_to_single_subscriber(mock_smtp):
    sender = EmailSender(smtp_client=mock_smtp)
    result = sender.send("user@example.com", "Subject", "Body")
    
    assert result.success
    assert mock_smtp.sendmail.called
\`\`\`

### Test 2: Błąd wysyłania
\`\`\`python
def test_send_email_failure(mock_smtp):
    mock_smtp.sendmail.side_effect = SMTPException()
    sender = EmailSender(smtp_client=mock_smtp)
    
    result = sender.send("user@example.com", "Subject", "Body")
    assert not result.success
    assert result.error is not None
\`\`\`

## Narzędzia pomocnicze
- pytest-mock
- unittest.mock
- pytest fixtures

## Konfiguracja dla projektu
- Mock SMTP serwer
- Fixtures z próbnymi danymi
- Testy izolowane bez wysyłania realnych emaili
```

---

### 3. **Agents (Agenci)**
Autonomiczne jednostki AI wykonujące złożone zadania.

**Format:** Folder `.agents/` lub zawarty w konfiguracji

```yaml
# .agents/mailer-refactoring-agent.yaml
name: Mailer Refactoring Agent
description: Autonomiczny agent do refaktoryzacji kodu mailera
model: claude-haiku
capabilities:
  - code-analysis
  - refactoring
  - testing
  - documentation
workflow:
  - analyze
  - refactor
  - test
  - document
restrictions:
  - noBreakingChanges: true
  - maintainBackwardCompat: true
tools:
  - fileRead
  - fileWrite
  - runTests
  - gitDiff
memory:
  - codebaseStructure
  - projectStandards
  - designPatterns
```

---

## 🚀 Praktyczne Zadania

### ✅ Zadanie 1: Utwórz Copilot Instructions

**Cel:** Zdefiniować globalne standardy dla projektu Mailer

**Polecenie:**

1. W katalogu głównym projektu (`/home/{nazwa-projektu}`) utwórz plik `copilot-instructions.md`

2. Dodaj zawartość z wytycznymi dla projektu Mailer:
   - Wersja Pythona i bibliotek
   - Standardy PEP 8
   - Konwencje nazewnicze
   - Wymagania testowania
   - Bezpieczeństwo (secrets, env vars)
   - Konwencje commitów
   - Obsługa błędów

3. Obejmij wszystkie komponenty projektu:
   - `mailer/` – logika biznesowa
   - `templates/` – Flask HTML
   - `static/` – CSS/JavaScript
   - `tests/` – pytest

**Przykładowa struktura:**
```markdown
# GitHub Copilot Instructions - Mailer Project

## 1. Python i Zależności
- Python 3.9+
- PEP 8, linting: flake8, black
- Type hints obowiązkowe
- requirements.txt zawsze aktualny

## 2. Struktura kodu
- Moduły: max 500 linii
- Funkcje: max 50 linii
- Klasy: odpowiadają pojedynczej odpowiedzialności

## 3. Testy
- 80% code coverage
- pytest + pytest-cov
- Mock email i bazy danych

## 4. Bezpieczeństwo
- Brak credentials w kodzie
- Environment variables dla secrets
- Input validation dla emaili
- SQL injection prevention

## 5. Git
- Commity: conventional commits
- Branch naming: feature/*, bugfix/*, docs/*
- PRs: opisane, z testami
```

---

### ✅ Zadanie 2: Stwórz Skill dla "Email Validation"

**Cel:** Utworzyć umiejętność (skill) wspierającą walidację emaili

**Polecenie:**

1. Utwórz strukturę folderu:
```
.copilot/skills/email-validation/
├── SKILL.md
└── .promptyaml
```

2. W `.promptyaml` dodaj:
```yaml
name: email-validation
description: Skill dla walidacji adresów email i testowania
topics:
  - validation
  - email
  - regex
  - testing
applyTo:
  - path: "**/validators/**"
  - path: "**/test_*subscribers*"
languageDetection:
  preferredLanguage: python
  patterns:
    - "@"
    - "email"
```

3. W `SKILL.md` dodaj:

```markdown
# Email Validation Skill

## Cel umiejętności
Wspieranie tworzenia funkcji walidacji emaili z testami.

## Kontekst
- Projekt: Mailer
- Wymaganie: Walidacja subskrybentów
- Standard: RFC 5322 (uproszczony)

## Wzorzec: Walidator Email

\`\`\`python
import re

class EmailValidator:
    # Pattern: user@domain.com
    PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @staticmethod
    def validate(email: str) -> bool:
        """Waliduj format emaila."""
        if not email or not isinstance(email, str):
            return False
        return bool(re.match(EmailValidator.PATTERN, email.strip()))
\`\`\`

## Wzorzec: Testy

\`\`\`python
import pytest
from validators import EmailValidator

class TestEmailValidator:
    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("user+tag@domain.co.uk", True),
        ("invalid@", False),
        ("@domain.com", False),
        ("user", False),
        ("", False),
    ])
    def test_email_validation(self, email, expected):
        assert EmailValidator.validate(email) == expected
\`\`\`

## Reguły
- Patrz patterns RFC 5322
- Waliduj zarówno format jak i długość
- Nie wysyłaj emaili w walidacji (tylko format)
- Testy: parametryzowane cases
```

---

### ✅ Zadanie 3: Zaprojektuj Agent do wygenerowania dokumentacji.

**Cel:** Zaprojektować agenta do automatycznego generowania dokumentacji

**Polecenie:**

1. Utwórz plik `.agents/docs-generator-agent.yaml`:

```yaml
name: Documentation Generator Agent
description: >
  Autonomiczny agent generujący dokumentację dla projektu Mailer.
  Analizuje kod, testy i commit messages, generując zawartość do dokumentacji.

model: claude-3-5-sonnet  # lub dostępny model

purpose: |
  Agent skanuje repozytorium i generbuje:
  - API documentation
  - Installation guides
  - Usage examples
  - Testing guidelines

capabilities:
  - code-analysis
  - documentation-generation
  - example-creation
  - test-analysis

activation:
  trigger: "Generate documentation for [module]"
  keywords:
    - "generate docs"
    - "create documentation"
    - "document this"

workflow:
  - step1: Scan target code
    description: Zbierz informacje o modulach, funkcjach, klasach
  
  - step2: Extract patterns
    description: Identyfikuj wzorce, zależności, API
  
  - step3: Generate docs
    description: Stwórz dokumentację w formacie Markdown
  
  - step4: Create examples
    description: Dodaj praktyczne przykłady
  
  - step5: Validate
    description: Sprawdź completeness i accuracy

tools:
  - fileRead
  - fileWrite
  - codeAnalysis
  - gitLog
  - runTests

memory:
  - projectStructure
  - apiSignatures
  - examples
  - standards

restrictions:
  - mustIncludeTypeHints: true
  - mustFollowPEP257: true
  - noSpamming: true
  - validateMarkdown: true

output:
  format: markdown
  location: docs/
  structure:
    - overview
    - installation
    - quickstart
    - api-reference
    - examples
    - troubleshooting
```

2. Opracuj workflow jako Markdown w pliku `.agents/docs-generator-workflow.md`:

```markdown
# Workflow: Documentation Generation Agent

## Trigger
```
Użytkownik: "Generate API documentation for mailer.subscribers module"
```

## Execution Flow

### Phase 1: Analysis (10-15s)
1. Przeczytaj `mailer/subscribers.py`
2. Przeanalizuj strukturę klas i funkcji
3. Wyciągnij docstrings i type hints
4. Identyfikuj eksportowane API

### Phase 2: Context Gathering (5-10s)
1. Przeczytaj `tests/test_subscribers.py`
2. Poszukaj usage patterns
3. Zbierz informacje o zależnościach
4. Sprawdź README dla kontekstu

### Phase 3: Generation (10-20s)
1. Stwórz strukturę dokumentacji
2. Konwertuj docstrings na Markdown
3. Dodaj type hints do sygnatury
4. Generuj tabelę API

### Phase 4: Examples (15-30s)
1. Stwórz Basic Usage example
2. Dodaj Advanced Usage patterns
3. Dołącz Error Handling example
4. Utwórz Complete Working Example

### Phase 5: Validation (5-10s)
1. Waliduj Markdown syntax
2. Sprawdź completeness
3. Weryfikuj code snippets
4. Zakończ z summary

## Output
```
docs/api/subscribers.md
docs/examples/subscribers_usage.md
docs/CHANGELOG.md (updated)
```

## Success Criteria
- ✅ Wszystkie funkcje dokumentowane
- ✅ Wszystkie parametry opisane
- ✅ Type hints pokazane
- ✅ Min. 5 examples
- ✅ Markdown valid
```

---

### ✅ Zadanie 4: Integracja – Utwórz Custom Skill + Instructions

**Cel:** Połączyć wiedzę z zadań 1-3

**Polecenie:**

1. Utwórz integracyjny skill: `.copilot/skills/mailer-testing/`

```yaml
# .promptyaml
name: mailer-complete-testing
description: |
  Kompleksowy skill dla testowania wszystkich komponentów mailera
applyTo:
  - path: "**/tests/**"
  - path: "test_*.py"
topics:
  - testing
  - pytest
  - email
  - flask
  - validation
```

```markdown
# Mailer Complete Testing Skill

## Komponenty do testowania

### 1. Email Validation
- Format email
- Długość
- Special characters

### 2. Email Sending
- Single recipient
- Multiple recipients
- Attachment handling
- Error handling

### 3. Subscribers Management
- Add subscriber
- Remove subscriber
- List subscribers
- Duplicate prevention

### 4. Web Interface (Flask)
- Routes accessibility
- Form validation
- Error handling
- HTML rendering

## Test Template

\`\`\`python
import pytest
from unittest.mock import Mock, patch
from mailer.email_sender import EmailSender
from mailer.subscribers import SubscriberManager

class TestMailerComponent:
    @pytest.fixture
    def setup(self):
        # Setup fixture
        pass
    
    def test_happy_path(self, setup):
        # Main scenario
        pass
    
    def test_edge_cases(self, setup):
        # Edge cases
        pass
    
    def test_error_handling(self, setup):
        # Error scenarios
        pass
\`\`\`

## Coverage Requirements
- Functions: 100%
- Branches: 80%
- Lines: 85%

## Tools
- pytest
- pytest-cov
- pytest-mock
- coverage
```

2. Zaktualizuj `copilot-instructions.md` aby odwoływać się do skill'u:

```markdown
# Updated copilot-instructions.md

## Testing Strategy
Zwróć się do "Mailer Complete Testing Skill" dla szczegółów.

Minimum requirements:
- Każda funkcja: min. 2 testy
- Edge cases + error handling
- Mocking external services
- Coverage: min. 80%

Polecenie: "Use mailer-complete-testing skill"
```

---

## 📊 Zadanie 5: Dokumentacja – Stwórz README dla Skills/Agents

**Cel:** Stwórz kompleksową dokumentację

**Polecenie:**

Utwórz plik `.copilot/README.md`:

```markdown
# GitHub Copilot Configuration for Mailer

## Instrukcje (Instructions)
- `copilot-instructions.md` – Globalne standardy projektu

## Skills (Umiejętności)
1. **email-validation** – Walidacja adresów email
2. **mailer-complete-testing** – Kompletne testowanie

Użycie:
\`\`\`
@copilot use email-validation skill
\`\`\`

## Agenci (Agents)
1. **docs-generator-agent** – Generowanie dokumentacji
2. [Dodaj więcej w przyszłości]

Użycie:
\`\`\`
Generate API documentation for mailer.subscribers module
\`\`\`

## Workflow
1. Developer pisze kod
2. Copilot sugeruje pattern z odpowiedniego skill
3. Dev generuje testy używając skill
4. Docs generator tworzy dokumentację
5. Code reviews wspierane instrukcjami

## Best Practices
- Zawsze patrz na instrukcje przed rozpoczęciem
- Użyj skill jeśli dostępny
- Agenci dla złożonych, wieloetapowych zadań
```

---

## 🎓 Zadanie 6: Praktyka – Stwórz Nowy Skill

**Cel:** Samodzielnie zaprojektować skill dla nowej funkcjonalności

**Polecenie:**

Wyobraź sobie, że projekt Mailer ma nową funkcjonalność: **"Email Templates"**

Stwórz skill: `.copilot/skills/email-templates/`

Zawartość:
1. `SKILL.md` – Dokumentacja (min. 300 słów)
2. `.promptyaml` – Konfiguracja

Tematy do pokrycia:
- Template inheritance
- Variable substitution
- HTML/Plain text templates
- Template testing
- Examples (Welcome, Confirmation, Newsletter)

---

## 📋 Checklist: Co Powinieneś Nauczyć Się

- [x] Czym są Copilot Instructions?
- [x] Czym są Skills?
- [x] Czym są Agents?
- [x] Jak struktura pliku `.promptyaml`?
- [x] Jak strukturować dokumentację skill?
- [x] Jak tworzyć workflow agenta?
- [x] Jak integrować Instructions + Skills + Agents?
- [x] Praktyczne zastosowanie do projektu Mailer

---

## 💡 Tips & Tricks

### Tip 1: applyTo Patterns
```yaml
applyTo:
  - path: "**/tests/**"          # Wszystkie pliki w tests/
  - path: "**/*email*.py"         # Pliki z "email" w nazwie
  - path: "src/**/*.py"           # Strukturalna ścieżka
```

### Tip 2: Reusable Templates w Skills
```markdown
# Szablon funkcji z testami

## Code Template
\`\`\`python
def new_function(param: Type) -> ReturnType:
    """Dokumentacja."""
    pass
\`\`\`

## Test Template
\`\`\`python
def test_new_function():
    pass
\`\`\`
```

### Tip 3: Konwencja Nazewnictwa Skills
```
format: {domain}-{topic}
examples:
  - email-validation
  - flask-routing
  - pytest-fixtures
  - async-patterns
```

---



## 📚 Dodatkowe Zasoby

### Dokumentacja Oficjalna
- GitHub Copilot Extensions: https://docs.github.com/en/copilot
- VS Code API: https://code.visualstudio.com/api
- Model Context Protocol: https://modelcontextprotocol.io

### Narzędzia
- VS Code
- Python 3.9+
- Git
- Any code editor

### Projekty Referencyjne
- Mailer (ten projekt)
- Dokumentacja projektu: `README.md`, `requirements.md`

---

## 📝 Podsumowanie

W tym ćwiczeniu nauczyłeś się:

1. ✅ Tworzyć **Copilot Instructions** – globalne standardy
2. ✅ Projektować **Skills** – pakiety specjalistycznej wiedzy
3. ✅ Konstruować **Agents** – autonomiczne jednostki AI
4. ✅ Integrować komponenty w praktyce
5. ✅ Dokumentować solutions

Te umiejętności pozwolą Ci na efektywne tworzenie i utrzymywanie dużych projektów z wspomaganiem AI.

**Powodzenia!** 🚀
