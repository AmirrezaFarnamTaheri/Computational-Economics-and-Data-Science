from scripts.audit_curriculum_ast import _bootstrap_name_errors


def test_bootstrap_audit_catches_use_before_import():
    source = """rng = np.random.default_rng(42)
import numpy as np
"""
    errors = _bootstrap_name_errors(source)
    assert any("'np' used before import/definition" in item for item in errors)


def test_bootstrap_audit_catches_undefined_top_level_name():
    errors = _bootstrap_name_errors("result = missing_name + 1\n")
    assert any(
        "'missing_name' used before import/definition" in item for item in errors
    )


def test_bootstrap_audit_accepts_clean_import_order():
    source = """import numpy as np
rng = np.random.default_rng(42)
values = rng.normal(size=10)
"""
    assert _bootstrap_name_errors(source) == []


def test_bootstrap_audit_accepts_try_local_import_and_helper():
    source = """try:
    from sympy import init_printing

    def configure():
        init_printing(use_unicode=True)

    configure()
except ImportError as exc:
    reason = str(exc)
"""
    assert _bootstrap_name_errors(source) == []
