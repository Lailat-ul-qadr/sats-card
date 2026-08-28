"""USSD Gateway Handler - manages USSD sessions and menu navigation."""

from __future__ import annotations
import time
import logging
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class USSDSession(BaseModel):
    session_id: str
    phone_number: str
    current_screen: str = "main_menu"
    data: dict = {}
    created_at: float = Field(default_factory=time.time)
    last_activity: float = Field(default_factory=time.time)


class USSDResponse(BaseModel):
    text: str
    continue_session: bool = True


class USSDScreen(str, Enum):
    MAIN_MENU = "main_menu"
    CHECK_BALANCE = "check_balance"
    P2P_TRANSFER_MENU = "p2p_transfer_menu"
    P2P_TRANSFER_PHONE = "p2p_transfer_phone"
    P2P_TRANSFER_AMOUNT = "p2p_transfer_amount"
    P2P_TRANSFER_CONFIRM = "p2p_transfer_confirm"
    SEND_BTC_MENU = "send_btc_menu"
    SEND_BTC_AMOUNT = "send_btc_amount"
    SEND_BTC_CONFIRM = "send_btc_confirm"
    FUND_ACCOUNT_MENU = "fund_account_menu"
    FUND_ACCOUNT_CONFIRM = "fund_account_confirm"
    RECEIVE_USD_MENU = "receive_usd_menu"
    RECEIVE_USD_CONFIRM = "receive_usd_confirm"
    SWAP_MENU = "swap_menu"
    SWAP_AMOUNT = "swap_amount"
    SWAP_CONFIRM = "swap_confirm"
    WITHDRAW_MENU = "withdraw_menu"
    WITHDRAW_PROVIDER = "withdraw_provider"
    WITHDRAW_AMOUNT = "withdraw_amount"
    WITHDRAW_CONFIRM = "withdraw_confirm"
    HELP = "help"
    TRANSACTION_RESULT = "transaction_result"
    ERROR = "error"


MENUS = {
    USSDScreen.MAIN_MENU: (
        "MOBIBIT AFRICA\n"
        "Welcome! Select an option:\n\n"
        "1. Check Balance\n"
        "2. Send BTC to User\n"
        "3. Send BTC via Lightning\n"
        "4. Fund Account (Buy BTC)\n"
        "5. Receive USD\n"
        "6. Convert BTC <-> USD\n"
        "7. Withdraw BTC to Mobile Money\n"
        "8. Help\n\n"
        "Reply with a number:"
    ),
    USSDScreen.P2P_TRANSFER_MENU: (
        "SEND BTC TO USER\n"
        "Enter recipient's phone number:\n\n"
        "Example: +256701234567"
    ),
    USSDScreen.SEND_BTC_MENU: (
        "SEND BTC VIA LIGHTNING\n"
        "Enter the Lightning invoice:\n\n"
        "Example: lnbc1000n1p..."
    ),
    USSDScreen.CHECK_BALANCE: (
        "MOBIBIT AFRICA BALANCE\n\n"
        "Reply 0 for main menu."
    ),
    USSDScreen.FUND_ACCOUNT_MENU: (
        "FUND ACCOUNT (Buy BTC)\n"
        "Enter amount in UGX:\n\n"
        "Min: 1,000 | Max: 500,000"
    ),
    USSDScreen.RECEIVE_USD_MENU: (
        "RECEIVE USD\n"
        "Enter amount in USD:\n\n"
        "$1 - $10,000"
    ),
    USSDScreen.SWAP_MENU: (
        "CONVERT BTC <-> USD\n\n"
        "1. BTC -> USD\n"
        "2. USD -> BTC\n\n"
        "Reply 1 or 2:"
    ),
    USSDScreen.WITHDRAW_MENU: (
        "WITHDRAW BTC TO MOBILE MONEY\n"
        "Select provider:\n\n"
        "1. MTN MoMo\n"
        "2. Airtel Money\n"
        "3. Orange Money\n"
        "4. MPESA\n\n"
        "Reply 1-4:"
    ),
    USSDScreen.WITHDRAW_PROVIDER: (
        "WITHDRAW BTC\n"
        "Enter amount in sats:\n\n"
        "Min: 1,000 | Max: 10,000,000"
    ),
    USSDScreen.ERROR: (
        "MOBIBIT AFRICA\n\n"
        "Sorry, an error occurred.\n"
        "Please try again.\n\n"
        "Reply 0 for main menu."
    ),
    USSDScreen.TRANSACTION_RESULT: (
        "MOBIBIT AFRICA\n\n"
        "Reply 0 for main menu."
    ),
    USSDScreen.HELP: (
        "MOBIBIT AFRICA HELP\n\n"
        "How it works:\n"
        "- Fund your account via mobile money\n"
        "- Funds convert to Bitcoin instantly\n"
        "- Send BTC to anyone with a phone\n"
        "- Receive USD payments\n"
        "- Convert BTC <-> USD\n"
        "- Withdraw BTC back to mobile money\n"
        "- Spend with virtual card\n\n"
        "Supported providers:\n"
        "MTN MoMo, Airtel, Orange, MPESA\n\n"
        "Support: +256700000000\n"
        "Web: mobibitafrica.com\n\n"
        "Reply 0 to go back."
    ),
}


class USSDHandler:
    def __init__(self, session_store=None):
        self._sessions = session_store or {}
        self._balance_service = None
        self._payment_service = None
        self._exchange_service = None

    def inject_services(self, balance_service=None, payment_service=None, exchange_service=None):
        self._balance_service = balance_service
        self._payment_service = payment_service
        self._exchange_service = exchange_service

    def handle(self, session_id: str, phone_number: str, user_input: str = "") -> USSDResponse:
        session = self._get_or_create_session(session_id, phone_number)
        session.last_activity = time.time()
        screen = session.current_screen

        try:
            if screen == USSDScreen.MAIN_MENU:
                return self._handle_main_menu(session, user_input)
            elif screen == USSDScreen.CHECK_BALANCE:
                return self._handle_check_balance(session, user_input)
            elif screen == USSDScreen.P2P_TRANSFER_MENU:
                return self._handle_p2p_transfer_menu(session, user_input)
            elif screen == USSDScreen.P2P_TRANSFER_AMOUNT:
                return self._handle_p2p_transfer_amount(session, user_input)
            elif screen == USSDScreen.P2P_TRANSFER_CONFIRM:
                return self._handle_p2p_transfer_confirm(session, user_input)
            elif screen == USSDScreen.SEND_BTC_MENU:
                return self._handle_send_btc_menu(session, user_input)
            elif screen == USSDScreen.WITHDRAW_MENU:
                return self._handle_withdraw_menu(session, user_input)
            elif screen == USSDScreen.WITHDRAW_AMOUNT:
                return self._handle_withdraw_amount(session, user_input)
            elif screen == USSDScreen.WITHDRAW_CONFIRM:
                return self._handle_withdraw_confirm(session, user_input)
            elif screen == USSDScreen.SEND_BTC_MENU:
                return self._handle_send_btc_menu(session, user_input)
            elif screen == USSDScreen.SEND_BTC_AMOUNT:
                return self._handle_send_btc_amount(session, user_input)
            elif screen == USSDScreen.SEND_BTC_CONFIRM:
                return self._handle_send_btc_confirm(session, user_input)
            elif screen == USSDScreen.FUND_ACCOUNT_MENU:
                return self._handle_fund_account_menu(session, user_input)
            elif screen == USSDScreen.FUND_ACCOUNT_CONFIRM:
                return self._handle_fund_account_confirm(session, user_input)
            elif screen == USSDScreen.RECEIVE_USD_MENU:
                return self._handle_receive_usd_menu(session, user_input)
            elif screen == USSDScreen.RECEIVE_USD_CONFIRM:
                return self._handle_receive_usd_confirm(session, user_input)
            elif screen == USSDScreen.SWAP_MENU:
                return self._handle_swap_menu(session, user_input)
            elif screen == USSDScreen.SWAP_AMOUNT:
                return self._handle_swap_amount(session, user_input)
            elif screen == USSDScreen.SWAP_CONFIRM:
                return self._handle_swap_confirm(session, user_input)
            elif screen == USSDScreen.HELP:
                return self._handle_help(session, user_input)
            elif screen == USSDScreen.TRANSACTION_RESULT:
                return self._handle_result(session, user_input)
            else:
                return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)
        except Exception as e:
            logger.error("USSD handler error: %s", e)
            return self._respond(MENUS[USSDScreen.ERROR], USSDScreen.ERROR, session)

    # --- Main Menu ---
    def _handle_main_menu(self, session, input):
        menu = {
            "1": (MENUS.get(USSDScreen.CHECK_BALANCE, ""), USSDScreen.CHECK_BALANCE),
            "2": (MENUS[USSDScreen.P2P_TRANSFER_MENU], USSDScreen.P2P_TRANSFER_MENU),
            "3": (MENUS[USSDScreen.SEND_BTC_MENU], USSDScreen.SEND_BTC_MENU),
            "4": (MENUS[USSDScreen.FUND_ACCOUNT_MENU], USSDScreen.FUND_ACCOUNT_MENU),
            "5": (MENUS[USSDScreen.RECEIVE_USD_MENU], USSDScreen.RECEIVE_USD_MENU),
            "6": (MENUS[USSDScreen.SWAP_MENU], USSDScreen.SWAP_MENU),
            "7": (MENUS[USSDScreen.WITHDRAW_MENU], USSDScreen.WITHDRAW_MENU),
            "8": (MENUS[USSDScreen.HELP], USSDScreen.HELP),
        }
        text, next_screen = menu.get(input, (MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU))
        return self._respond(text, next_screen, session)

    # --- Check Balance ---
    def _handle_check_balance(self, session, input):
        text = (
            "MOBIBIT AFRICA BALANCE\n\n"
            "BTC: 250,000 sats\n"
            "   = 0.00250000 BTC\n"
            "   = $98.75 USD\n\n"
            "USD Wallet: $0.00\n\n"
            "Reply 0 for main menu."
        )
        return self._respond(text, USSDScreen.MAIN_MENU, session)

    # --- P2P Transfer (Send BTC to Another User) ---
    def _handle_p2p_transfer_menu(self, session, input):
        if input == "0":
            return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)
        if not input.startswith("+") or len(input) < 10:
            return self._respond("Invalid phone. Use format: +256701234567\nReply 0 to cancel.", USSDScreen.P2P_TRANSFER_MENU, session)
        session.data["p2p_recipient"] = input
        text = "SEND BTC TO USER\nRecipient: " + input + "\n\nEnter amount in sats (e.g. 10000):"
        return self._respond(text, USSDScreen.P2P_TRANSFER_AMOUNT, session)

    def _handle_p2p_transfer_amount(self, session, input):
        if input == "0":
            return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)
        try:
            amount = int(input)
            if amount <= 0 or amount > 10000000:
                raise ValueError
        except ValueError:
            return self._respond("Invalid amount. Enter 1-10,000,000 sats.\nReply 0 to cancel.", USSDScreen.P2P_TRANSFER_AMOUNT, session)
        session.data["p2p_amount"] = amount
        phone = session.data["p2p_recipient"]
        fee = max(1, int(amount * 0.005))  # 0.5% fee
        total = amount + fee
        text = (
            "SEND BTC - CONFIRM\n"
            "To: " + phone + "\n"
            "Amount: " + f"{amount:,}" + " sats\n"
            "Fee: " + f"{fee:,}" + " sats\n"
            "Total: " + f"{total:,}" + " sats\n\n"
            "1. Confirm & Send\n"
            "2. Cancel\n\n"
            "Reply 1 or 2:"
        )
        return self._respond(text, USSDScreen.P2P_TRANSFER_CONFIRM, session)

    def _handle_p2p_transfer_confirm(self, session, input):
        if input == "1":
            phone = session.data["p2p_recipient"]
            amount = session.data["p2p_amount"]
            fee = max(1, int(amount * 0.005))
            text = (
                "BTC SENT!\n\n"
                "To: " + phone + "\n"
                "Amount: " + f"{amount:,}" + " sats\n"
                "Fee: " + f"{fee:,}" + " sats\n"
                "Status: Confirmed\n\n"
                "Reply 0 for main menu."
            )
            return self._respond(text, USSDScreen.MAIN_MENU, session)
        return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)

    # --- Send BTC via Lightning ---
    def _handle_send_btc_menu(self, session, input):
        if input == "0":
            return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)
        if not input.startswith("+") or len(input) < 10:
            return self._respond("Invalid phone. Use format: +256701234567\nReply 0 to cancel.", USSDScreen.SEND_BTC_MENU, session)
        session.data["recipient_phone"] = input
        text = "SEND BTC\nRecipient: " + input + "\n\nEnter amount in sats (e.g. 10000):"
        return self._respond(text, USSDScreen.SEND_BTC_AMOUNT, session)

    def _handle_send_btc_amount(self, session, input):
        if input == "0":
            return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)
        try:
            amount = int(input)
            if amount <= 0 or amount > 10000000:
                raise ValueError
        except ValueError:
            return self._respond("Invalid amount. Enter 1-10,000,000 sats.\nReply 0 to cancel.", USSDScreen.SEND_BTC_AMOUNT, session)
        session.data["amount_sats"] = amount
        phone = session.data["recipient_phone"]
        usd_est = round(amount * 0.000025, 2)
        text = (
            "SEND BTC - CONFIRM\n"
            "To: " + phone + "\n"
            "Amount: " + f"{amount:,}" + " sats\n"
            "Fee: ~1 sat\n\n"
            "1. Confirm & Send\n"
            "2. Cancel\n\n"
            "Reply 1 or 2:"
        )
        return self._respond(text, USSDScreen.SEND_BTC_CONFIRM, session)

    def _handle_send_btc_confirm(self, session, input):
        if input == "1":
            phone = session.data["recipient_phone"]
            amount = session.data["amount_sats"]
            text = (
                "BTC SENT!\n\n"
                "To: " + phone + "\n"
                "Amount: " + f"{amount:,}" + " sats\n"
                "Status: Confirmed\n\n"
                "Reply 0 for main menu."
            )
            return self._respond(text, USSDScreen.MAIN_MENU, session)
        return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)

    # --- Fund Account (Buy BTC) ---
    def _handle_fund_account_menu(self, session, input):
        if input == "0":
            return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)
        try:
            amount = float(input)
            if amount < 1000 or amount > 500000:
                raise ValueError
        except ValueError:
            return self._respond("Invalid amount. Min: 1,000 | Max: 500,000 UGX\nReply 0 to cancel.", USSDScreen.FUND_ACCOUNT_MENU, session)
        session.data["fund_amount"] = amount
        sats_est = int(amount / 3700 * 100000000)
        text = (
            "FUND ACCOUNT - CONFIRM\n"
            "Amount: " + f"{amount:,.0f}" + " UGX\n"
            "You will receive: " + f"{sats_est:,}" + " sats\n\n"
            "A payment prompt will be sent to your phone.\n\n"
            "1. Confirm\n"
            "2. Cancel\n\n"
            "Reply 1 or 2:"
        )
        return self._respond(text, USSDScreen.FUND_ACCOUNT_CONFIRM, session)

    def _handle_fund_account_confirm(self, session, input):
        if input == "1":
            amount = session.data.get("fund_amount", 0)
            text = (
                "FUND REQUEST SENT\n\n"
                "Amount: " + f"{amount:,.0f}" + " UGX\n"
                "You will receive a payment prompt on your phone.\n\n"
                "Reply 0 for main menu."
            )
            return self._respond(text, USSDScreen.MAIN_MENU, session)
        return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)

    # --- Receive USD ---
    def _handle_receive_usd_menu(self, session, input):
        if input == "0":
            return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)
        try:
            amount = float(input)
            if amount <= 0 or amount > 10000:
                raise ValueError
        except ValueError:
            return self._respond("Enter amount between $1 and $10,000.\nReply 0 to cancel.", USSDScreen.RECEIVE_USD_MENU, session)
        session.data["receive_usd_amount"] = amount
        text = (
            "RECEIVE USD - CONFIRM\n"
            "Amount: $" + f"{amount:,.2f}" + " USD\n\n"
            "A payment request will be sent.\n\n"
            "1. Confirm\n"
            "2. Cancel\n\n"
            "Reply 1 or 2:"
        )
        return self._respond(text, USSDScreen.RECEIVE_USD_CONFIRM, session)

    def _handle_receive_usd_confirm(self, session, input):
        if input == "1":
            amount = session.data.get("receive_usd_amount", 0)
            text = (
                "USD PAYMENT REQUEST SENT\n\n"
                "Amount: $" + f"{amount:,.2f}" + " USD\n"
                "A payment request has been created.\n"
                "Share the invoice with the sender.\n\n"
                "Reply 0 for main menu."
            )
            return self._respond(text, USSDScreen.MAIN_MENU, session)
        return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)

    # --- Swap BTC <-> USD ---
    def _handle_swap_menu(self, session, input):
        if input == "0":
            return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)
        if input == "1":
            session.data["swap_from"] = "BTC"
            session.data["swap_to"] = "USD"
            text = "SWAP BTC -> USD\n\nEnter amount in sats:"
            return self._respond(text, USSDScreen.SWAP_AMOUNT, session)
        elif input == "2":
            session.data["swap_from"] = "USD"
            session.data["swap_to"] = "BTC"
            text = "SWAP USD -> BTC\n\nEnter amount in USD:"
            return self._respond(text, USSDScreen.SWAP_AMOUNT, session)
        return self._respond("Reply 1 for BTC->USD or 2 for USD->BTC.", USSDScreen.SWAP_MENU, session)

    def _handle_swap_amount(self, session, input):
        if input == "0":
            return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)
        try:
            amount = float(input)
            if amount <= 0:
                raise ValueError
        except ValueError:
            return self._respond("Invalid amount. Reply 0 to cancel.", USSDScreen.SWAP_AMOUNT, session)
        from_cur = session.data.get("swap_from", "BTC")
        to_cur = session.data.get("swap_to", "USD")
        if from_cur == "BTC":
            converted = round(amount * 0.000025 * 100, 2)
            text = "SWAP CONFIRM\n" + f"{amount:,}" + " sats -> $" + f"{converted:,.2f}" + " USD\n\n1. Confirm Swap\n2. Cancel"
        else:
            converted = int(amount * 40000)
            text = "SWAP CONFIRM\n$" + f"{amount:,.2f}" + " USD -> " + f"{converted:,}" + " sats\n\n1. Confirm Swap\n2. Cancel"
        session.data["swap_amount"] = amount
        return self._respond(text, USSDScreen.SWAP_CONFIRM, session)

    def _handle_swap_confirm(self, session, input):
        if input == "1":
            from_cur = session.data.get("swap_from", "BTC")
            amount = session.data.get("swap_amount", 0)
            text = "SWAP COMPLETED\n\n" + f"{amount}" + " " + from_cur + " converted successfully.\n\nReply 0 for main menu."
            return self._respond(text, USSDScreen.MAIN_MENU, session)
        return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)

    # --- Withdraw BTC to Mobile Money ---
    def _handle_withdraw_menu(self, session, input):
        if input == "0":
            return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)
        providers = {
            "1": "mtn_momo",
            "2": "airtel_money",
            "3": "orange_money",
            "4": "mpesa",
        }
        provider = providers.get(input)
        if not provider:
            return self._respond("Invalid provider. Reply 1-4.", USSDScreen.WITHDRAW_MENU, session)
        session.data["withdraw_provider"] = provider
        text = (
            "WITHDRAW BTC TO " + provider.upper().replace("_", " ") + "\n"
            "Enter amount in sats:\n\n"
            "Min: 1,000 | Max: 10,000,000"
        )
        return self._respond(text, USSDScreen.WITHDRAW_AMOUNT, session)

    def _handle_withdraw_amount(self, session, input):
        if input == "0":
            return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)
        try:
            amount = int(input)
            if amount < 1000 or amount > 10000000:
                raise ValueError
        except ValueError:
            return self._respond("Invalid amount. Min: 1,000 | Max: 10,000,000 sats.\nReply 0 to cancel.", USSDScreen.WITHDRAW_AMOUNT, session)
        session.data["withdraw_amount"] = amount
        provider = session.data.get("withdraw_provider", "mpesa")
        # Calculate conversion (sats → USD → local currency)
        usd_est = round(amount * 0.000025 * 0.98, 2)  # 2% fee
        if provider == "mpesa":
            fiat_est = round(usd_est * 130, 0)  # KES
            currency = "KES"
        elif provider in ["mtn_momo", "airtel_money"]:
            fiat_est = round(usd_est * 3700, 0)  # UGX
            currency = "UGX"
        else:
            fiat_est = round(usd_est * 600, 0)  # XOF
            currency = "XOF"
        text = (
            "WITHDRAW CONFIRM\n"
            "Amount: " + f"{amount:,}" + " sats\n"
            "You will receive: " + f"{fiat_est:,.0f}" + " " + currency + "\n"
            "Fee: ~2%\n"
            "Provider: " + provider.upper().replace("_", " ") + "\n\n"
            "1. Confirm Withdraw\n"
            "2. Cancel\n\n"
            "Reply 1 or 2:"
        )
        return self._respond(text, USSDScreen.WITHDRAW_CONFIRM, session)

    def _handle_withdraw_confirm(self, session, input):
        if input == "1":
            amount = session.data.get("withdraw_amount", 0)
            provider = session.data.get("withdraw_provider", "mpesa")
            text = (
                "WITHDRAWAL INITIATED\n\n"
                "Amount: " + f"{amount:,}" + " sats\n"
                "Provider: " + provider.upper().replace("_", " ") + "\n"
                "Status: Processing\n\n"
                "You will receive an SMS confirmation.\n"
                "Reply 0 for main menu."
            )
            return self._respond(text, USSDScreen.MAIN_MENU, session)
        return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)

    # --- Help ---
    def _handle_help(self, session, input):
        return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)

    # --- Result ---
    def _handle_result(self, session, input):
        return self._respond(MENUS[USSDScreen.MAIN_MENU], USSDScreen.MAIN_MENU, session)

    # --- Helpers ---
    def _get_or_create_session(self, session_id, phone_number):
        if session_id not in self._sessions:
            self._sessions[session_id] = USSDSession(session_id=session_id, phone_number=phone_number)
        return self._sessions[session_id]

    def _respond(self, text, next_screen, session, continue_session=True):
        session.current_screen = next_screen
        return USSDResponse(text=text, continue_session=continue_session)
