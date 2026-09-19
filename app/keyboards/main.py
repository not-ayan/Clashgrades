from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


NAV_BUTTONS = [
    ("📊 Dashboard", "nav:dashboard"),
    ("🔨 Builders", "nav:builders"),
    ("⚔️ Upgrades", "nav:upgrades"),
    ("🎯 Plan", "nav:plan"),
    ("📈 Progress", "nav:progress"),
    ("🧠 Ask AI", "nav:ask"),
    ("⚙️ Settings", "nav:settings"),
    ("🧪 Audit", "nav:audit"),
    ("🔄 Refresh", "action:sync"),
]


def main_menu_keyboard() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=text, callback_data=cb)] for text, cb in NAV_BUTTONS]
    return InlineKeyboardMarkup(inline_keyboard=rows)
