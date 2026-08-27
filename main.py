from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import subprocess
import json


app = FastAPI(
    title="Sats Card API",
    description="Backend API for Sats Card",
    version="1.0.0"
)


# ============================================================
# POLAR NETWORK CONFIGURATION
# ============================================================

ALICE_CONTAINER = "polar-n1-alice"
BOB_CONTAINER = "polar-n1-bob"


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_URL = "sqlite:///./sats_card.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, unique=True, nullable=False)
    balance_sats = Column(Integer, default=0, nullable=False)

class Deposit(Base):
    __tablename__ = "deposits"

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(String, unique=True, nullable=False)
    amount_sats = Column(Integer, nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=True
    )



Base.metadata.create_all(bind=engine)
# ============================================================
# DATABASE MIGRATION
# ============================================================

def migrate_database():

    with engine.connect() as connection:

        result = connection.execute(
            text("PRAGMA table_info(deposits)")
        )

        columns = [
            row[1]
            for row in result.fetchall()
        ]

        if "created_at" not in columns:

            connection.execute(
                text(
                    "ALTER TABLE deposits "
                    "ADD COLUMN created_at DATETIME"
                )
            )

            connection.commit()


migrate_database()



# ============================================================
# INITIALIZE DEFAULT CARD
# ============================================================

def initialize_card():
    db = SessionLocal()

    try:
        card = db.query(Card).filter(
            Card.card_number == "SATSCARD-001"
        ).first()

        if card is None:
            card = Card(
                card_number="SATSCARD-001",
                balance_sats=0
            )

            db.add(card)
            db.commit()

    finally:
        db.close()


initialize_card()


# ============================================================
# REQUEST MODELS
# ============================================================

class InvoiceRequest(BaseModel):
    amount_sats: int = Field(..., gt=0)
    memo: str = "Sats Card Payment"


class PaymentRequest(BaseModel):
    payment_request: str


# ============================================================
# LNCLI HELPER
# ============================================================

def run_lncli(container: str, command: list):

    result = subprocess.run(
        [
            "docker",
            "exec",
            container,
            "lncli",
            "--lnddir=/home/lnd/.lnd",
            "--network=regtest",
            *command
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(result.stderr.strip())

    try:
        return json.loads(result.stdout)

    except json.JSONDecodeError:
        raise Exception("Invalid JSON returned by lncli")


# ============================================================
# BASIC ENDPOINTS
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Welcome to Sats Card API",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# NODE INFORMATION
# ============================================================

@app.get("/api/node_info")
def node_info():

    try:

        data = run_lncli(
            ALICE_CONTAINER,
            ["getinfo"]
        )

        return {
            "alias": data["alias"],
            "network": data["chains"][0]["network"],
            "block_height": data["block_height"],
            "num_active_channels": data["num_active_channels"],
            "num_peers": data["num_peers"],
            "synced_to_chain": data["synced_to_chain"],
            "synced_to_graph": data["synced_to_graph"]
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# CREATE LIGHTNING INVOICE
# ============================================================

@app.post("/api/create_invoice")
def create_invoice(request: InvoiceRequest):

    try:

        data = run_lncli(
            ALICE_CONTAINER,
            [
                "addinvoice",
                "--amt",
                str(request.amount_sats),
                "--memo",
                request.memo
            ]
        )

        return {
            "status": "created",
            "amount_sats": request.amount_sats,
            "memo": request.memo,
            "payment_request": data["payment_request"],
            "payment_hash": data["r_hash"]
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# CHECK PAYMENT
# ============================================================

@app.get("/api/check_payment/{payment_id}")
def check_payment(payment_id: str):

    try:

        data = run_lncli(
            ALICE_CONTAINER,
            [
                "lookupinvoice",
                payment_id
            ]
        )

        return {
            "payment_id": payment_id,
            "status": "paid" if data["settled"] else "pending",
            "amount_sats": int(data["value"]),
            "settled": data["settled"]
        }

    except Exception as e:

        return {
            "payment_id": payment_id,
            "status": "error",
            "message": str(e)
        }


# ============================================================
# LIGHTNING WALLET BALANCE
# ============================================================

@app.get("/api/balance")
def balance():

    try:

        data = run_lncli(
            ALICE_CONTAINER,
            ["walletbalance"]
        )

        return {
            "total_balance_sats": int(data["total_balance"]),
            "confirmed_balance_sats": int(
                data["confirmed_balance"]
            ),
            "unconfirmed_balance_sats": int(
                data["unconfirmed_balance"]
            )
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# CHANNEL BALANCE
# ============================================================

@app.get("/api/channel_balance")
def channel_balance():

    try:

        data = run_lncli(
            ALICE_CONTAINER,
            ["channelbalance"]
        )

        return {
            "balance_sats": int(data["balance"]),
            "local_balance_sats": int(
                data["local_balance"]["sat"]
            ),
            "remote_balance_sats": int(
                data["remote_balance"]["sat"]
            ),
            "pending_open_balance_sats": int(
                data["pending_open_balance"]
            )
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# LIST CHANNELS
# ============================================================

@app.get("/api/channels")
def channels():

    try:

        data = run_lncli(
            ALICE_CONTAINER,
            ["listchannels"]
        )

        return {
            "channels": data["channels"],
            "count": len(data["channels"])
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# LIST PEERS
# ============================================================

@app.get("/api/peers")
def peers():

    try:

        data = run_lncli(
            ALICE_CONTAINER,
            ["listpeers"]
        )

        return {
            "peers": data["peers"],
            "count": len(data["peers"])
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# DEPOSIT PAYMENT INTO SATS CARD
# ============================================================

@app.post("/api/deposit/{payment_id}")
def deposit_to_card(payment_id: str):

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # Prevent double deposits
        # ----------------------------------------------------

        existing_deposit = db.query(Deposit).filter(
            Deposit.payment_id == payment_id
        ).first()

        if existing_deposit:

            raise HTTPException(
                status_code=400,
                detail="This payment has already been deposited"
            )


        # ----------------------------------------------------
        # Check Lightning invoice
        # ----------------------------------------------------

        data = run_lncli(
            ALICE_CONTAINER,
            [
                "lookupinvoice",
                payment_id
            ]
        )


        if not data["settled"]:

            return {
                "status": "pending",
                "message": "Payment has not been settled yet",
                "payment_id": payment_id
            }


        # ----------------------------------------------------
        # Get payment amount
        # ----------------------------------------------------

        amount = int(data["value"])


        # ----------------------------------------------------
        # Get card
        # ----------------------------------------------------

        card = db.query(Card).filter(
            Card.card_number == "SATSCARD-001"
        ).first()


        if card is None:

            raise HTTPException(
                status_code=404,
                detail="Card not found"
            )


        # ----------------------------------------------------
        # Update balance
        # ----------------------------------------------------

        card.balance_sats += amount


        # ----------------------------------------------------
        # Record deposit
        # ----------------------------------------------------

        deposit = Deposit(
            payment_id=payment_id,
            amount_sats=amount
        )

        db.add(deposit)

        db.commit()

        db.refresh(card)


        return {
            "status": "deposited",
            "payment_id": payment_id,
            "amount_sats": amount,
            "card_number": card.card_number,
            "card_balance_sats": card.balance_sats
        }


    except HTTPException:
        raise


    except Exception as e:

        db.rollback()

        return {
            "status": "error",
            "message": str(e)
        }


    finally:

        db.close()


# ============================================================
# CARD BALANCE
# ============================================================

@app.get("/api/card_balance")
def get_card_balance():

    db = SessionLocal()

    try:

        card = db.query(Card).filter(
            Card.card_number == "SATSCARD-001"
        ).first()


        if card is None:

            raise HTTPException(
                status_code=404,
                detail="Card not found"
            )


        return {
            "card_number": card.card_number,
            "card_balance_sats": card.balance_sats
        }


    finally:

        db.close()


# ============================================================
# DEPOSIT HISTORY
# ============================================================

@app.get("/api/deposits")
def deposit_history():

    db = SessionLocal()

    try:

        deposits = db.query(Deposit).all()

        return {
    "deposits": [
        {
            "payment_id": deposit.payment_id,
            "amount_sats": deposit.amount_sats,
            "created_at": (
                deposit.created_at.isoformat()
                if deposit.created_at
                else None
            )
        }
        for deposit in deposits
    ],
    "count": len(deposits)
}
    finally:

        db.close()
# ============================================================
# LIGHTNING PAYMENT HISTORY
# ============================================================

@app.get("/api/payments")
def payment_history():

    try:

        data = run_lncli(
            ALICE_CONTAINER,
            ["listinvoices"]
        )

        payments = []

        for invoice in data["invoices"]:

            payments.append(
                {
                    "payment_hash": invoice["r_hash"],
                    "memo": invoice["memo"],
                    "amount_sats": int(invoice["value"]),
                    "amount_paid_sats": int(
                        invoice.get("amt_paid_sat", 0)
                    ),
                    "status": (
                        "paid"
                        if invoice["settled"]
                        else "pending"
                    ),
                    "settled": invoice["settled"],
                    "creation_date": invoice["creation_date"],
                    "settle_date": invoice["settle_date"]
                }
            )

        return {
            "payments": payments,
            "count": len(payments)
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
# ============================================================
# SATS CARD TRANSACTION SUMMARY
# ============================================================

@app.get("/api/transactions")
def transaction_history():

    db = SessionLocal()

    try:

        deposits = db.query(Deposit).order_by(
            Deposit.id.desc()
        ).all()

        transactions = []

        for deposit in deposits:

            transactions.append(
                {
                    "transaction_id": deposit.id,
                    "type": "deposit",
                    "payment_id": deposit.payment_id,
                    "amount_sats": deposit.amount_sats,
                    "status": "completed",
                       "created_at": (
                        deposit.created_at.isoformat()
                        if deposit.created_at
                        else None
    )
                }
            )

        return {
            "transactions": transactions,
            "count": len(transactions)
        }

    finally:

        db.close()
