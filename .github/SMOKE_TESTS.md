# Bronze CI Smoke Tests Configuration

## Overview
Smoke tests are fast, minimal tests that verify basic functionality.
They should run in under 10 seconds total.

## Naming Convention
Use one of these patterns:
- `test_smoke_*.py` (Python)
- `*_smoke_test.dart` (Dart)
- `*.smoke.test.js` (JavaScript)

Or mark tests with `@pytest.mark.smoke` decorator in pytest.

## Examples

### Python (pytest)
```python
import pytest

@pytest.mark.smoke
def test_imports():
    """Verify critical imports work."""
    import mymodule
    assert mymodule is not None

@pytest.mark.smoke
def test_basic_functionality():
    """Verify basic app starts."""
    from mymodule import main
    assert main is not None
```

### Dart
```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:myapp/main.dart';

void main() {
  testWidgets('Smoke test: App builds', (WidgetTester tester) async {
    await tester.pumpWidget(MyApp());
    expect(find.byType(MyApp), findsOneWidget);
  });
}
```

## Running Smoke Tests

### Via Bronze CI
The Bronze CI workflow automatically detects and runs smoke tests.

### Locally
```bash
# Python
pytest -m smoke -v

# Dart
flutter test --name=smoke

# All tests (fallback)
pytest -q -k "smoke or not smoke"
```

## Best Practices
1. Keep smoke tests under 10 seconds total
2. Test only critical paths
3. Don't test external dependencies
4. Use mocks for I/O operations
5. Mark tests clearly with naming or decorators
