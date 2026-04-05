import subprocess
import sys
from pathlib import Path


def test_main_script_execution():
    """Тест if __name__ == '__main__' блока."""
    result = subprocess.run(
        [sys.executable, "-m", "ecommerce_core.main"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    assert result.returncode == 0
    assert "Samsung Galaxy" in result.stdout
    assert "Смартфоны" in result.stdout
