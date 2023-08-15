from aiogram import types

POST_REGULAR_SHIPPING = types.ShippingOption(
    id="reg_ship",
    title="Доставка",
    prices=[
        types.LabeledPrice(
            "Доставка", 0
        )
    ]
)
