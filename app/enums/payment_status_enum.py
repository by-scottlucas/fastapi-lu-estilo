from enum import Enum

class PaymentStatusEnum(str, Enum):
    PENDING = "pending"         
    PAID = "paid"               
    FAILED = "failed"           
    CANCELED = "canceled"      
    REFUNDED = "refunded" 