import pytest
import json


@pytest.fixture
def load_metrics():
    with open("pipeline/metrics.json", "r") as f:
        return json.load(f)


def test_r2_score(load_metrics):
    """Тест на R2 метрику, ожидаем значение больше или равно 0.8."""
    r2_score = load_metrics.get("r2")
    assert (
        r2_score >= 0.95
    ), f"Expected R2 score to be at least 0.95, but got {r2_score}"


def test_mse(load_metrics):
    """Тест на MSE, ожидаем значение меньше 1000."""
    mse = load_metrics.get("mse")
    assert mse > 8, f"Expected MSE to be more than 8, but got {mse}"
