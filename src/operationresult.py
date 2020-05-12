from enum import Enum

class OperationResult(Enum):
    Success = 1
    InsufficientFunds = 2
    NotAllowed = 3