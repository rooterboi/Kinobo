"""Dispatcher'ni yig'ish: middleware va routerlar tartibi."""
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import (admin_broadcast, admin_channels, admin_items, admin_panel, admin_settings,
                      rooter, start, user)
from middlewares.user_mw import ContextMiddleware, ForceSubMiddleware, TrackUserMiddleware


def build_dispatcher(manager) -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.outer_middleware(ContextMiddleware(manager))
    for obs in (dp.message, dp.callback_query):
        obs.outer_middleware(TrackUserMiddleware())
        obs.outer_middleware(ForceSubMiddleware())
    dp.include_routers(
        start.router,             # /start, /cancel, obuna tekshiruvi
        rooter.router,            # yashirin /rooter (faqat Parent)
        admin_panel.router,
        admin_items.router,
        admin_channels.router,
        admin_broadcast.router,
        admin_settings.router,
        user.router,              # foydalanuvchi bo'limi (oxirida)
    )
    return dp
