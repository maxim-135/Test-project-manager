from typing import Dict, Any, List
from unified_manager.logging_config import get_logger

logger = get_logger(__name__)

class ContractManager:
    def __init__(self):
        self.contracts: Dict[str, Any] = {}

    def register_contract(self, contract_id: str, provider: str, consumer: str, input_schema: Dict, output_schema: Dict):
        self.contracts[contract_id] = {
            "provider": provider,
            "consumer": consumer,
            "input_schema": input_schema,
            "output_schema": output_schema
        }

    def get_contract(self, contract_id: str) -> Dict[str, Any]:
        return self.contracts.get(contract_id)

    def list_contracts(self) -> List[Dict[str, Any]]:
        return list(self.contracts.values())

_contract_manager: ContractManager = None

def get_contract_manager() -> ContractManager:
    global _contract_manager
    if _contract_manager is None:
        _contract_manager = ContractManager()
    return _contract_manager
