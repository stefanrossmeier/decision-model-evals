from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal
import json

Primitive = Literal["choice", "noul", "score"]


@dataclass(frozen=True)
class Gold:
    choice: str | None = None
    noul: bool | None = None
    score: int | None = None
    rationale: str = ""


@dataclass(frozen=True)
class Case:
    id: str
    primitive: Primitive
    domain: str
    task: str
    state: Any
    instructions: str
    criteria: dict[str, str] | list[str] | None
    gold: Gold
    tags: tuple[str, ...]
    metadata: dict[str, Any]

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Case":
        primitive = raw.get("primitive")
        if primitive not in {"choice", "noul", "score"}:
            raise ValueError(f"invalid primitive for {raw.get('id')}: {primitive!r}")
        gold_raw = raw.get("gold") or {}
        gold = Gold(
            choice=gold_raw.get("choice"),
            noul=gold_raw.get("noul"),
            score=gold_raw.get("score"),
            rationale=gold_raw.get("rationale", ""),
        )
        case = cls(
            id=str(raw["id"]),
            primitive=primitive,
            domain=str(raw["domain"]),
            task=str(raw["task"]),
            state=raw["state"],
            instructions=str(raw["instructions"]),
            criteria=raw.get("criteria"),
            gold=gold,
            tags=tuple(raw.get("tags") or ()),
            metadata=dict(raw.get("metadata") or {}),
        )
        case.validate()
        return case

    def validate(self) -> None:
        if not self.id or not self.domain or not self.task or not self.instructions:
            raise ValueError(f"case {self.id!r} has required empty fields")
        if self.primitive == "choice":
            if not isinstance(self.criteria, dict) or len(self.criteria) < 2:
                raise ValueError(f"choice case {self.id} needs a criteria mapping with >=2 options")
            if self.gold.choice not in self.criteria:
                raise ValueError(f"choice gold {self.gold.choice!r} not in criteria for {self.id}")
        elif self.primitive == "noul":
            if self.gold.noul is None:
                raise ValueError(f"noul case {self.id} needs boolean gold")
            if self.criteria is not None and not isinstance(self.criteria, dict):
                raise ValueError(f"noul criteria for {self.id} must be mapping or null")
        else:
            if not isinstance(self.criteria, list) or not (2 <= len(self.criteria) <= 10):
                raise ValueError(f"score case {self.id} needs 2..10 ordered levels")
            if self.gold.score is None or not 0 <= self.gold.score < len(self.criteria):
                raise ValueError(f"score gold out of range for {self.id}")

    def question_payload(self) -> dict[str, Any]:
        question: dict[str, Any] = {
            "type": self.primitive,
            "instructions": self.instructions,
        }
        if self.criteria is not None:
            question["criteria"] = self.criteria
        return question


def load_corpus(path: Path) -> list[Case]:
    cases: list[Case] = []
    seen: set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            case = Case.from_dict(raw)
            if case.id in seen:
                raise ValueError(f"duplicate case id {case.id!r} at {path}:{line_no}")
            seen.add(case.id)
            cases.append(case)
    if not cases:
        raise ValueError(f"corpus is empty: {path}")
    return cases
