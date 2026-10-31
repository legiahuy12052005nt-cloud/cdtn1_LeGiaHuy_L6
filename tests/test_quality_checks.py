
import pandas as pd
import pytest

from src.quality.quality_checks import (
    check_order_id,
    check_product_id,
    check_quantity,
    check_unit_price,
    check_reported_sales_amount,
)


@pytest.mark.parametrize(
    "check_function, column, values, expected_count, expected_rate",
    [
        (check_order_id, "order_id", ["O001", "", None, "O004"],
         2, 50.0),

        (check_product_id, "product_id", ["P001", None, " ", "P004"],
         2, 50.0),

        (check_quantity, "quantity", [1, 0, -1, 2],
         2, 50.0),

        (check_unit_price, "unit_price", [100, 0, -10, None],
         2, 50.0),

        (check_reported_sales_amount,
         "reported_sales_amount", [500, 0, -100, "abc"],
         2, 50.0),
    ],
)
def test_quality_checks(
    check_function, column, values, expected_count, expected_rate
):
    df = pd.DataFrame({column: values})

    result = check_function(df)

    assert result["error_count"] == expected_count
    assert result["error_rate"] == expected_rate


def test_check_quantity_empty_dataframe():
    """Dữ liệu rỗng phải trả về 0 lỗi và tỷ lệ 0%."""
    df = pd.DataFrame({"quantity": []})

    result = check_quantity(df)

    assert result["error_count"] == 0
    assert result["error_rate"] == 0.0
