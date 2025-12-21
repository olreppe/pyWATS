from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Type, TypeVar
from pydantic import BaseModel, ConfigDict


class ToolInput(BaseModel):
    model_config = ConfigDict(extra="forbid")


TInput = TypeVar("TInput", bound=ToolInput)


class AgentToolV2(ABC, Generic[TInput]):
    """Canonical tool interface for the SDK-side agent layer."""

    name: str
    description: str
    input_model: Type[TInput]

    def __init__(self, api: Any):
        self._api = api

    @classmethod
    def openai_definition(cls) -> Dict[str, Any]:
        schema = cls.input_model.model_json_schema()
        return {
            "name": cls.name,
            "description": cls.description,
            "parameters": {
                "type": "object",
                "properties": schema.get("properties", {}),
                "required": schema.get("required", []),
            },
        }

    def execute(self, params: Dict[str, Any]) -> tuple[bool, str, Any, dict[str, Any]]:
        """Executes tool and returns (ok, summary, data, metadata).

        Data can be arbitrarily large; the executor will store it in a DataStore.
        """
        input_obj = self.input_model.model_validate(params)
        return self.run(input_obj)

    @abstractmethod
    def run(self, input_obj: TInput) -> tuple[bool, str, Any, dict[str, Any]]:
        raise NotImplementedError
