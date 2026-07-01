import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

from config import BOT_TOKEN, ADMIN_IDS
from database.db import init_db

from handlers.start import cmd_start, show_main_menu
from handlers.ai_chat import menu_ai_chat, ai_clear_history, handle_ai_message
from handlers.image_gen import menu_image_gen, gen_balance_cb, handle_image_request
from handlers.translator import menu_translator, translator_lang_selected, handle_translate
from handlers.games import (
    menu_games, game_dice, dice_bet, dice_guess,
    game_coin, coin_bet, coin_side,
    game_guess, guess_bet, guess_number,
    game_21, game21_action,
)
from handlers.subscriptions import menu_subscription, my_subscription
from handlers.payments import buy_plan, paid_callback, handle_receipt, admin_confirm_payment, admin_reject_payment
from handlers.promo import menu_promo, handle_promo_input
from handlers.coins import menu_coins, menu_leaderboard
from handlers.referral import menu_referral
from handlers.wheel import menu_wheel, spin_wheel
from handlers.shop import menu_shop, shop_item_cb, shop_buy_cb, shop_equip_cb
from handlers.rates import menu_rates
from handlers.achievements import menu_achievements
from handlers.admin import (
    cmd_admin, adm_back, adm_users, adm_user_count, adm_user_search_start,
    adm_block_user, adm_unblock_user,
    adm_payments, adm_pay_pending, adm_pay_history,
    adm_promos, adm_promo_list, adm_promo_create_start, adm_promo_delete_start, adm_promo_edit_start,
    adm_subs, adm_sub_list, adm_sub_grant_start, adm_sub_extend_start, adm_sub_cancel_start,
    adm_grant_plan, adm_gens, adm_gen_add_start, adm_gen_deduct_start, adm_gen_check_start,
    adm_stats, adm_settings, adm_set_card, adm_set_prices, adm_set_limits,
    adm_set_welcome, adm_maintenance, adm_maint_toggle,
    adm_broadcast, adm_bc_target,
    adm_add_coins_cb, adm_add_gen_cb, adm_grant_sub_cb,
    admin_text_handler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def universal_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Routes text messages based on current user mode."""
    if not update.message or not update.message.text:
        return

    # 1. Admin flows have priority
    if update.effective_user.id in ADMIN_IDS:
        handled = await admin_text_handler(update, context)
        if handled:
            return

    mode = context.user_data.get("mode")

    # 2. Receipt upload mode
    if mode == "awaiting_receipt":
        # handled by photo handler
        return

    # 3. Promo input
    if mode == "promo_input":
        await handle_promo_input(update, context)
        return

    # 4. Translator input
    if mode == "translator_input":
        await handle_translate(update, context)
        return

    # 5. Image gen mode — check for style prefix
    if mode == "image_gen":
        text = update.message.text
        if text.startswith("/style "):
            style_key = text[7:].strip().lower()
            from handlers.image_gen import STYLE_PROMPTS
            style = STYLE_PROMPTS.get(style_key, "")
            await update.message.reply_text(
                f"🎨 Описание образа в стиле <b>{style_key}</b>?\nВведи описание:",
                parse_mode="HTML",
            )
            context.user_data["image_style"] = style
            return
        else:
            style = context.user_data.pop("image_style", "")
            prompt = f"{text}, {style}" if style else text
            await handle_image_request(update, context, prompt)
            return

    # 6. Default: AI chat
    await handle_ai_message(update, context)


async def universal_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Routes photo messages."""
    mode = context.user_data.get("mode")
    if mode == "awaiting_receipt":
        await handle_receipt(update, context)
        return
    # Default: send to AI for analysis
    await handle_ai_message(update, context)


async def noop_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()


def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not set in .env!")
        sys.exit(1)

    init_db()
    logger.info("Database initialized.")

    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("admin", cmd_admin))

    # ── Main menu callbacks ───────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(show_main_menu, pattern="^menu_main$"))
    app.add_handler(CallbackQueryHandler(menu_ai_chat, pattern="^menu_ai_chat$"))
    app.add_handler(CallbackQueryHandler(menu_image_gen, pattern="^menu_image_gen$"))
    app.add_handler(CallbackQueryHandler(menu_translator, pattern="^menu_translator$"))
    app.add_handler(CallbackQueryHandler(menu_games, pattern="^menu_games$"))
    app.add_handler(CallbackQueryHandler(menu_subscription, pattern="^menu_subscription$"))
    app.add_handler(CallbackQueryHandler(menu_promo, pattern="^menu_promo$"))
    app.add_handler(CallbackQueryHandler(menu_coins, pattern="^menu_coins$"))
    app.add_handler(CallbackQueryHandler(menu_leaderboard, pattern="^menu_leaderboard$"))
    app.add_handler(CallbackQueryHandler(menu_referral, pattern="^menu_referral$"))
    app.add_handler(CallbackQueryHandler(menu_wheel, pattern="^menu_wheel$"))
    app.add_handler(CallbackQueryHandler(menu_shop, pattern="^menu_shop$"))
    app.add_handler(CallbackQueryHandler(menu_rates, pattern="^menu_rates$"))
    app.add_handler(CallbackQueryHandler(menu_achievements, pattern="^menu_achievements$"))

    # ── AI Chat ───────────────────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(ai_clear_history, pattern="^ai_clear_history$"))

    # ── Image gen ─────────────────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(gen_balance_cb, pattern="^gen_balance$"))

    # ── Translator ────────────────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(translator_lang_selected, pattern="^tl_"))

    # ── Games ─────────────────────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(game_dice, pattern="^game_dice$"))
    app.add_handler(CallbackQueryHandler(dice_bet, pattern="^dice_bet_"))
    app.add_handler(CallbackQueryHandler(dice_guess, pattern="^dice_(higher|lower)_"))
    app.add_handler(CallbackQueryHandler(game_coin, pattern="^game_coin$"))
    app.add_handler(CallbackQueryHandler(coin_bet, pattern="^coin_bet_"))
    app.add_handler(CallbackQueryHandler(coin_side, pattern="^coin_(heads|tails)_"))
    app.add_handler(CallbackQueryHandler(game_guess, pattern="^game_guess$"))
    app.add_handler(CallbackQueryHandler(guess_bet, pattern="^guess_bet_"))
    app.add_handler(CallbackQueryHandler(guess_number, pattern="^guess_num_"))
    app.add_handler(CallbackQueryHandler(game_21, pattern="^game_21$"))
    app.add_handler(CallbackQueryHandler(game21_action, pattern="^game21_(hit|stand)_"))

    # ── Subscriptions ─────────────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(my_subscription, pattern="^sub_my$"))
    app.add_handler(CallbackQueryHandler(buy_plan, pattern="^sub_buy_"))
    app.add_handler(CallbackQueryHandler(paid_callback, pattern="^paid_"))

    # ── Wheel ─────────────────────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(spin_wheel, pattern="^wheel_spin$"))

    # ── Shop ──────────────────────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(shop_item_cb, pattern="^shop_item_"))
    app.add_handler(CallbackQueryHandler(shop_buy_cb, pattern="^shop_buy_"))
    app.add_handler(CallbackQueryHandler(shop_equip_cb, pattern="^shop_equip_"))

    # ── Admin payment confirm/reject ──────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(admin_confirm_payment, pattern="^adm_pay_confirm_"))
    app.add_handler(CallbackQueryHandler(admin_reject_payment, pattern="^adm_pay_reject_"))

    # ── Admin panel callbacks ─────────────────────────────────────────────────
    app.add_handler(CallbackQueryHandler(adm_back, pattern="^adm_back$"))
    app.add_handler(CallbackQueryHandler(adm_users, pattern="^adm_users$"))
    app.add_handler(CallbackQueryHandler(adm_user_count, pattern="^adm_user_count$"))
    app.add_handler(CallbackQueryHandler(adm_user_search_start, pattern="^adm_user_search$"))
    app.add_handler(CallbackQueryHandler(adm_block_user, pattern="^adm_block_"))
    app.add_handler(CallbackQueryHandler(adm_unblock_user, pattern="^adm_unblock_"))
    app.add_handler(CallbackQueryHandler(adm_payments, pattern="^adm_payments$"))
    app.add_handler(CallbackQueryHandler(adm_pay_pending, pattern="^adm_pay_pending$"))
    app.add_handler(CallbackQueryHandler(adm_pay_history, pattern="^adm_pay_history$"))
    app.add_handler(CallbackQueryHandler(adm_promos, pattern="^adm_promos$"))
    app.add_handler(CallbackQueryHandler(adm_promo_list, pattern="^adm_promo_list$"))
    app.add_handler(CallbackQueryHandler(adm_promo_create_start, pattern="^adm_promo_create$"))
    app.add_handler(CallbackQueryHandler(adm_promo_delete_start, pattern="^adm_promo_delete$"))
    app.add_handler(CallbackQueryHandler(adm_promo_edit_start, pattern="^adm_promo_edit$"))
    app.add_handler(CallbackQueryHandler(adm_subs, pattern="^adm_subs$"))
    app.add_handler(CallbackQueryHandler(adm_sub_list, pattern="^adm_sub_list$"))
    app.add_handler(CallbackQueryHandler(adm_sub_grant_start, pattern="^adm_sub_grant$"))
    app.add_handler(CallbackQueryHandler(adm_sub_extend_start, pattern="^adm_sub_extend$"))
    app.add_handler(CallbackQueryHandler(adm_sub_cancel_start, pattern="^adm_sub_cancel$"))
    app.add_handler(CallbackQueryHandler(adm_grant_plan, pattern="^adm_grant_\\d+_"))
    app.add_handler(CallbackQueryHandler(adm_grant_sub_cb, pattern="^adm_grant_sub_"))
    app.add_handler(CallbackQueryHandler(adm_add_coins_cb, pattern="^adm_add_coins_"))
    app.add_handler(CallbackQueryHandler(adm_add_gen_cb, pattern="^adm_add_gen_"))
    app.add_handler(CallbackQueryHandler(adm_gens, pattern="^adm_gens$"))
    app.add_handler(CallbackQueryHandler(adm_gen_add_start, pattern="^adm_gen_add$"))
    app.add_handler(CallbackQueryHandler(adm_gen_deduct_start, pattern="^adm_gen_deduct$"))
    app.add_handler(CallbackQueryHandler(adm_gen_check_start, pattern="^adm_gen_check$"))
    app.add_handler(CallbackQueryHandler(adm_stats, pattern="^adm_stats$"))
    app.add_handler(CallbackQueryHandler(adm_settings, pattern="^adm_settings$"))
    app.add_handler(CallbackQueryHandler(adm_set_card, pattern="^adm_set_card$"))
    app.add_handler(CallbackQueryHandler(adm_set_prices, pattern="^adm_set_prices$"))
    app.add_handler(CallbackQueryHandler(adm_set_limits, pattern="^adm_set_limits$"))
    app.add_handler(CallbackQueryHandler(adm_set_welcome, pattern="^adm_set_welcome$"))
    app.add_handler(CallbackQueryHandler(adm_maintenance, pattern="^adm_set_maintenance$"))
    app.add_handler(CallbackQueryHandler(adm_maint_toggle, pattern="^adm_maint_(on|off)$"))
    app.add_handler(CallbackQueryHandler(adm_broadcast, pattern="^adm_broadcast$"))
    app.add_handler(CallbackQueryHandler(adm_bc_target, pattern="^adm_bc_"))
    app.add_handler(CallbackQueryHandler(noop_cb, pattern="^noop$"))

    # ── Message handlers ──────────────────────────────────────────────────────
    app.add_handler(MessageHandler(filters.PHOTO, universal_photo_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, universal_text_handler))

    logger.info("Bot is starting...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

