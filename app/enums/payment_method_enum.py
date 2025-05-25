from enum import Enum

class PaymentMethodEnum(str, Enum):
    PIX = "pix"
    BANK_SLIP = "bank_slip"
    DEBIT_CARD = "debit_card"
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"