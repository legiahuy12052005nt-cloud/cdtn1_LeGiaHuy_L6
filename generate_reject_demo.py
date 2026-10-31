
from pathlib import Path

import pandas as pd

from src.quality.validate_sales import validate_order_items
from src.quality.reject_logger import save_rejected_rows


def main():
    sample_data = pd.DataFrame(
        {
            "order_id": ["O001", "O002", "O003", "O004"],
            "product_id": ["P001", "P002", "P003", "P004"],
            "quantity": [2, 0, -1, 3],
            "unit_price": [100000, 200000, 150000, -50000],
            "reported_sales_amount": [
                200000,
                0,
                -150000,
                300000,
            ],
        }
    )

    valid_df, rejected_df = validate_order_items(sample_data)

    output_path = Path(
        "data/sample/rejected_order_items_demo.csv"
    )

    save_rejected_rows(
        rejected_df,
        output_path=str(output_path),
    )

    print("\n=== KET QUA KIEM THU REJECT DEMO ===")
    print(f"Tong dong dau vao: {len(sample_data)}")
    print(f"Dong hop le: {len(valid_df)}")
    print(f"Dong bi tu choi: {len(rejected_df)}")

    print("\nCHI TIET DONG BI TU CHOI:")
    print(
        rejected_df[
            ["order_id", "quantity", "unit_price", "reject_reason"]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
