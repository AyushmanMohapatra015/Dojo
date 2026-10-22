

\## Batch A Delivery Manifest \& WP1–WP5 Checklist







\### File and Dependency Manifest







| File Path | Role in Batch A | Runtime / Test Dependencies |

| --- | --- | --- |

| `dojo/bench/records.py` | \*\*WP1\*\*: Immutable normalized record/plan/audit DTOs, strict bounded JSON parsing, canonical SHA-256 identity, complete panel \& evidence validation.



&#x20;| Python standard library (`dataclasses`, `fractions`, `hashlib`, `json`, `math`, `re`, `typing`) + `dojo.solve.signals.ObservableSignals`<br> |

| `dojo/bench/stats.py` | \*\*WP2, WP3, WP4\*\*: Reusable `TaskSeries` / `SeriesPoint` abstractions, exact `Fraction` primary metrics, paired task bootstrap, family-cluster bootstrap, and seed sensitivity.



&#x20;| Python standard library (`dataclasses`, `fractions`, `math`, `random`, `typing`) + `dojo.bench.records`<br> |

| `dojo/bench/frontier.py` | \*\*WP5\*\*: Exact rational Pareto non-dominance and tie-group evaluation across both `cost\_per\_solved` and `mean\_task\_cost` axes, with undefined-point exclusion.



&#x20;| Python standard library (`dataclasses`, `fractions`, `typing`) + `dojo.bench.records`, `dojo.bench.stats`<br> |

| `tests/test\_analysis\_records.py` | \*\*WP1 Acceptance Tests\*\*: Valid/invalid fixture parsing, duplicate JSON keys, lone surrogates, bool/int/float traps, candidate\_error baseline rules, canonical hashes.



&#x20;| `pytest` + `dojo.bench.records`<br> |

| `tests/test\_statistics.py` | \*\*WP2–WP5 Acceptance Tests\*\*: Exact known-answer arithmetic, unequal seeds, injectable paired bootstrap indices, zero-solve draws, RNG isolation, family/seed sensitivity, and frontiers.



&#x20;| `pytest` + `dojo.bench.records`, `dojo.bench.stats`, `dojo.bench.frontier`<br> |

| `tests/fixtures/analysis/valid\_panel.json` | 4-task synthetic train panel fixture (without `expected` test annotation).



&#x20;| JSON data



&#x20;|

| `tests/fixtures/analysis/unequal\_seed\_panel.json` | 1-task unequal-seed (`A: \[0, 1]`, `B: \[0]`) synthetic fixture (without `expected` test annotation).



&#x20;| JSON data



&#x20;|

| `tests/fixtures/analysis/invalid\_panel.json` | Deliberately invalid panel fixture missing `B/synthetic\_stats\_4/0` and duplicating `A/synthetic\_stats\_1/0` (without `expected` test annotation).



&#x20;| JSON data



&#x20;|

| `docs/analysis-foundation-methods.md` | Mathematical specification, estimands, quantile rules, zero-solve handling, sensitivity weighting, and inference limitations.



&#x20;| Markdown documentation



&#x20;|

| `docs/analysis-foundation-api.md` | Public symbols, exact signatures, DTO schemas, Batch B cascade extension seams, limits, and executable usage examples.



&#x20;| Markdown documentation



&#x20;|



\---



\### Work Package Completion Checklist (WP1–WP5 Only)







| WP | Plan Scope | Status | Deliverable \& Verification Summary |

| --- | --- | --- | --- |

| \*\*WP1\*\* | 9a / 9h | \*\*COMPLETE (UNEXECUTED)\*\* | `dojo/bench/records.py` \& `tests/test\_analysis\_records.py`: Enforces 1 MiB byte limit, JSON nesting depth $\\le 32$, $\\le 10,000$ records, duplicate-key rejection, lone surrogate (`\\uD800`–`\\uDFFF`) and huge-exponent rejection, strict `bool` vs `int` checks, `scorer\_status`/`outcome`/`evidence\_validity`/`baseline\_verified` matrix, exact expected-plan coverage, and record-order-invariant canonical SHA-256 digests.



&#x20;|

| \*\*WP2\*\* | 9a | \*\*COMPLETE (UNEXECUTED)\*\* | `dojo/bench/stats.py` \& `tests/test\_statistics.py`: Computes equal-task-weighted `pass\_at\_1`, expected 1-seed total cost (`expected\_total\_cost\_nanos`), `mean\_task\_cost\_nanos`, `expected\_cost\_per\_solved\_nanos`, and `actual\_all\_repetitions\_spend\_nanos` using exact `Fraction` and `int` arithmetic. Secondary metrics (`turns`, `commands`, `actual\_prompt\_tokens`, `actual\_completion\_tokens`, `wall\_seconds`, `hit\_step\_cap`, `no\_command\_rate`) report known/missing counts without inferring `0`.



&#x20;|

| \*\*WP3\*\* | 9b / 9c | \*\*COMPLETE (UNEXECUTED)\*\* | `dojo/bench/stats.py` \& `tests/test\_statistics.py`: Paired task bootstrap with default 10,000 replicates, local `random.Random(seed)` RNG isolation, injectable `sampled\_task\_indices` for index-level pairing tests, workload cap ($\\le 10,000,000$ task-series evaluations), explicit `zero\_solve\_draws`, blocked unconditional intervals when any resample has 0 solves, and paired deltas (`B - A`).



&#x20;|

| \*\*WP4\*\* | 9f | \*\*COMPLETE (UNEXECUTED)\*\* | `dojo/bench/stats.py` \& `tests/test\_statistics.py`: Family-cluster bootstrap (`family\_cluster\_bootstrap`) resampling families with replacement while preserving the original-$n$ total cost target ($n \\times \\bar{m}^\*$), and `seed\_sensitivity\_analysis` evaluating predeclared seed positions (`k`-th seed) and explicit seed subsets without held-out selection.



&#x20;|

| \*\*WP5\*\* | 9c | \*\*COMPLETE (UNEXECUTED)\*\* | `dojo/bench/frontier.py` \& `tests/test\_statistics.py`: Exact `Fraction` Pareto frontier evaluation on both `cost\_per\_solved` and `mean\_task\_cost` vs `pass\_at\_1`. Separates `undefined\_cost` configs (e.g., zero solves or missing costs) so they never dominate or get dominated by valid points, and groups exact rational ties into deterministic `tie\_group` IDs.



&#x20;|

| \*\*WP6–10\*\* | Batch B | \*\*DEFERRED\*\* | Policies, frozen train selection, cold-restart cascade composition, report export, and offline CLI are intentionally deferred per Batch A instructions.



&#x20;|



\---



\## FILE: dojo/bench/records.py



```python

"""WP1: Normalized immutable analysis records, expected plan, bounded JSON parser, and panel audit."""



from \_\_future\_\_ import annotations



import hashlib

import json

import math

import re

from collections.abc import Mapping, Sequence

from dataclasses import dataclass

from fractions import Fraction

from typing import Any



from dojo.solve.signals import ObservableSignals



SCHEMA\_VERSION: int = 1

FOUNDATION\_METHOD\_VERSION: str = "dojo-stats-foundation-v1"



MAX\_INPUT\_BYTES: int = 1\_048\_576  # 1 MiB

MAX\_JSON\_DEPTH: int = 32

MAX\_RECORDS: int = 10\_000

MAX\_COST\_NANO\_USD: int = 10\*\*18  # 1 billion USD in nano-USD

MAX\_COUNT\_VALUE: int = 10\*\*12

MAX\_WALL\_SECONDS: float = 10\*\*7

MAX\_STRING\_LENGTH: int = 256

MAX\_NUMBER\_TOKEN\_CHARS: int = 64



VALID\_SPLITS: frozenset\[str] = frozenset({"train", "held\_out"})

VALID\_EVIDENCE\_KINDS: frozenset\[str] = frozenset({"synthetic", "real"})

VALID\_OUTCOMES: frozenset\[str] = frozenset({"solved", "unsolved", "undetermined"})

VALID\_EVIDENCE\_VALIDITIES: frozenset\[str] = frozenset({"valid", "invalid", "unknown"})

VALID\_SCORER\_STATUSES: frozenset\[str] = frozenset(

&#x20;   {

&#x20;       "passed",

&#x20;       "failed",

&#x20;       "candidate\_error",

&#x20;       "invalid\_evidence",

&#x20;       "infrastructure\_error",

&#x20;   }

)



REQUIRED\_ENVELOPE\_KEYS: frozenset\[str] = frozenset(

&#x20;   {

&#x20;       "schema\_version",

&#x20;       "evidence\_kind",

&#x20;       "dataset\_id",

&#x20;       "expected\_plan",

&#x20;       "records",

&#x20;   }

)

REQUIRED\_PLAN\_KEYS: frozenset\[str] = frozenset({"tasks", "seeds\_by\_config"})

REQUIRED\_SIGNAL\_KEYS: frozenset\[str] = frozenset(

&#x20;   {

&#x20;       "has\_patch",

&#x20;       "visible\_tests\_pass",

&#x20;       "hit\_step\_cap",

&#x20;       "no\_command\_rate",

&#x20;       "agent\_self\_reports\_done",

&#x20;   }

)

REQUIRED\_RECORD\_KEYS: frozenset\[str] = frozenset(

&#x20;   {

&#x20;       "task\_id",

&#x20;       "config\_id",

&#x20;       "seed",

&#x20;       "split",

&#x20;       "family\_id",

&#x20;       "dataset\_id",

&#x20;       "evidence\_kind",

&#x20;       "registration\_id",

&#x20;       "execution\_complete",

&#x20;       "outcome",

&#x20;       "evidence\_validity",

&#x20;       "scorer\_status",

&#x20;       "baseline\_verified",

&#x20;       "cost\_nano\_usd",

&#x20;       "signals",

&#x20;   }

)

OPTIONAL\_RECORD\_KEYS: frozenset\[str] = frozenset(

&#x20;   {

&#x20;       "turns",

&#x20;       "commands",

&#x20;       "actual\_prompt\_tokens",

&#x20;       "actual\_completion\_tokens",

&#x20;       "wall\_seconds",

&#x20;   }

)

ALLOWED\_RECORD\_KEYS: frozenset\[str] = REQUIRED\_RECORD\_KEYS | OPTIONAL\_RECORD\_KEYS



\_SURROGATE\_ESCAPE\_RE = re.compile(r"\\\\u\[dD]\[89a-fA-F]\[0-9a-fA-F]{2}")

\_NUMBER\_TOKEN\_RE = re.compile(r"-?(?:0|\[1-9]\\d\*)(?:\\.\\d+)?(?:\[eE]\[+-]?\\d+)?")



\_\_all\_\_ = \[

&#x20;   "ALLOWED\_RECORD\_KEYS",

&#x20;   "AnalysisInputError",

&#x20;   "AuditFinding",

&#x20;   "EligibilityStatus",

&#x20;   "ExpectedPlan",

&#x20;   "FOUNDATION\_METHOD\_VERSION",

&#x20;   "MAX\_COST\_NANO\_USD",

&#x20;   "MAX\_COUNT\_VALUE",

&#x20;   "MAX\_INPUT\_BYTES",

&#x20;   "MAX\_JSON\_DEPTH",

&#x20;   "MAX\_RECORDS",

&#x20;   "NormalizedEnvelope",

&#x20;   "NormalizedRecord",

&#x20;   "OPTIONAL\_RECORD\_KEYS",

&#x20;   "PanelAudit",

&#x20;   "REQUIRED\_ENVELOPE\_KEYS",

&#x20;   "REQUIRED\_PLAN\_KEYS",

&#x20;   "REQUIRED\_RECORD\_KEYS",

&#x20;   "REQUIRED\_SIGNAL\_KEYS",

&#x20;   "SCHEMA\_VERSION",

&#x20;   "UndefinedValue",

&#x20;   "VALID\_EVIDENCE\_KINDS",

&#x20;   "VALID\_EVIDENCE\_VALIDITIES",

&#x20;   "VALID\_OUTCOMES",

&#x20;   "VALID\_SCORER\_STATUSES",

&#x20;   "VALID\_SPLITS",

&#x20;   "canonical\_json\_bytes",

&#x20;   "canonical\_sha256",

&#x20;   "compute\_expected\_plan\_hash",

&#x20;   "compute\_input\_sha256",

&#x20;   "format\_fraction\_Or\_undef",

&#x20;   "loads\_bounded\_json",

&#x20;   "parse\_analysis\_envelope",

&#x20;   "parse\_analysis\_json",

&#x20;   "validate\_panel",

]





class AnalysisInputError(ValueError):

&#x20;   """Raised when raw JSON or envelope structure violates hard schema/safety bounds."""





@dataclass(frozen=True)

class UndefinedValue:

&#x20;   """Explicit representation of an undefined quantity, serializable to JSON null + reason."""



&#x20;   reason: str

&#x20;   numerator: int | str | None = None

&#x20;   denominator: int | str | None = None



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "value": None,

&#x20;           "defined": False,

&#x20;           "reason": self.reason,

&#x20;           "numerator": self.numerator,

&#x20;           "denominator": self.denominator,

&#x20;       }





@dataclass(frozen=True)

class EligibilityStatus:

&#x20;   """Provenance and publication eligibility status; always unverified in this math engine."""



&#x20;   status: str = "UNVERIFIED"

&#x20;   publishable: bool = False

&#x20;   development\_only: bool = True

&#x20;   reason: str = (

&#x20;       "Pure mathematical analysis engine cannot verify Stage B registration or real "

&#x20;       "held-out governance."

&#x20;   )



&#x20;   def \_\_post\_init\_\_(self) -> None:

&#x20;       if self.status != "UNVERIFIED" or self.publishable is not False:

&#x20;           raise ValueError("EligibilityStatus in math engine must remain UNVERIFIED/non-publishable")



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "status": self.status,

&#x20;           "publishable": self.publishable,

&#x20;           "development\_only": self.development\_only,

&#x20;           "reason": self.reason,

&#x20;       }





@dataclass(frozen=True)

class ExpectedPlan:

&#x20;   """Declared experimental design specifying ordered tasks and exact seeds per config."""



&#x20;   tasks: tuple\[str, ...]

&#x20;   seeds\_by\_config: tuple\[tuple\[str, tuple\[int, ...]], ...]



&#x20;   def \_\_post\_init\_\_(self) -> None:

&#x20;       if not isinstance(self.tasks, tuple) or not self.tasks:

&#x20;           raise AnalysisInputError("expected\_plan.tasks must be a non-empty tuple of task IDs")

&#x20;       seen\_tasks: set\[str] = set()

&#x20;       for task\_id in self.tasks:

&#x20;           \_validate\_identifier(task\_id, "expected\_plan.tasks item")

&#x20;           if task\_id in seen\_tasks:

&#x20;               raise AnalysisInputError(f"Duplicate task\_id in expected\_plan.tasks: {task\_id!r}")

&#x20;           seen\_tasks.add(task\_id)



&#x20;       if not isinstance(self.seeds\_by\_config, tuple) or not self.seeds\_by\_config:

&#x20;           raise AnalysisInputError("expected\_plan.seeds\_by\_config must be a non-empty tuple")

&#x20;       seen\_configs: set\[str] = set()

&#x20;       for item in self.seeds\_by\_config:

&#x20;           if not isinstance(item, tuple) or len(item) != 2:

&#x20;               raise AnalysisInputError("seeds\_by\_config entries must be (config\_id, seeds) pairs")

&#x20;           config\_id, seeds = item

&#x20;           \_validate\_identifier(config\_id, "expected\_plan.seeds\_by\_config key")

&#x20;           if config\_id in seen\_configs:

&#x20;               raise AnalysisInputError(f"Duplicate config\_id in expected\_plan: {config\_id!r}")

&#x20;           seen\_configs.add(config\_id)

&#x20;           if not isinstance(seeds, tuple) or not seeds:

&#x20;               raise AnalysisInputError(

&#x20;                   f"expected\_plan.seeds\_by\_config\[{config\_id!r}] must be a non-empty seed list"

&#x20;               )

&#x20;           seen\_seeds: set\[int] = set()

&#x20;           for seed in seeds:

&#x20;               if not \_is\_exact\_int(seed) or seed < 0 or seed > MAX\_COUNT\_VALUE:

&#x20;                   raise AnalysisInputError(

&#x20;                       f"Seed in expected\_plan.seeds\_by\_config\[{config\_id!r}] must be a non-negative int"

&#x20;                   )

&#x20;               if seed in seen\_seeds:

&#x20;                   raise AnalysisInputError(

&#x20;                       f"Duplicate seed {seed} in expected\_plan.seeds\_by\_config\[{config\_id!r}]"

&#x20;                   )

&#x20;               seen\_seeds.add(seed)



&#x20;   @property

&#x20;   def config\_ids(self) -> tuple\[str, ...]:

&#x20;       return tuple(cfg for cfg, \_ in self.seeds\_by\_config)



&#x20;   def seeds\_for\_config(self, config\_id: str) -> tuple\[int, ...]:

&#x20;       for cfg, seeds in self.seeds\_by\_config:

&#x20;           if cfg == config\_id:

&#x20;               return seeds

&#x20;       raise KeyError(f"Unknown config\_id in expected\_plan: {config\_id!r}")



&#x20;   def seeds\_map(self) -> dict\[str, tuple\[int, ...]]:

&#x20;       return dict(self.seeds\_by\_config)



&#x20;   def expected\_cells(self) -> tuple\[tuple\[str, str, int], ...]:

&#x20;       cells: list\[tuple\[str, str, int]] = \[]

&#x20;       for task\_id in self.tasks:

&#x20;           for config\_id, seeds in self.seeds\_by\_config:

&#x20;               for seed in seeds:

&#x20;                   cells.append((config\_id, task\_id, seed))

&#x20;       return tuple(cells)



&#x20;   def to\_canonical\_dict(self) -> dict\[str, Any]:

&#x20;       """Preserve declared task order and declared seed order per config for expected\_plan\_hash."""

&#x20;       return {

&#x20;           "tasks": list(self.tasks),

&#x20;           "seeds\_by\_config": {

&#x20;               cfg: list(seeds) for cfg, seeds in sorted(self.seeds\_by\_config, key=lambda x: x\[0])

&#x20;           },

&#x20;       }





@dataclass(frozen=True)

class NormalizedRecord:

&#x20;   """Immutable validated run record across the analysis boundary."""



&#x20;   task\_id: str

&#x20;   config\_id: str

&#x20;   seed: int

&#x20;   split: str

&#x20;   family\_id: str

&#x20;   dataset\_id: str

&#x20;   evidence\_kind: str

&#x20;   registration\_id: str | None

&#x20;   execution\_complete: bool

&#x20;   outcome: str

&#x20;   evidence\_validity: str

&#x20;   scorer\_status: str

&#x20;   baseline\_verified: bool

&#x20;   cost\_nano\_usd: int | None

&#x20;   signals: ObservableSignals

&#x20;   turns: int | None = None

&#x20;   commands: int | None = None

&#x20;   actual\_prompt\_tokens: int | None = None

&#x20;   actual\_completion\_tokens: int | None = None

&#x20;   wall\_seconds: Fraction | None = None



&#x20;   def \_\_post\_init\_\_(self) -> None:

&#x20;       \_validate\_identifier(self.task\_id, "task\_id")

&#x20;       \_validate\_identifier(self.config\_id, "config\_id")

&#x20;       if not \_is\_exact\_int(self.seed) or self.seed < 0 or self.seed > MAX\_COUNT\_VALUE:

&#x20;           raise AnalysisInputError("seed must be a non-negative integer (bool rejected)")

&#x20;       if self.split not in VALID\_SPLITS:

&#x20;           raise AnalysisInputError(f"Invalid split: {self.split!r}")

&#x20;       \_validate\_identifier(self.family\_id, "family\_id")

&#x20;       \_validate\_identifier(self.dataset\_id, "dataset\_id")

&#x20;       if self.evidence\_kind not in VALID\_EVIDENCE\_KINDS:

&#x20;           raise AnalysisInputError(f"Invalid evidence\_kind: {self.evidence\_kind!r}")

&#x20;       if self.registration\_id is not None:

&#x20;           \_validate\_identifier(self.registration\_id, "registration\_id")

&#x20;       if not isinstance(self.execution\_complete, bool):

&#x20;           raise AnalysisInputError("execution\_complete must be a bool")

&#x20;       if self.outcome not in VALID\_OUTCOMES:

&#x20;           raise AnalysisInputError(f"Invalid outcome: {self.outcome!r}")

&#x20;       if self.evidence\_validity not in VALID\_EVIDENCE\_VALIDITIES:

&#x20;           raise AnalysisInputError(f"Invalid evidence\_validity: {self.evidence\_validity!r}")

&#x20;       if self.scorer\_status not in VALID\_SCORER\_STATUSES:

&#x20;           raise AnalysisInputError(f"Invalid scorer\_status: {self.scorer\_status!r}")

&#x20;       if not isinstance(self.baseline\_verified, bool):

&#x20;           raise AnalysisInputError("baseline\_verified must be a bool")

&#x20;       if self.cost\_nano\_usd is not None:

&#x20;           if (

&#x20;               not \_is\_exact\_int(self.cost\_nano\_usd)

&#x20;               or self.cost\_nano\_usd < 0

&#x20;               or self.cost\_nano\_usd > MAX\_COST\_NANO\_USD

&#x20;           ):

&#x20;               raise AnalysisInputError("cost\_nano\_usd must be a non-negative integer within bounds")

&#x20;       if not isinstance(self.signals, ObservableSignals):

&#x20;           raise AnalysisInputError("signals must be an ObservableSignals instance")

&#x20;       \_validate\_signals\_instance(self.signals)



&#x20;       for field\_name, val in (

&#x20;           ("turns", self.turns),

&#x20;           ("commands", self.commands),

&#x20;           ("actual\_prompt\_tokens", self.actual\_prompt\_tokens),

&#x20;           ("actual\_completion\_tokens", self.actual\_completion\_tokens),

&#x20;       ):

&#x20;           if val is not None:

&#x20;               if not \_is\_exact\_int(val) or val < 0 or val > MAX\_COUNT\_VALUE:

&#x20;                   raise AnalysisInputError(f"{field\_name} must be a non-negative integer or null")



&#x20;       if self.wall\_seconds is not None:

&#x20;           if not isinstance(self.wall\_seconds, Fraction):

&#x20;               raise AnalysisInputError("wall\_seconds must be normalized to Fraction or None")

&#x20;           if self.wall\_seconds < 0 or self.wall\_seconds > Fraction(int(MAX\_WALL\_SECONDS), 1):

&#x20;               raise AnalysisInputError("wall\_seconds must be non-negative and within bounds")



&#x20;   @property

&#x20;   def cell\_key(self) -> tuple\[str, str, int]:

&#x20;       return (self.config\_id, self.task\_id, self.seed)



&#x20;   def to\_canonical\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "actual\_completion\_tokens": self.actual\_completion\_tokens,

&#x20;           "actual\_prompt\_tokens": self.actual\_prompt\_tokens,

&#x20;           "baseline\_verified": self.baseline\_verified,

&#x20;           "commands": self.commands,

&#x20;           "config\_id": self.config\_id,

&#x20;           "cost\_nano\_usd": self.cost\_nano\_usd,

&#x20;           "dataset\_id": self.dataset\_id,

&#x20;           "evidence\_kind": self.evidence\_kind,

&#x20;           "evidence\_validity": self.evidence\_validity,

&#x20;           "execution\_complete": self.execution\_complete,

&#x20;           "family\_id": self.family\_id,

&#x20;           "outcome": self.outcome,

&#x20;           "registration\_id": self.registration\_id,

&#x20;           "scorer\_status": self.scorer\_status,

&#x20;           "seed": self.seed,

&#x20;           "signals": {

&#x20;               "agent\_self\_reports\_done": self.signals.agent\_self\_reports\_done,

&#x20;               "has\_patch": self.signals.has\_patch,

&#x20;               "hit\_step\_cap": self.signals.hit\_step\_cap,

&#x20;               "no\_command\_rate": str(Fraction(str(self.signals.no\_command\_rate))),

&#x20;               "visible\_tests\_pass": self.signals.visible\_tests\_pass,

&#x20;           },

&#x20;           "split": self.split,

&#x20;           "task\_id": self.task\_id,

&#x20;           "turns": self.turns,

&#x20;           "wall\_seconds": str(self.wall\_seconds) if self.wall\_seconds is not None else None,

&#x20;       }





@dataclass(frozen=True)

class AuditFinding:

&#x20;   """Single structured validation finding for a panel or record."""



&#x20;   code: str

&#x20;   severity: str  # "blocker" | "warning"

&#x20;   message: str

&#x20;   config\_id: str | None = None

&#x20;   task\_id: str | None = None

&#x20;   seed: int | None = None



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "code": self.code,

&#x20;           "severity": self.severity,

&#x20;           "message": self.message,

&#x20;           "config\_id": self.config\_id,

&#x20;           "task\_id": self.task\_id,

&#x20;           "seed": self.seed,

&#x20;       }





@dataclass(frozen=True)

class PanelAudit:

&#x20;   """Complete structured audit verdict for an input panel."""



&#x20;   status: str  # "valid" | "cost\_incomplete" | "blocked"

&#x20;   headline\_Comparison\_allowed: bool

&#x20;   cost\_comparison\_allowed: bool

&#x20;   success\_only\_allowed: bool

&#x20;   findings: tuple\[AuditFinding, ...]

&#x20;   expected\_cell\_count: int

&#x20;   observed\_record\_count: int

&#x20;   valid\_cell\_count: int

&#x20;   missing\_cost\_configs: tuple\[str, ...]

&#x20;   splits\_present: tuple\[str, ...]



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "status": self.status,

&#x20;           "headline\_comparison\_allowed": self.headline\_Comparison\_allowed,

&#x20;           "cost\_comparison\_allowed": self.cost\_comparison\_allowed,

&#x20;           "success\_only\_allowed": self.success\_only\_allowed,

&#x20;           "expected\_cell\_count": self.expected\_cell\_count,

&#x20;           "observed\_record\_count": self.observed\_record\_count,

&#x20;           "valid\_cell\_count": self.valid\_cell\_count,

&#x20;           "missing\_cost\_configs": list(self.missing\_cost\_configs),

&#x20;           "splits\_present": list(self.splits\_present),

&#x20;           "findings": \[f.to\_dict() for f in self.findings],

&#x20;       }





@dataclass(frozen=True)

class NormalizedEnvelope:

&#x20;   """Validated top-level analysis input envelope with canonical hashes and panel audit."""



&#x20;   schema\_version: int

&#x20;   dataset\_id: str

&#x20;   evidence\_kind: str

&#x20;   expected\_plan: ExpectedPlan

&#x20;   records: tuple\[NormalizedRecord, ...]

&#x20;   input\_sha256: str

&#x20;   expected\_plan\_hash: str

&#x20;   eligibility\_status: EligibilityStatus

&#x20;   audit: PanelAudit





def \_is\_exact\_int(value: Any) -> bool:

&#x20;   return type(value) is int





def \_validate\_identifier(value: Any, field\_name: str) -> str:

&#x20;   if not isinstance(value, str) or not value or len(value) > MAX\_STRING\_LENGTH:

&#x20;       raise AnalysisInputError(

&#x20;           f"{field\_name} must be a non-empty string of at most {MAX\_STRING\_LENGTH} chars"

&#x20;       )

&#x20;   if value.strip() != value:

&#x20;       raise AnalysisInputError(f"{field\_name} must not have leading or trailing whitespace")

&#x20;   for ch in value:

&#x20;       code = ord(ch)

&#x20;       if code < 32 or code == 127 or 0xD800 <= code <= 0xDFFF:

&#x20;           raise AnalysisInputError(

&#x20;               f"{field\_name} contains control characters or lone surrogates"

&#x20;           )

&#x20;   return value





def \_validate\_signals\_instance(signals: ObservableSignals) -> None:

&#x20;   if not isinstance(signals.has\_patch, bool):

&#x20;       raise AnalysisInputError("signals.has\_patch must be a bool")

&#x20;   if signals.visible\_tests\_pass is not None and not isinstance(signals.visible\_tests\_pass, bool):

&#x20;       raise AnalysisInputError("signals.visible\_tests\_pass must be bool or null")

&#x20;   if not isinstance(signals.hit\_step\_cap, bool):

&#x20;       raise AnalysisInputError("signals.hit\_step\_cap must be a bool")

&#x20;   if not isinstance(signals.agent\_self\_reports\_done, bool):

&#x20;       raise AnalysisInputError("signals.agent\_self\_reports\_done must be a bool")

&#x20;   if isinstance(signals.no\_command\_rate, bool) or not isinstance(

&#x20;       signals.no\_command\_rate, (int, float)

&#x20;   ):

&#x20;       raise AnalysisInputError("signals.no\_command\_rate must be a finite number in \[0.0, 1.0]")

&#x20;   rate = float(signals.no\_command\_rate)

&#x20;   if not math.isfinite(rate) or rate < 0.0 or rate > 1.0:

&#x20;       raise AnalysisInputError("signals.no\_command\_rate must be finite and within \[0.0, 1.0]")





def \_check\_json\_depth(obj: Any, current\_depth: int = 0) -> None:

&#x20;   if current\_depth > MAX\_JSON\_DEPTH:

&#x20;       raise AnalysisInputError(f"JSON nesting depth exceeds maximum of {MAX\_JSON\_DEPTH}")

&#x20;   if isinstance(obj, dict):

&#x20;       for v in obj.values():

&#x20;           \_check\_json\_depth(v, current\_depth + 1)

&#x20;   elif isinstance(obj, list):

&#x20;       for item in obj:

&#x20;           \_check\_json\_depth(item, current\_depth + 1)





def \_scan\_raw\_json\_hazards(raw\_text: str) -> None:

&#x20;   """Reject lone UTF-16 surrogates (literal or escaped) and oversized numeric literals."""

&#x20;   for ch in raw\_text:

&#x20;       if 0xD800 <= ord(ch) <= 0xDFFF:

&#x20;           raise AnalysisInputError("Input contains lone UTF-16 surrogate character")

&#x20;   if \_SURROGATE\_ESCAPE\_RE.search(raw\_text):

&#x20;       raise AnalysisInputError("Input contains escaped UTF-16 surrogate sequence")



&#x20;   # Scan outside string literals for overly long number tokens or extreme exponents.

&#x20;   in\_string = False

&#x20;   escape = False

&#x20;   i = 0

&#x20;   n = len(raw\_text)

&#x20;   while i < n:

&#x20;       ch = raw\_text\[i]

&#x20;       if in\_string:

&#x20;           if escape:

&#x20;               escape = False

&#x20;           elif ch == "\\\\":

&#x20;               escape = True

&#x20;           elif ch == '"':

&#x20;               in\_string = False

&#x20;           i += 1

&#x20;           continue

&#x20;       if ch == '"':

&#x20;           in\_string = True

&#x20;           i += 1

&#x20;           continue

&#x20;       if ch in "-0123456789":

&#x20;           match = \_NUMBER\_TOKEN\_RE.match(raw\_text, i)

&#x20;           if match:

&#x20;               token = match.group(0)

&#x20;               if len(token) > MAX\_NUMBER\_TOKEN\_CHARS:

&#x20;                   raise AnalysisInputError("Numeric literal exceeds maximum token length")

&#x20;               if "e" in token or "E" in token:

&#x20;                   exp\_str = token.lower().split("e", 1)\[1]

&#x20;                   if abs(int(exp\_str)) > 30:

&#x20;                       raise AnalysisInputError("Numeric exponent magnitude exceeds safe bound (30)")

&#x20;               i = match.end()

&#x20;               continue

&#x20;       i += 1





def loads\_bounded\_json(raw: str | bytes) -> dict\[str, Any]:

&#x20;   """Parse JSON with size, depth, duplicate-key, non-finite, and surrogate guards."""

&#x20;   if isinstance(raw, bytes):

&#x20;       if len(raw) > MAX\_INPUT\_BYTES:

&#x20;           raise AnalysisInputError(f"Input size {len(raw)} exceeds limit of {MAX\_INPUT\_BYTES} bytes")

&#x20;       try:

&#x20;           text = raw.decode("utf-8", errors="strict")

&#x20;       except UnicodeDecodeError as exc:

&#x20;           raise AnalysisInputError("Input is not valid UTF-8") from exc

&#x20;   elif isinstance(raw, str):

&#x20;       encoded = raw.encode("utf-8", errors="surrogatepass")

&#x20;       if len(encoded) > MAX\_INPUT\_BYTES:

&#x20;           raise AnalysisInputError(

&#x20;               f"Input size {len(encoded)} exceeds limit of {MAX\_INPUT\_BYTES} bytes"

&#x20;           )

&#x20;       text = raw

&#x20;   else:

&#x20;       raise AnalysisInputError("Input must be str or bytes")



&#x20;   \_scan\_raw\_json\_hazards(text)



&#x20;   def \_reject\_duplicates(pairs: list\[tuple\[str, Any]]) -> dict\[str, Any]:

&#x20;       result: dict\[str, Any] = {}

&#x20;       for k, v in pairs:

&#x20;           if not isinstance(k, str) or len(k) > MAX\_STRING\_LENGTH:

&#x20;               raise AnalysisInputError("JSON object key must be a bounded string")

&#x20;           if k in result:

&#x20;               raise AnalysisInputError(f"Duplicate JSON key: {k!r}")

&#x20;           result\[k] = v

&#x20;       return result



&#x20;   def \_reject\_nonfinite(constant: str) -> Any:

&#x20;       raise AnalysisInputError(f"Non-finite JSON numeric constant rejected: {constant}")



&#x20;   try:

&#x20;       parsed = json.loads(

&#x20;           text,

&#x20;           object\_pairs\_hook=\_reject\_duplicates,

&#x20;           parse\_constant=\_reject\_nonfinite,

&#x20;       )

&#x20;   except AnalysisInputError:

&#x20;       raise

&#x20;   except Exception as exc:

&#x20;       raise AnalysisInputError(f"Malformed JSON input: {exc}") from exc



&#x20;   if not isinstance(parsed, dict):

&#x20;       raise AnalysisInputError("Top-level JSON value must be an object")

&#x20;   \_check\_json\_depth(parsed, 0)

&#x20;   return parsed





def \_parse\_expected\_plan(raw\_plan: Any) -> ExpectedPlan:

&#x20;   if not isinstance(raw\_plan, Mapping):

&#x20;       raise AnalysisInputError("expected\_plan must be a JSON object")

&#x20;   keys = set(raw\_plan.keys())

&#x20;   if keys != REQUIRED\_PLAN\_KEYS:

&#x20;       unknown = sorted(keys - REQUIRED\_PLAN\_KEYS)

&#x20;       missing = sorted(REQUIRED\_PLAN\_KEYS - keys)

&#x20;       raise AnalysisInputError(

&#x20;           f"expected\_plan key mismatch (missing={missing}, unknown={unknown})"

&#x20;       )

&#x20;   raw\_tasks = raw\_plan\["tasks"]

&#x20;   if not isinstance(raw\_tasks, list) or not raw\_tasks:

&#x20;       raise AnalysisInputError("expected\_plan.tasks must be a non-empty list")

&#x20;   tasks = tuple(\_validate\_identifier(t, "expected\_plan.tasks item") for t in raw\_tasks)



&#x20;   raw\_sbc = raw\_plan\["seeds\_by\_config"]

&#x20;   if not isinstance(raw\_sbc, Mapping) or not raw\_sbc:

&#x20;       raise AnalysisInputError("expected\_plan.seeds\_by\_config must be a non-empty object")

&#x20;   seeds\_by\_config: list\[tuple\[str, tuple\[int, ...]]] = \[]

&#x20;   for cfg\_id, raw\_seeds in raw\_sbc.items():

&#x20;       \_validate\_identifier(cfg\_id, "expected\_plan.seeds\_by\_config key")

&#x20;       if not isinstance(raw\_seeds, list) or not raw\_seeds:

&#x20;           raise AnalysisInputError(

&#x20;               f"expected\_plan.seeds\_by\_config\[{cfg\_id!r}] must be a non-empty list"

&#x20;           )

&#x20;       parsed\_seeds: list\[int] = \[]

&#x20;       for s in raw\_seeds:

&#x20;           if not \_is\_exact\_int(s) or s < 0 or s > MAX\_COUNT\_VALUE:

&#x20;               raise AnalysisInputError(

&#x20;                   f"Seed in expected\_plan.seeds\_by\_config\[{cfg\_id!r}] must be a non-negative integer"

&#x20;               )

&#x20;           parsed\_seeds.append(s)

&#x20;       seeds\_by\_config.append((cfg\_id, tuple(parsed\_seeds)))



&#x20;   return ExpectedPlan(tasks=tasks, seeds\_by\_config=tuple(seeds\_by\_config))





def \_parse\_signals(raw\_signals: Any) -> ObservableSignals:

&#x20;   if not isinstance(raw\_signals, Mapping):

&#x20;       raise AnalysisInputError("record.signals must be a JSON object")

&#x20;   keys = set(raw\_signals.keys())

&#x20;   if keys != REQUIRED\_SIGNAL\_KEYS:

&#x20;       unknown = sorted(keys - REQUIRED\_SIGNAL\_KEYS)

&#x20;       missing = sorted(REQUIRED\_SIGNAL\_KEYS - keys)

&#x20;       raise AnalysisInputError(

&#x20;           f"record.signals key mismatch (missing={missing}, unknown={unknown})"

&#x20;       )

&#x20;   no\_cmd = raw\_signals\["no\_command\_rate"]

&#x20;   if isinstance(no\_cmd, bool) or not isinstance(no\_cmd, (int, float)):

&#x20;       raise AnalysisInputError("signals.no\_command\_rate must be a finite float or int")

&#x20;   rate\_float = float(no\_cmd)

&#x20;   if not math.isfinite(rate\_float) or rate\_float < 0.0 or rate\_float > 1.0:

&#x20;       raise AnalysisInputError("signals.no\_command\_rate must be finite and within \[0.0, 1.0]")



&#x20;   signals = ObservableSignals(

&#x20;       has\_patch=raw\_signals\["has\_patch"],

&#x20;       visible\_tests\_pass=raw\_signals\["visible\_tests\_pass"],

&#x20;       hit\_step\_cap=raw\_signals\["hit\_step\_cap"],

&#x20;       no\_command\_rate=rate\_float,

&#x20;       agent\_self\_reports\_done=raw\_signals\["agent\_self\_reports\_done"],

&#x20;   )

&#x20;   \_validate\_signals\_instance(signals)

&#x20;   return signals





def \_parse\_optional\_wall\_seconds(val: Any) -> Fraction | None:

&#x20;   if val is None:

&#x20;       return None

&#x20;   if isinstance(val, bool) or not isinstance(val, (int, float)):

&#x20;       raise AnalysisInputError("wall\_seconds must be a finite non-negative number or null")

&#x20;   if isinstance(val, float) and not math.isfinite(val):

&#x20;       raise AnalysisInputError("wall\_seconds must be finite")

&#x20;   frac = Fraction(str(val))

&#x20;   if frac < 0 or frac > Fraction(int(MAX\_WALL\_SECONDS), 1):

&#x20;       raise AnalysisInputError("wall\_seconds out of bounds")

&#x20;   return frac





def \_parse\_record(raw\_rec: Any, index: int) -> NormalizedRecord:

&#x20;   if not isinstance(raw\_rec, Mapping):

&#x20;       raise AnalysisInputError(f"records\[{index}] must be a JSON object")

&#x20;   keys = set(raw\_rec.keys())

&#x20;   missing = REQUIRED\_RECORD\_KEYS - keys

&#x20;   unknown = keys - ALLOWED\_RECORD\_KEYS

&#x20;   if missing or unknown:

&#x20;       raise AnalysisInputError(

&#x20;           f"records\[{index}] field mismatch (missing={sorted(missing)}, unknown={sorted(unknown)})"

&#x20;       )



&#x20;   signals = \_parse\_signals(raw\_rec\["signals"])

&#x20;   wall\_seconds = \_parse\_optional\_wall\_seconds(raw\_rec.get("wall\_seconds"))



&#x20;   return NormalizedRecord(

&#x20;       task\_id=raw\_rec\["task\_id"],

&#x20;       config\_id=raw\_rec\["config\_id"],

&#x20;       seed=raw\_rec\["seed"],

&#x20;       split=raw\_rec\["split"],

&#x20;       family\_id=raw\_rec\["family\_id"],

&#x20;       dataset\_id=raw\_rec\["dataset\_id"],

&#x20;       evidence\_kind=raw\_rec\["evidence\_kind"],

&#x20;       registration\_id=raw\_rec\["registration\_id"],

&#x20;       execution\_complete=raw\_rec\["execution\_complete"],

&#x20;       outcome=raw\_rec\["outcome"],

&#x20;       evidence\_validity=raw\_rec\["evidence\_validity"],

&#x20;       scorer\_status=raw\_rec\["scorer\_status"],

&#x20;       baseline\_verified=raw\_rec\["baseline\_verified"],

&#x20;       cost\_nano\_usd=raw\_rec\["cost\_nano\_usd"],

&#x20;       signals=signals,

&#x20;       turns=raw\_rec.get("turns"),

&#x20;       commands=raw\_rec.get("commands"),

&#x20;       actual\_prompt\_tokens=raw\_rec.get("actual\_prompt\_tokens"),

&#x20;       actual\_completion\_tokens=raw\_rec.get("actual\_completion\_tokens"),

&#x20;       wall\_seconds=wall\_seconds,

&#x20;   )





def \_audit\_single\_record\_semantics(

&#x20;   rec: NormalizedRecord,

&#x20;   envelope\_dataset\_id: str,

&#x20;   envelope\_evidence\_kind: str,

) -> list\[AuditFinding]:

&#x20;   """Check record-level protocol and scorer/outcome/validity consistency rules."""

&#x20;   findings: list\[AuditFinding] = \[]

&#x20;   cfg, task, seed = rec.config\_id, rec.task\_id, rec.seed



&#x20;   if rec.dataset\_id != envelope\_dataset\_id:

&#x20;       findings.append(

&#x20;           AuditFinding(

&#x20;               code="conflicting\_dataset\_id",

&#x20;               severity="blocker",

&#x20;               message=(

&#x20;                   f"Record dataset\_id {rec.dataset\_id!r} conflicts with envelope "

&#x20;                   f"dataset\_id {envelope\_dataset\_id!r}"

&#x20;               ),

&#x20;               config\_id=cfg,

&#x20;               task\_id=task,

&#x20;               seed=seed,

&#x20;           )

&#x20;       )



&#x20;   if rec.evidence\_kind != envelope\_evidence\_kind:

&#x20;       findings.append(

&#x20;           AuditFinding(

&#x20;               code="conflicting\_evidence\_kind",

&#x20;               severity="blocker",

&#x20;               message=(

&#x20;                   f"Record evidence\_kind {rec.evidence\_kind!r} conflicts with envelope "

&#x20;                   f"evidence\_kind {envelope\_evidence\_kind!r}"

&#x20;               ),

&#x20;               config\_id=cfg,

&#x20;               task\_id=task,

&#x20;               seed=seed,

&#x20;           )

&#x20;       )



&#x20;   # Normalization rule table:

&#x20;   # 1. scorer\_status == "passed" -> outcome == "solved", evidence\_validity == "valid", execution\_complete == True

&#x20;   # 2. scorer\_status == "failed" -> outcome == "unsolved", evidence\_validity == "valid", execution\_complete == True

&#x20;   # 3. scorer\_status == "candidate\_error" -> valid unsolved ONLY when baseline\_verified is True and execution\_complete is True

&#x20;   # 4. scorer\_status == "invalid\_evidence" -> outcome == "undetermined", evidence\_validity == "invalid" (blocks headline)

&#x20;   # 5. scorer\_status == "infrastructure\_error" -> outcome == "undetermined", evidence\_validity == "unknown" (blocks headline)

&#x20;   if rec.scorer\_status == "passed":

&#x20;       if (

&#x20;           rec.outcome != "solved"

&#x20;           or rec.evidence\_validity != "valid"

&#x20;           or not rec.execution\_complete

&#x20;       ):

&#x20;           findings.append(

&#x20;               AuditFinding(

&#x20;                   code="contradictory\_scorer\_outcome",

&#x20;                   severity="blocker",

&#x20;                   message=(

&#x20;                       "scorer\_status='passed' requires outcome='solved', "

&#x20;                       "evidence\_validity='valid', and execution\_complete=True"

&#x20;                   ),

&#x20;                   config\_id=cfg,

&#x20;                   task\_id=task,

&#x20;                   seed=seed,

&#x20;               )

&#x20;           )

&#x20;   elif rec.scorer\_status == "failed":

&#x20;       if (

&#x20;           rec.outcome != "unsolved"

&#x20;           or rec.evidence\_validity != "valid"

&#x20;           or not rec.execution\_complete

&#x20;       ):

&#x20;           findings.append(

&#x20;               AuditFinding(

&#x20;                   code="contradictory\_scorer\_outcome",

&#x20;                   severity="blocker",

&#x20;                   message=(

&#x20;                       "scorer\_status='failed' requires outcome='unsolved', "

&#x20;                       "evidence\_validity='valid', and execution\_complete=True"

&#x20;                   ),

&#x20;                   config\_id=cfg,

&#x20;                   task\_id=task,

&#x20;                   seed=seed,

&#x20;               )

&#x20;           )

&#x20;   elif rec.scorer\_status == "candidate\_error":

&#x20;       if not rec.baseline\_verified:

&#x20;           findings.append(

&#x20;               AuditFinding(

&#x20;                   code="unverified\_candidate\_error\_baseline",

&#x20;                   severity="blocker",

&#x20;                   message=(

&#x20;                       "scorer\_status='candidate\_error' requires baseline\_verified=True "

&#x20;                       "to count as a valid unsolved run"

&#x20;                   ),

&#x20;                   config\_id=cfg,

&#x20;                   task\_id=task,

&#x20;                   seed=seed,

&#x20;               )

&#x20;           )

&#x20;       if (

&#x20;           rec.outcome != "unsolved"

&#x20;           or rec.evidence\_validity != "valid"

&#x20;           or not rec.execution\_complete

&#x20;       ):

&#x20;           findings.append(

&#x20;               AuditFinding(

&#x20;                   code="contradictory\_scorer\_outcome",

&#x20;                   severity="blocker",

&#x20;                   message=(

&#x20;                       "scorer\_status='candidate\_error' requires outcome='unsolved', "

&#x20;                       "evidence\_validity='valid', and execution\_complete=True"

&#x20;                   ),

&#x20;                   config\_id=cfg,

&#x20;                   task\_id=task,

&#x20;                   seed=seed,

&#x20;               )

&#x20;           )

&#x20;   elif rec.scorer\_status == "invalid\_evidence":

&#x20;       if rec.outcome != "undetermined" or rec.evidence\_validity != "invalid":

&#x20;           findings.append(

&#x20;               AuditFinding(

&#x20;                   code="contradictory\_scorer\_outcome",

&#x20;                   severity="blocker",

&#x20;                   message=(

&#x20;                       "scorer\_status='invalid\_evidence' requires outcome='undetermined' "

&#x20;                       "and evidence\_validity='invalid'"

&#x20;                   ),

&#x20;                   config\_id=cfg,

&#x20;                   task\_id=task,

&#x20;                   seed=seed,

&#x20;               )

&#x20;           )

&#x20;       findings.append(

&#x20;           AuditFinding(

&#x20;               code="invalid\_evidence\_cell",

&#x20;               severity="blocker",

&#x20;               message=f"Cell {cfg}/{task}/seed{seed} has invalid\_evidence and blocks aggregation",

&#x20;               config\_id=cfg,

&#x20;               task\_id=task,

&#x20;               seed=seed,

&#x20;           )

&#x20;       )

&#x20;   elif rec.scorer\_status == "infrastructure\_error":

&#x20;       if rec.outcome != "undetermined" or rec.evidence\_validity != "unknown":

&#x20;           findings.append(

&#x20;               AuditFinding(

&#x20;                   code="contradictory\_scorer\_outcome",

&#x20;                   severity="blocker",

&#x20;                   message=(

&#x20;                       "scorer\_status='infrastructure\_error' requires outcome='undetermined' "

&#x20;                       "and evidence\_validity='unknown'"

&#x20;                   ),

&#x20;                   config\_id=cfg,

&#x20;                   task\_id=task,

&#x20;                   seed=seed,

&#x20;               )

&#x20;           )

&#x20;       findings.append(

&#x20;           AuditFinding(

&#x20;               code="infrastructure\_error\_cell",

&#x20;               severity="blocker",

&#x20;               message=(

&#x20;                   f"Cell {cfg}/{task}/seed{seed} had infrastructure\_error and blocks aggregation"

&#x20;               ),

&#x20;               config\_id=cfg,

&#x20;               task\_id=task,

&#x20;               seed=seed,

&#x20;           )

&#x20;       )



&#x20;   if not rec.execution\_complete and rec.scorer\_status not in {

&#x20;       "invalid\_evidence",

&#x20;       "infrastructure\_error",

&#x20;   }:

&#x20;       findings.append(

&#x20;           AuditFinding(

&#x20;               code="incomplete\_execution\_cell",

&#x20;               severity="blocker",

&#x20;               message=f"Cell {cfg}/{task}/seed{seed} has execution\_complete=False",

&#x20;               config\_id=cfg,

&#x20;               task\_id=task,

&#x20;               seed=seed,

&#x20;           )

&#x20;       )



&#x20;   return findings





def validate\_panel(

&#x20;   expected\_plan: ExpectedPlan,

&#x20;   records: Sequence\[NormalizedRecord],

&#x20;   \*,

&#x20;   dataset\_id: str,

&#x20;   evidence\_kind: str,

) -> PanelAudit:

&#x20;   """Validate complete task/config/seed coverage, split/family consistency, and cost availability."""

&#x20;   findings: list\[AuditFinding] = \[]

&#x20;   expected\_cells = expected\_plan.expected\_cells()

&#x20;   expected\_set = set(expected\_cells)



&#x20;   cell\_counts: dict\[tuple\[str, str, int], int] = {}

&#x20;   records\_by\_cell: dict\[tuple\[str, str, int], list\[NormalizedRecord]] = {}

&#x20;   splits\_seen: set\[str] = set()

&#x20;   task\_families: dict\[str, str] = {}

&#x20;   task\_splits: dict\[str, str] = {}



&#x20;   for rec in records:

&#x20;       splits\_seen.add(rec.split)

&#x20;       cell = rec.cell\_key

&#x20;       cell\_counts\[cell] = cell\_counts.get(cell, 0) + 1

&#x20;       records\_by\_cell.setdefault(cell, \[]).append(rec)



&#x20;       if cell not in expected\_set:

&#x20;           findings.append(

&#x20;               AuditFinding(

&#x20;                   code="unexpected\_cell",

&#x20;                   severity="blocker",

&#x20;                   message=f"unexpected {rec.config\_id}/{rec.task\_id}/seed{rec.seed}",

&#x20;                   config\_id=rec.config\_id,

&#x20;                   task\_id=rec.task\_id,

&#x20;                   seed=rec.seed,

&#x20;               )

&#x20;           )



&#x20;       if rec.task\_id in task\_families and task\_families\[rec.task\_id] != rec.family\_id:

&#x20;           findings.append(

&#x20;               AuditFinding(

&#x20;                   code="inconsistent\_task\_family",

&#x20;                   severity="blocker",

&#x20;                   message=(

&#x20;                       f"Task {rec.task\_id!r} has conflicting family\_id values: "

&#x20;                       f"{task\_families\[rec.task\_id]!r} vs {rec.family\_id!r}"

&#x20;                   ),

&#x20;                   config\_id=rec.config\_id,

&#x20;                   task\_id=rec.task\_id,

&#x20;                   seed=rec.seed,

&#x20;               )

&#x20;           )

&#x20;       else:

&#x20;           task\_families\[rec.task\_id] = rec.family\_id



&#x20;       if rec.task\_id in task\_splits and task\_splits\[rec.task\_id] != rec.split:

&#x20;           findings.append(

&#x20;               AuditFinding(

&#x20;                   code="inconsistent\_task\_split",

&#x20;                   severity="blocker",

&#x20;                   message=(

&#x20;                       f"Task {rec.task\_id!r} has conflicting split values: "

&#x20;                       f"{task\_splits\[rec.task\_id]!r} vs {rec.split!r}"

&#x20;                   ),

&#x20;                   config\_id=rec.config\_id,

&#x20;                   task\_id=rec.task\_id,

&#x20;                   seed=rec.seed,

&#x20;               )

&#x20;           )

&#x20;       else:

&#x20;           task\_splits\[rec.task\_id] = rec.split



&#x20;       findings.extend(\_audit\_single\_record\_semantics(rec, dataset\_id, evidence\_kind))



&#x20;   if len(splits\_seen) > 1:

&#x20;       findings.append(

&#x20;           AuditFinding(

&#x20;               code="mixed\_splits\_in\_panel",

&#x20;               severity="blocker",

&#x20;               message=f"Panel mixes multiple dataset splits: {sorted(splits\_seen)}",

&#x20;           )

&#x20;       )



&#x20;   # Check duplicates in deterministic cell order

&#x20;   for cell in sorted(cell\_counts):

&#x20;       count = cell\_counts\[cell]

&#x20;       if count > 1:

&#x20;           cfg, task, seed = cell

&#x20;           findings.append(

&#x20;               AuditFinding(

&#x20;                   code="duplicate\_cell",

&#x20;                   severity="blocker",

&#x20;                   message=f"duplicate {cfg}/{task}/seed{seed} (count={count})",

&#x20;                   config\_id=cfg,

&#x20;                   task\_id=task,

&#x20;                   seed=seed,

&#x20;               )

&#x20;           )



&#x20;   # Check missing cells in declared plan order

&#x20;   for cfg, task, seed in expected\_cells:

&#x20;       if (cfg, task, seed) not in cell\_counts:

&#x20;           findings.append(

&#x20;               AuditFinding(

&#x20;                   code="missing\_cell",

&#x20;                   severity="blocker",

&#x20;                   message=f"missing {cfg}/{task}/seed{seed}",

&#x20;                   config\_id=cfg,

&#x20;                   task\_id=task,

&#x20;                   seed=seed,

&#x20;               )

&#x20;           )



&#x20;   # Count valid cells and check missing cost per config

&#x20;   valid\_cell\_count = 0

&#x20;   missing\_cost\_configs: set\[str] = set()

&#x20;   for cfg, task, seed in expected\_cells:

&#x20;       cell\_recs = records\_by\_cell.get((cfg, task, seed), \[])

&#x20;       if len(cell\_recs) == 1:

&#x20;           r = cell\_recs\[0]

&#x20;           if (

&#x20;               r.evidence\_validity == "valid"

&#x20;               and r.outcome in {"solved", "unsolved"}

&#x20;               and r.execution\_complete

&#x20;               and (r.scorer\_status != "candidate\_error" or r.baseline\_verified)

&#x20;           ):

&#x20;               valid\_cell\_count += 1

&#x20;           if r.cost\_nano\_usd is None:

&#x20;               missing\_cost\_configs.add(cfg)

&#x20;               findings.append(

&#x20;                   AuditFinding(

&#x20;                       code="missing\_cost\_nano\_usd",

&#x20;                       severity="warning",

&#x20;                       message=f"missing cost\_nano\_usd for {cfg}/{task}/seed{seed}",

&#x20;                       config\_id=cfg,

&#x20;                       task\_id=task,

&#x20;                       seed=seed,

&#x20;                   )

&#x20;               )



&#x20;   has\_blocker = any(f.severity == "blocker" for f in findings) or (

&#x20;       valid\_cell\_count != len(expected\_cells)

&#x20;   )

&#x20;   if has\_blocker:

&#x20;       status = "blocked"

&#x20;       headline\_ok = False

&#x20;       cost\_ok = False

&#x20;       success\_only\_ok = False

&#x20;   elif missing\_cost\_configs:

&#x20;       status = "cost\_incomplete"

&#x20;       headline\_ok = False

&#x20;       cost\_ok = False

&#x20;       success\_only\_ok = True

&#x20;   else:

&#x20;       status = "valid"

&#x20;       headline\_ok = True

&#x20;       cost\_ok = True

&#x20;       success\_only\_ok = True



&#x20;   return PanelAudit(

&#x20;       status=status,

&#x20;       headline\_Comparison\_allowed=headline\_ok,

&#x20;       cost\_comparison\_allowed=cost\_ok,

&#x20;       success\_only\_allowed=success\_only\_ok,

&#x20;       findings=tuple(findings),

&#x20;       expected\_cell\_count=len(expected\_cells),

&#x20;       observed\_record\_count=len(records),

&#x20;       valid\_cell\_count=valid\_cell\_count,

&#x20;       missing\_cost\_configs=tuple(sorted(missing\_cost\_configs)),

&#x20;       splits\_present=tuple(sorted(splits\_seen)),

&#x20;   )





def canonical\_json\_bytes(obj: Any) -> bytes:

&#x20;   """Serialize a canonical dictionary/list structure to deterministic UTF-8 JSON bytes."""

&#x20;   return json.dumps(

&#x20;       obj,

&#x20;       sort\_keys=True,

&#x20;       separators=(",", ":"),

&#x20;       ensure\_ascii=True,

&#x20;       allow\_nan=False,

&#x20;   ).encode("utf-8")





def canonical\_sha256(obj: Any) -> str:

&#x20;   """Return hex SHA-256 of canonical JSON bytes."""

&#x20;   return hashlib.sha256(canonical\_json\_bytes(obj)).hexdigest()





def compute\_expected\_plan\_hash(expected\_plan: ExpectedPlan) -> str:

&#x20;   """Compute SHA-256 of expected\_plan preserving declared task and seed ordering."""

&#x20;   return canonical\_sha256(expected\_plan.to\_canonical\_dict())





def compute\_input\_sha256(

&#x20;   \*,

&#x20;   schema\_version: int,

&#x20;   dataset\_id: str,

&#x20;   evidence\_kind: str,

&#x20;   expected\_plan: ExpectedPlan,

&#x20;   records: Sequence\[NormalizedRecord],

) -> str:

&#x20;   """Compute canonical SHA-256 of normalized envelope invariant to record input ordering."""

&#x20;   sorted\_records = sorted(

&#x20;       (r.to\_canonical\_dict() for r in records),

&#x20;       key=lambda d: (

&#x20;           d\["config\_id"],

&#x20;           d\["task\_id"],

&#x20;           d\["seed"],

&#x20;           canonical\_json\_bytes(d).decode("ascii"),

&#x20;       ),

&#x20;   )

&#x20;   canonical\_envelope = {

&#x20;       "dataset\_id": dataset\_id,

&#x20;       "evidence\_kind": evidence\_kind,

&#x20;       "expected\_plan": expected\_plan.to\_canonical\_dict(),

&#x20;       "records": sorted\_records,

&#x20;       "schema\_version": schema\_version,

&#x20;   }

&#x20;   return canonical\_sha256(canonical\_envelope)





def parse\_analysis\_envelope(data: Mapping\[str, Any]) -> NormalizedEnvelope:

&#x20;   """Validate and normalize a parsed JSON dictionary into an immutable NormalizedEnvelope."""

&#x20;   if not isinstance(data, Mapping):

&#x20;       raise AnalysisInputError("Envelope must be a mapping")

&#x20;   keys = set(data.keys())

&#x20;   if "expected" in keys:

&#x20;       raise AnalysisInputError(

&#x20;           "Test-harness 'expected' field is not permitted in production analysis input"

&#x20;       )

&#x20;   if keys != REQUIRED\_ENVELOPE\_KEYS:

&#x20;       unknown = sorted(keys - REQUIRED\_ENVELOPE\_KEYS)

&#x20;       missing = sorted(REQUIRED\_ENVELOPE\_KEYS - keys)

&#x20;       raise AnalysisInputError(

&#x20;           f"Envelope key mismatch (missing={missing}, unknown={unknown})"

&#x20;       )



&#x20;   schema\_version = data\["schema\_version"]

&#x20;   if not \_is\_exact\_int(schema\_version) or schema\_version != SCHEMA\_VERSION:

&#x20;       raise AnalysisInputError(

&#x20;           f"Unsupported schema\_version: {schema\_version!r} (expected {SCHEMA\_VERSION})"

&#x20;       )



&#x20;   dataset\_id = \_validate\_identifier(data\["dataset\_id"], "dataset\_id")

&#x20;   evidence\_kind = data\["evidence\_kind"]

&#x20;   if evidence\_kind not in VALID\_EVIDENCE\_KINDS:

&#x20;       raise AnalysisInputError(f"Invalid envelope evidence\_kind: {evidence\_kind!r}")



&#x20;   expected\_plan = \_parse\_expected\_plan(data\["expected\_plan"])



&#x20;   raw\_records = data\["records"]

&#x20;   if not isinstance(raw\_records, list):

&#x20;       raise AnalysisInputError("records must be a JSON list")

&#x20;   if len(raw\_records) > MAX\_RECORDS:

&#x20;       raise AnalysisInputError(

&#x20;           f"Record count {len(raw\_records)} exceeds maximum of {MAX\_RECORDS}"

&#x20;       )



&#x20;   records = tuple(\_parse\_record(r, idx) for idx, r in enumerate(raw\_records))



&#x20;   audit = validate\_panel(

&#x20;       expected\_plan,

&#x20;       records,

&#x20;       dataset\_id=dataset\_id,

&#x20;       evidence\_kind=evidence\_kind,

&#x20;   )

&#x20;   plan\_hash = compute\_expected\_plan\_hash(expected\_plan)

&#x20;   input\_hash = compute\_input\_sha256(

&#x20;       schema\_version=schema\_version,

&#x20;       dataset\_id=dataset\_id,

&#x20;       evidence\_kind=evidence\_kind,

&#x20;       expected\_plan=expected\_plan,

&#x20;       records=records,

&#x20;   )



&#x20;   return NormalizedEnvelope(

&#x20;       schema\_version=schema\_version,

&#x20;       dataset\_id=dataset\_id,

&#x20;       evidence\_kind=evidence\_kind,

&#x20;       expected\_plan=expected\_plan,

&#x20;       records=records,

&#x20;       input\_sha256=input\_hash,

&#x20;       expected\_plan\_hash=plan\_hash,

&#x20;       eligibility\_status=EligibilityStatus(),

&#x20;       audit=audit,

&#x20;   )





def parse\_analysis\_json(raw: str | bytes) -> NormalizedEnvelope:

&#x20;   """Parse bounded raw JSON bytes/str directly into a NormalizedEnvelope."""

&#x20;   parsed = loads\_bounded\_json(raw)

&#x20;   return parse\_analysis\_envelope(parsed)





def format\_fraction\_Or\_undef(value: Fraction | UndefinedValue) -> dict\[str, Any]:

&#x20;   """Serialize a Fraction or UndefinedValue into a deterministic JSON-safe dictionary."""

&#x20;   if isinstance(value, UndefinedValue):

&#x20;       return value.to\_dict()

&#x20;   if not isinstance(value, Fraction):

&#x20;       raise TypeError(f"Expected Fraction or UndefinedValue, got {type(value).\_\_name\_\_}")

&#x20;   return {

&#x20;       "value": float(value),

&#x20;       "exact": f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator),

&#x20;       "numerator": value.numerator,

&#x20;       "denominator": value.denominator,

&#x20;       "defined": True,

&#x20;       "reason": None,

&#x20;   }



```



\---



\## FILE: dojo/bench/stats.py



```python

"""WP2, WP3, WP4: Primary metrics, paired task bootstrap, family-cluster and seed sensitivity."""



from \_\_future\_\_ import annotations



import math

import random

from collections.abc import Mapping, Sequence

from dataclasses import dataclass

from fractions import Fraction

from typing import Any



from dojo.bench.records import (

&#x20;    FOUNDATION\_METHOD\_VERSION,

&#x20;   AnalysisInputError,

&#x20;   NormalizedEnvelope,

&#x20;   NormalizedRecord,

&#x20;   UndefinedValue,

&#x20;   format\_fraction\_Or\_undef,

)



DEFAULT\_BOOTSTRAP\_REPLICATES: int = 10\_000

MAX\_BOOTSTRAP\_REPLICATES: int = 100\_000

MAX\_BOOTSTRAP\_WORKLOAD: int = 10\_000\_000  # Max (replicates \* n\_tasks \* n\_series)

QUANTILE\_METHOD: str = "sorted\_empirical\_nearest\_rank\_linear\_endpoints"



\_\_all\_\_ = \[

&#x20;   "BootstrapInterval",

&#x20;   "ConfigMetrics",

&#x20;   "DEFAULT\_BOOTSTRAP\_REPLICATES",

&#x20;   "FamilyBootstrapResult",

&#x20;   "FamilySeriesSummary",

&#x20;   "MAX\_BOOTSTRAP\_REPLICATES",

&#x20;   "MAX\_BOOTSTRAP\_WORKLOAD",

&#x20;   "PairedBootstrapResult",

&#x20;   "PairedDifferenceSummary",

&#x20;   "QUANTILE\_METHOD",

&#x20;   "SecondaryMetricSummary",

&#x20;   "SeedSensitivityEntry",

&#x20;   "SeedSensitivityResult",

&#x20;   "SeriesBootstrapSummary",

&#x20;   "SeriesPoint",

&#x20;   "TaskPoint",

&#x20;   "TaskSeries",

&#x20;   "build\_config\_task\_series",

&#x20;   "compute\_all\_config\_metrics",

&#x20;   "compute\_config\_metrics",

&#x20;   "compute\_empirical\_quantile",

&#x20;   "evaluate\_series\_point",

&#x20;   "family\_cluster\_bootstrap",

&#x20;   "paired\_task\_bootstrap",

&#x20;   "seed\_sensitivity\_analysis",

]





@dataclass(frozen=True)

class TaskPoint:

&#x20;   """Per-task aggregated success rate and mean 1-seed cost for a config or cascade series."""



&#x20;   task\_id: str

&#x20;   family\_id: str

&#x20;   seed\_count: int

&#x20;   pass\_rate: Fraction

&#x20;   mean\_cost\_nanos: Fraction | None

&#x20;   actual\_all\_seeds\_cost\_nanos: int | None





@dataclass(frozen=True)

class TaskSeries:

&#x20;   """Reusable ordered per-task series for any baseline config or Batch B cascade policy."""



&#x20;   series\_id: str

&#x20;   series\_kind: str  # "config" | "cascade" | "seed\_subset"

&#x20;   tasks: tuple\[TaskPoint, ...]

&#x20;   declared\_seed\_count: int

&#x20;   has\_complete\_costs: bool



&#x20;   def \_\_post\_init\_\_(self) -> None:

&#x20;       if not self.tasks:

&#x20;           raise ValueError("TaskSeries.tasks must be non-empty")



&#x20;   @property

&#x20;   def n\_tasks(self) -> int:

&#x20;       return len(self.tasks)





@dataclass(frozen=True)

class SeriesPoint:

&#x20;   """Point estimates for a TaskSeries across n tasks (or resampled tasks)."""



&#x20;   series\_id: str

&#x20;   n\_tasks: int

&#x20;   pass\_at\_1: Fraction

&#x20;   expected\_solved\_tasks: Fraction

&#x20;   expected\_total\_cost\_nanos: Fraction | UndefinedValue

&#x20;   mean\_task\_cost\_nanos: Fraction | UndefinedValue

&#x20;   expected\_cost\_per\_solved\_nanos: Fraction | UndefinedValue

&#x20;   actual\_all\_repetitions\_spend\_nanos: int | UndefinedValue



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "series\_id": self.series\_id,

&#x20;           "n\_tasks": self.n\_tasks,

&#x20;           "pass\_at\_1": format\_fraction\_Or\_undef(self.pass\_at\_1),

&#x20;           "expected\_solved\_tasks": format\_fraction\_Or\_undef(self.expected\_solved\_tasks),

&#x20;           "expected\_total\_cost\_nanos": format\_fraction\_Or\_undef(self.expected\_total\_cost\_nanos),

&#x20;           "mean\_task\_cost\_nanos": format\_fraction\_Or\_undef(self.mean\_task\_cost\_nanos),

&#x20;           "expected\_cost\_per\_solved\_nanos": format\_fraction\_Or\_undef(

&#x20;               self.expected\_cost\_per\_solved\_nanos

&#x20;           ),

&#x20;           "actual\_all\_repetitions\_spend\_nanos": (

&#x20;               self.actual\_all\_repetitions\_spend\_nanos.to\_dict()

&#x20;               if isinstance(self.actual\_all\_repetitions\_spend\_nanos, UndefinedValue)

&#x20;               else {

&#x20;                   "value": self.actual\_all\_repetitions\_spend\_nanos,

&#x20;                   "defined": True,

&#x20;                   "reason": None,

&#x20;               }

&#x20;           ),

&#x20;       }





@dataclass(frozen=True)

class SecondaryMetricSummary:

&#x20;   """Summary of an optional/secondary metric without inferring 0 for absent values."""



&#x20;   metric\_name: str

&#x20;   total\_runs: int

&#x20;   known\_runs: int

&#x20;   missing\_runs: int

&#x20;   task\_weighted\_mean: Fraction | UndefinedValue

&#x20;   all\_repetitions\_sum: Fraction | UndefinedValue



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "metric\_name": self.metric\_name,

&#x20;           "total\_runs": self.total\_runs,

&#x20;           "known\_runs": self.known\_runs,

&#x20;           "missing\_runs": self.missing\_runs,

&#x20;           "task\_weighted\_mean": format\_fraction\_Or\_undef(self.task\_weighted\_mean),

&#x20;           "all\_repetitions\_sum": format\_fraction\_Or\_undef(self.all\_repetitions\_sum),

&#x20;       }





@dataclass(frozen=True)

class ConfigMetrics:

&#x20;   """Complete WP2 primary and secondary metrics for a single configuration."""



&#x20;   config\_id: str

&#x20;   dataset\_id: str

&#x20;   split: str

&#x20;   n\_tasks: int

&#x20;   declared\_seeds: tuple\[int, ...]

&#x20;   total\_runs: int

&#x20;   primary: SeriesPoint

&#x20;   task\_points: tuple\[TaskPoint, ...]

&#x20;   secondary\_metrics: Mapping\[str, SecondaryMetricSummary]



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "config\_id": self.config\_id,

&#x20;           "dataset\_id": self.dataset\_id,

&#x20;           "split": self.split,

&#x20;           "n\_tasks": self.n\_tasks,

&#x20;           "declared\_seeds": list(self.declared\_seeds),

&#x20;           "declared\_seed\_count": len(self.declared\_seeds),

&#x20;           "total\_runs": self.total\_runs,

&#x20;           "primary": self.primary.to\_dict(),

&#x20;           "secondary\_metrics": {

&#x20;               k: v.to\_dict() for k, v in sorted(self.secondary\_metrics.items())

&#x20;           },

&#x20;       }





@dataclass(frozen=True)

class BootstrapInterval:

&#x20;   """Empirical bootstrap confidence interval with explicit undefined/zero-solve accounting."""



&#x20;   metric\_name: str

&#x20;   point\_estimate: Fraction | UndefinedValue

&#x20;   lower: Fraction | UndefinedValue

&#x20;   upper: Fraction | UndefinedValue

&#x20;   confidence\_level: Fraction

&#x20;   replicates: int

&#x20;   defined\_draws: int

&#x20;   undefined\_draws: int

&#x20;   zero\_solve\_draws: int

&#x20;   quantile\_method: str = QUANTILE\_METHOD



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "metric\_name": self.metric\_name,

&#x20;           "point\_estimate": format\_fraction\_Or\_undef(self.point\_estimate),

&#x20;           "lower": format\_fraction\_Or\_undef(self.lower),

&#x20;           "upper": format\_fraction\_Or\_undef(self.upper),

&#x20;           "confidence\_level": float(self.confidence\_level),

&#x20;           "replicates": self.replicates,

&#x20;           "defined\_draws": self.defined\_draws,

&#x20;           "undefined\_draws": self.undefined\_draws,

&#x20;           "zero\_solve\_draws": self.zero\_solve\_draws,

&#x20;           "quantile\_method": self.quantile\_method,

&#x20;       }





@dataclass(frozen=True)

class SeriesBootstrapSummary:

&#x20;   """Bootstrap intervals for a single config or cascade series."""



&#x20;   series\_id: str

&#x20;   pass\_at\_1: BootstrapInterval

&#x20;   expected\_total\_cost\_nanos: BootstrapInterval

&#x20;   mean\_task\_cost\_nanos: BootstrapInterval

&#x20;   expected\_cost\_per\_solved\_nanos: BootstrapInterval



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "series\_id": self.series\_id,

&#x20;           "pass\_at\_1": self.pass\_at\_1.to\_dict(),

&#x20;           "expected\_total\_cost\_nanos": self.expected\_total\_cost\_nanos.to\_dict(),

&#x20;           "mean\_task\_cost\_nanos": self.mean\_task\_cost\_nanos.to\_dict(),

&#x20;           "expected\_cost\_per\_solved\_nanos": self.expected\_cost\_per\_solved\_nanos.to\_dict(),

&#x20;       }





@dataclass(frozen=True)

class PairedDifferenceSummary:

&#x20;   """Paired bootstrap delta (target - baseline) using identical sampled task indices."""



&#x20;   baseline\_id: str

&#x20;   target\_id: str

&#x20;   delta\_pass\_at\_1: BootstrapInterval

&#x20;   delta\_expected\_total\_cost\_nanos: BootstrapInterval

&#x20;   delta\_expected\_cost\_per\_solved\_nanos: BootstrapInterval



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "baseline\_id": self.baseline\_id,

&#x20;           "target\_id": self.target\_id,

&#x20;           "definition": f"{self.target\_id} minus {self.baseline\_id}",

&#x20;           "delta\_pass\_at\_1": self.delta\_pass\_at\_1.to\_dict(),

&#x20;           "delta\_expected\_total\_cost\_nanos": self.delta\_expected\_total\_cost\_nanos.to\_dict(),

&#x20;           "delta\_expected\_cost\_per\_solved\_nanos": (

&#x20;               self.delta\_expected\_cost\_per\_solved\_nanos.to\_dict()

&#x20;           ),

&#x20;       }





@dataclass(frozen=True)

class PairedBootstrapResult:

&#x20;   """WP3 paired task bootstrap output across all compared series."""



&#x20;   method\_version: str

&#x20;   estimand\_label: str

&#x20;   replicates: int

&#x20;   seed: int | None

&#x20;   confidence\_level: Fraction

&#x20;   n\_tasks: int

&#x20;   quantile\_method: str

&#x20;   series\_summaries: Mapping\[str, SeriesBootstrapSummary]

&#x20;   paired\_differences: tuple\[PairedDifferenceSummary, ...]



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "method\_version": self.method\_version,

&#x20;           "estimand\_label": self.estimand\_label,

&#x20;           "replicates": self.replicates,

&#x20;           "seed": self.seed,

&#x20;           "confidence\_level": float(self.confidence\_level),

&#x20;           "n\_tasks": self.n\_tasks,

&#x20;           "quantile\_method": self.quantile\_method,

&#x20;           "series\_summaries": {

&#x20;               k: v.to\_dict() for k, v in sorted(self.series\_summaries.items())

&#x20;           },

&#x20;           "paired\_differences": \[d.to\_dict() for d in self.paired\_differences],

&#x20;       }





@dataclass(frozen=True)

class FamilySeriesSummary:

&#x20;   """Cluster-resampled summary for a single series, preserving original\_n for total cost."""



&#x20;   series\_id: str

&#x20;   pass\_at\_1: BootstrapInterval

&#x20;   target\_n\_expected\_total\_cost\_nanos: BootstrapInterval

&#x20;   mean\_task\_cost\_nanos: BootstrapInterval

&#x20;   expected\_cost\_per\_solved\_nanos: BootstrapInterval



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "series\_id": self.series\_id,

&#x20;           "pass\_at\_1": self.pass\_at\_1.to\_dict(),

&#x20;           "target\_n\_expected\_total\_cost\_nanos": (

&#x20;               self.target\_n\_expected\_total\_cost\_nanos.to\_dict()

&#x20;           ),

&#x20;           "mean\_task\_cost\_nanos": self.mean\_task\_cost\_nanos.to\_dict(),

&#x20;           "expected\_cost\_per\_solved\_nanos": self.expected\_cost\_per\_solved\_nanos.to\_dict(),

&#x20;       }





@dataclass(frozen=True)

class FamilyBootstrapResult:

&#x20;   """WP4 non-primary family-cluster bootstrap sensitivity analysis."""



&#x20;   is\_primary: bool

&#x20;   estimand\_label: str

&#x20;   weighting\_method: str

&#x20;   total\_cost\_scaling\_rule: str

&#x20;   replicates: int

&#x20;   seed: int | None

&#x20;   confidence\_level: Fraction

&#x20;   original\_n\_tasks: int

&#x20;   n\_families: int

&#x20;   family\_sizes: Mapping\[str, int]

&#x20;   min\_resampled\_tasks: int

&#x20;   max\_resampled\_tasks: int

&#x20;   mean\_resampled\_tasks: Fraction

&#x20;   series\_summaries: Mapping\[str, FamilySeriesSummary]

&#x20;   paired\_differences: tuple\[PairedDifferenceSummary, ...]



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "is\_primary": self.is\_primary,

&#x20;           "estimand\_label": self.estimand\_label,

&#x20;           "weighting\_method": self.weighting\_method,

&#x20;           "total\_cost\_scaling\_rule": self.total\_cost\_scaling\_rule,

&#x20;           "replicates": self.replicates,

&#x20;           "seed": self.seed,

&#x20;           "confidence\_level": float(self.confidence\_level),

&#x20;           "original\_n\_tasks": self.original\_n\_tasks,

&#x20;           "n\_families": self.n\_families,

&#x20;           "family\_sizes": dict(sorted(self.family\_sizes.items())),

&#x20;           "min\_resampled\_tasks": self.min\_resampled\_tasks,

&#x20;           "max\_resampled\_tasks": self.max\_resampled\_tasks,

&#x20;           "mean\_resampled\_tasks": format\_fraction\_Or\_undef(self.mean\_resampled\_tasks),

&#x20;           "series\_summaries": {

&#x20;               k: v.to\_dict() for k, v in sorted(self.series\_summaries.items())

&#x20;           },

&#x20;           "paired\_differences": \[d.to\_dict() for d in self.paired\_differences],

&#x20;       }





@dataclass(frozen=True)

class SeedSensitivityEntry:

&#x20;   """Metrics for a predeclared seed position or seed subset on a single config."""



&#x20;   config\_id: str

&#x20;   slice\_label: str

&#x20;   selected\_seeds: tuple\[int, ...]

&#x20;   point: SeriesPoint



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "config\_id": self.config\_id,

&#x20;           "slice\_label": self.slice\_label,

&#x20;           "selected\_seeds": list(self.selected\_seeds),

&#x20;           "point": self.point.to\_dict(),

&#x20;       }





@dataclass(frozen=True)

class SeedSensitivityResult:

&#x20;   """WP4 non-primary seed-position and seed-subset sensitivity report."""



&#x20;   is\_primary: bool

&#x20;   estimand\_label: str

&#x20;   declared\_seeds\_by\_config: Mapping\[str, tuple\[int, ...]]

&#x20;   common\_seed\_positions: tuple\[int, ...]

&#x20;   shared\_exact\_seeds: tuple\[int, ...]

&#x20;   comparison\_rules\_note: str

&#x20;   entries: tuple\[SeedSensitivityEntry, ...]



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "is\_primary": self.is\_primary,

&#x20;           "estimand\_label": self.estimand\_label,

&#x20;           "declared\_seeds\_by\_config": {

&#x20;               k: list(v) for k, v in sorted(self.declared\_seeds\_by\_config.items())

&#x20;           },

&#x20;           "common\_seed\_positions": list(self.common\_seed\_positions),

&#x20;           "shared\_exact\_seeds": list(self.shared\_exact\_seeds),

&#x20;           "comparison\_rules\_note": self.comparison\_rules\_note,

&#x20;           "entries": \[e.to\_dict() for e in self.entries],

&#x20;       }





def \_require\_headline\_or\_success\_allowed(

&#x20;   envelope: NormalizedEnvelope,

&#x20;   \*,

&#x20;   require\_costs: bool = False,

) -> None:

&#x20;   if not envelope.audit.success\_only\_allowed:

&#x20;       reasons = ", ".join(f.message for f in envelope.audit.findings if f.severity == "blocker")

&#x20;       raise AnalysisInputError(

&#x20;           f"Panel audit status is {envelope.audit.status!r}; headline aggregation blocked: {reasons}"

&#x20;       )

&#x20;   if require\_costs and not envelope.audit.cost\_comparison\_allowed:

&#x20;       raise AnalysisInputError(

&#x20;           f"Panel has missing costs for configs {envelope.audit.missing\_cost\_configs}; "

&#x20;           "cost-dependent comparison blocked"

&#x20;       )





def evaluate\_series\_point(

&#x20;   series\_id: str,

&#x20;   task\_points: Sequence\[TaskPoint],

&#x20;   \*,

&#x20;   target\_n\_tasks: int | None = None,

&#x20;   include\_actual\_spend: bool = True,

) -> SeriesPoint:

&#x20;   """Evaluate primary estimands from an arbitrary sequence of TaskPoints."""

&#x20;   if not task\_points:

&#x20;       raise ValueError("task\_points must be non-empty")

&#x20;   n\_obs = len(task\_points)

&#x20;   effective\_n = target\_n\_tasks if target\_n\_tasks is not None else n\_obs



&#x20;   sum\_p = sum((tp.pass\_rate for tp in task\_points), Fraction(0, 1))

&#x20;   pass\_at\_1 = sum\_p / Fraction(n\_obs, 1)

&#x20;   expected\_solved = pass\_at\_1 \* Fraction(effective\_n, 1)



&#x20;   if any(tp.mean\_cost\_nanos is None for tp in task\_points):

&#x20;       undef\_cost = UndefinedValue(reason="missing\_cost\_nano\_usd")

&#x20;       return SeriesPoint(

&#x20;           series\_id=series\_id,

&#x20;           n\_tasks=effective\_n,

&#x20;           pass\_at\_1=pass\_at\_1,

&#x20;           expected\_solved\_tasks=expected\_solved,

&#x20;           expected\_total\_cost\_nanos=undef\_cost,

&#x20;           mean\_task\_cost\_nanos=undef\_cost,

&#x20;           expected\_cost\_per\_solved\_nanos=undef\_cost,

&#x20;           actual\_all\_repetitions\_spend\_nanos=undef\_cost,

&#x20;       )



&#x20;   sum\_m = sum(

&#x20;       (tp.mean\_cost\_nanos for tp in task\_points if tp.mean\_cost\_nanos is not None),

&#x20;       Fraction(0, 1),

&#x20;   )

&#x20;   mean\_task\_cost = sum\_m / Fraction(n\_obs, 1)

&#x20;   expected\_total\_cost = mean\_task\_cost \* Fraction(effective\_n, 1)



&#x20;   if sum\_p == 0:

&#x20;       cost\_per\_solved: Fraction | UndefinedValue = UndefinedValue(

&#x20;           reason="zero\_expected\_solves",

&#x20;           numerator=str(expected\_total\_cost),

&#x20;           denominator=0,

&#x20;       )

&#x20;   else:

&#x20;       # Note: sum\_m / sum\_p == expected\_total\_cost / expected\_solved

&#x20;       cost\_per\_solved = expected\_total\_cost / expected\_solved



&#x20;   if include\_actual\_spend and all(tp.actual\_all\_seeds\_cost\_nanos is not None for tp in task\_points):

&#x20;       actual\_spend: int | UndefinedValue = sum(

&#x20;           tp.actual\_all\_seeds\_cost\_nanos

&#x20;           for tp in task\_points

&#x20;           if tp.actual\_all\_seeds\_cost\_nanos is not None

&#x20;       )

&#x20;   else:

&#x20;       actual\_spend = UndefinedValue(

&#x20;           reason="not\_applicable\_to\_resample\_or\_synthetic\_series"

&#x20;           if not include\_actual\_spend

&#x20;           else "missing\_cost\_nano\_usd"

&#x20;       )



&#x20;   return SeriesPoint(

&#x20;       series\_id=series\_id,

&#x20;       n\_tasks=effective\_n,

&#x20;       pass\_at\_1=pass\_at\_1,

&#x20;       expected\_solved\_tasks=expected\_solved,

&#x20;       expected\_total\_cost\_nanos=expected\_total\_cost,

&#x20;       mean\_task\_cost\_nanos=mean\_task\_cost,

&#x20;       expected\_cost\_per\_solved\_nanos=cost\_per\_solved,

&#x20;       actual\_all\_repetitions\_spend\_nanos=actual\_spend,

&#x20;   )





def build\_config\_task\_series(

&#x20;   envelope: NormalizedEnvelope,

&#x20;   config\_id: str,

&#x20;   \*,

&#x20;   seed\_subset: Sequence\[int] | None = None,

&#x20;   series\_id: str | None = None,

) -> TaskSeries:

&#x20;   """Build an ordered TaskSeries for `config\_id` (optionally restricted to `seed\_subset`)."""

&#x20;   \_require\_headline\_or\_success\_allowed(envelope, require\_costs=False)

&#x20;   declared\_seeds = envelope.expected\_plan.seeds\_for\_config(config\_id)

&#x20;   if seed\_subset is None:

&#x20;       active\_seeds = declared\_seeds

&#x20;       kind = "config"

&#x20;   else:

&#x20;       active\_seeds = tuple(seed\_subset)

&#x20;       if not active\_seeds:

&#x20;           raise ValueError("seed\_subset must be non-empty")

&#x20;       declared\_set = set(declared\_seeds)

&#x20;       for s in active\_seeds:

&#x20;           if s not in declared\_set:

&#x20;               raise ValueError(

&#x20;                   f"Seed {s} in seed\_subset is not in declared seeds {declared\_seeds} "

&#x20;                   f"for config {config\_id!r}"

&#x20;               )

&#x20;       kind = "seed\_subset"



&#x20;   cell\_lookup: dict\[tuple\[str, int], NormalizedRecord] = {}

&#x20;   for rec in envelope.records:

&#x20;       if rec.config\_id == config\_id:

&#x20;           cell\_lookup\[(rec.task\_id, rec.seed)] = rec



&#x20;   k\_c = len(active\_seeds)

&#x20;   task\_points: list\[TaskPoint] = \[]

&#x20;   has\_complete\_costs = True



&#x20;   for task\_id in envelope.expected\_plan.tasks:

&#x20;       runs = \[cell\_lookup\[(task\_id, s)] for s in active\_seeds]

&#x20;       family\_id = runs\[0].family\_id

&#x20;       solved\_count = sum(1 for r in runs if r.outcome == "solved")

&#x20;       pass\_rate = Fraction(solved\_count, k\_c)



&#x20;       if any(r.cost\_nano\_usd is None for r in runs):

&#x20;           has\_complete\_costs = False

&#x20;           mean\_cost: Fraction | None = None

&#x20;           actual\_cost: int | None = None

&#x20;       else:

&#x20;           actual\_cost = sum(r.cost\_nano\_usd for r in runs if r.cost\_nano\_usd is not None)

&#x20;           mean\_cost = Fraction(actual\_cost, k\_c)



&#x20;       task\_points.append(

&#x20;           TaskPoint(

&#x20;               task\_id=task\_id,

&#x20;               family\_id=family\_id,

&#x20;               seed\_count=k\_c,

&#x20;               pass\_rate=pass\_rate,

&#x20;               mean\_cost\_nanos=mean\_cost,

&#x20;               actual\_all\_seeds\_cost\_nanos=actual\_cost,

&#x20;           )

&#x20;       )



&#x20;   return TaskSeries(

&#x20;       series\_id=series\_id if series\_id is not None else config\_id,

&#x20;       series\_kind=kind,

&#x20;       tasks=tuple(task\_points),

&#x20;       declared\_seed\_count=k\_c,

&#x20;       has\_complete\_costs=has\_complete\_costs,

&#x20;   )





def \_compute\_secondary\_metrics(

&#x20;   envelope: NormalizedEnvelope,

&#x20;   config\_id: str,

) -> dict\[str, SecondaryMetricSummary]:

&#x20;   declared\_seeds = envelope.expected\_plan.seeds\_for\_config(config\_id)

&#x20;   k\_c = len(declared\_seeds)

&#x20;   tasks = envelope.expected\_plan.tasks

&#x20;   n\_tasks = len(tasks)

&#x20;   total\_runs = n\_tasks \* k\_c



&#x20;   cell\_lookup: dict\[tuple\[str, int], NormalizedRecord] = {

&#x20;       (r.task\_id, r.seed): r for r in envelope.records if r.config\_id == config\_id

&#x20;   }



&#x20;   extractors: dict\[str, Any] = {

&#x20;       "turns": lambda r: Fraction(r.turns, 1) if r.turns is not None else None,

&#x20;       "commands": lambda r: Fraction(r.commands, 1) if r.commands is not None else None,

&#x20;       "actual\_prompt\_tokens": (

&#x20;           lambda r: Fraction(r.actual\_prompt\_tokens, 1)

&#x20;           if r.actual\_prompt\_tokens is not None

&#x20;           else None

&#x20;       ),

&#x20;       "actual\_completion\_tokens": (

&#x20;           lambda r: Fraction(r.actual\_completion\_tokens, 1)

&#x20;           if r.actual\_completion\_tokens is not None

&#x20;           else None

&#x20;       ),

&#x20;       "wall\_seconds": lambda r: r.wall\_seconds,

&#x20;       "hit\_step\_cap\_rate": lambda r: Fraction(1 if r.signals.hit\_step\_cap else 0, 1),

&#x20;       "no\_command\_rate": lambda r: Fraction(str(r.signals.no\_command\_rate)),

&#x20;   }



&#x20;   summaries: dict\[str, SecondaryMetricSummary] = {}

&#x20;   for name, fn in extractors.items():

&#x20;       known\_runs = 0

&#x20;       missing\_runs = 0

&#x20;       all\_sum = Fraction(0, 1)

&#x20;       task\_means: list\[Fraction] = \[]

&#x20;       all\_tasks\_complete = True



&#x20;       for t\_id in tasks:

&#x20;           t\_vals: list\[Fraction] = \[]

&#x20;           for s in declared\_seeds:

&#x20;               val = fn(cell\_lookup\[(t\_id, s)])

&#x20;               if val is None:

&#x20;                   missing\_runs += 1

&#x20;                   all\_tasks\_complete = False

&#x20;               else:

&#x20;                   known\_runs += 1

&#x20;                   all\_sum += val

&#x20;                   t\_vals.append(val)

&#x20;           if len(t\_vals) == k\_c:

&#x20;               task\_means.append(sum(t\_vals, Fraction(0, 1)) / Fraction(k\_c, 1))



&#x20;       if all\_tasks\_complete and len(task\_means) == n\_tasks:

&#x20;           tw\_mean: Fraction | UndefinedValue = sum(task\_means, Fraction(0, 1)) / Fraction(

&#x20;               n\_tasks, 1

&#x20;           )

&#x20;           rep\_sum: Fraction | UndefinedValue = all\_sum

&#x20;       else:

&#x20;           reason = "absent\_optional\_metric" if known\_runs == 0 else "partial\_optional\_metric"

&#x20;           tw\_mean = UndefinedValue(

&#x20;               reason=reason, numerator=known\_runs, denominator=total\_runs

&#x20;           )

&#x20;           rep\_sum = UndefinedValue(

&#x20;               reason=reason, numerator=known\_runs, denominator=total\_runs

&#x20;           )



&#x20;       summaries\[name] = SecondaryMetricSummary(

&#x20;           metric\_name=name,

&#x20;           total\_runs=total\_runs,

&#x20;           known\_runs=known\_runs,

&#x20;           missing\_runs=missing\_runs,

&#x20;           task\_weighted\_mean=tw\_mean,

&#x20;           all\_repetitions\_sum=rep\_sum,

&#x20;       )



&#x20;   return summaries





def compute\_config\_metrics(envelope: NormalizedEnvelope, config\_id: str) -> ConfigMetrics:

&#x20;   """Compute exact WP2 primary and secondary metrics for a single configuration."""

&#x20;   series = build\_config\_task\_series(envelope, config\_id)

&#x20;   point = evaluate\_series\_point(config\_id, series.tasks, include\_actual\_spend=True)

&#x20;   declared\_seeds = envelope.expected\_plan.seeds\_for\_config(config\_id)

&#x20;   split = envelope.audit.splits\_present\[0] if envelope.audit.splits\_present else "train"

&#x20;   secondary = \_compute\_secondary\_metrics(envelope, config\_id)



&#x20;   return ConfigMetrics(

&#x20;       config\_id=config\_id,

&#x20;       dataset\_id=envelope.dataset\_id,

&#x20;       split=split,

&#x20;       n\_tasks=series.n\_tasks,

&#x20;       declared\_seeds=declared\_seeds,

&#x20;       total\_runs=series.n\_tasks \* len(declared\_seeds),

&#x20;       primary=point,

&#x20;       task\_points=series.tasks,

&#x20;       secondary\_metrics=secondary,

&#x20;   )





def compute\_all\_config\_metrics(envelope: NormalizedEnvelope) -> dict\[str, ConfigMetrics]:

&#x20;   """Compute WP2 metrics for all configurations in expected\_plan."""

&#x20;   \_require\_headline\_or\_success\_allowed(envelope, require\_costs=False)

&#x20;   return {

&#x20;       cfg\_id: compute\_config\_metrics(envelope, cfg\_id)

&#x20;       for cfg\_id in sorted(envelope.expected\_plan.config\_ids)

&#x20;   }





def compute\_empirical\_quantile(sorted\_values: Sequence\[Fraction], q: Fraction) -> Fraction:

&#x20;   """Compute exact piecewise-linear empirical quantile (Hyndman-Fan type 7 over Fractions).



&#x20;   For sorted values x\[0] <= x\[1] <= ... <= x\[m-1] and quantile q in \[0, 1]:

&#x20;     index h = q \* (m - 1)

&#x20;     lo = floor(h), hi = ceil(h), frac = h - lo

&#x20;     quantile = x\[lo] + frac \* (x\[hi] - x\[lo])

&#x20;   """

&#x20;   if not sorted\_values:

&#x20;       raise ValueError("Cannot compute quantile of empty sequence")

&#x20;   if q < 0 or q > 1:

&#x20;       raise ValueError(f"Quantile q must be in \[0, 1], got {q}")

&#x20;   m = len(sorted\_values)

&#x20;   if m == 1:

&#x20;       return sorted\_values\[0]

&#x20;   h = q \* Fraction(m - 1, 1)

&#x20;   lo = math.floor(h)

&#x20;   hi = math.ceil(h)

&#x20;   if lo == hi:

&#x20;       return sorted\_values\[lo]

&#x20;   weight = h - Fraction(lo, 1)

&#x20;   return sorted\_values\[lo] + weight \* (sorted\_values\[hi] - sorted\_values\[lo])





def \_build\_bootstrap\_interval(

&#x20;   metric\_name: str,

&#x20;   point\_estimate: Fraction | UndefinedValue,

&#x20;   draws: Sequence\[Fraction | UndefinedValue],

&#x20;   confidence\_level: Fraction,

&#x20;   \*,

&#x20;   zero\_solve\_draws: int = 0,

) -> BootstrapInterval:

&#x20;   replicates = len(draws)

&#x20;   defined\_vals: list\[Fraction] = \[d for d in draws if isinstance(d, Fraction)]

&#x20;   undefined\_count = replicates - len(defined\_vals)



&#x20;   alpha = Fraction(1, 1) - confidence\_level

&#x20;   q\_low = alpha / Fraction(2, 1)

&#x20;   q\_high = Fraction(1, 1) - q\_low



&#x20;   # Never silently discard undefined / zero-solve draws and report a conditional interval

&#x20;   # as an unconditional confidence interval.

&#x20;   if isinstance(point\_estimate, UndefinedValue) or undefined\_count > 0 or not defined\_vals:

&#x20;       reason = (

&#x20;           "unconditional\_interval\_blocked\_by\_zero\_solve\_draws"

&#x20;           if zero\_solve\_draws > 0

&#x20;           else (

&#x20;               point\_estimate.reason

&#x20;               if isinstance(point\_estimate, UndefinedValue)

&#x20;               else "undefined\_bootstrap\_draws\_present"

&#x20;           )

&#x20;       )

&#x20;       undef = UndefinedValue(

&#x20;           reason=reason,

&#x20;           numerator=len(defined\_vals),

&#x20;           denominator=replicates,

&#x20;       )

&#x20;       return BootstrapInterval(

&#x20;           metric\_name=metric\_name,

&#x20;           point\_estimate=point\_estimate,

&#x20;           lower=undef,

&#x20;           upper=undef,

&#x20;           confidence\_level=confidence\_level,

&#x20;           replicates=replicates,

&#x20;           defined\_draws=len(defined\_vals),

&#x20;           undefined\_draws=undefined\_count,

&#x20;           zero\_solve\_draws=zero\_solve\_draws,

&#x20;       )



&#x20;   sorted\_vals = sorted(defined\_vals)

&#x20;   return BootstrapInterval(

&#x20;       metric\_name=metric\_name,

&#x20;       point\_estimate=point\_estimate,

&#x20;       lower=compute\_empirical\_quantile(sorted\_vals, q\_low),

&#x20;       upper=compute\_empirical\_quantile(sorted\_vals, q\_high),

&#x20;       confidence\_level=confidence\_level,

&#x20;       replicates=replicates,

&#x20;       defined\_draws=len(defined\_vals),

&#x20;       undefined\_draws=0,

&#x20;       zero\_solve\_draws=zero\_solve\_draws,

&#x20;   )





def \_validate\_bootstrap\_params(

&#x20;   replicates: int,

&#x20;   n\_units: int,

&#x20;   n\_series: int,

&#x20;   confidence\_level: float | Fraction,

) -> Fraction:

&#x20;   if isinstance(replicates, bool) or not isinstance(replicates, int):

&#x20;       raise AnalysisInputError("replicates must be an integer")

&#x20;   if replicates < 1 or replicates > MAX\_BOOTSTRAP\_REPLICATES:

&#x20;       raise AnalysisInputError(

&#x20;           f"replicates must be between 1 and {MAX\_BOOTSTRAP\_REPLICATES}, got {replicates}"

&#x20;       )

&#x20;   workload = replicates \* max(1, n\_units) \* max(1, n\_series)

&#x20;   if workload > MAX\_BOOTSTRAP\_WORKLOAD:

&#x20;       raise AnalysisInputError(

&#x20;           f"Estimated bootstrap workload ({workload} task-series evaluations) exceeds "

&#x20;           f"maximum of {MAX\_BOOTSTRAP\_WORKLOAD}"

&#x20;       )

&#x20;   if isinstance(confidence\_level, bool) or not isinstance(

&#x20;       confidence\_level, (int, float, Fraction)

&#x20;   ):

&#x20;       raise AnalysisInputError("confidence\_level must be a number in (0, 1)")

&#x20;   if isinstance(confidence\_level, float) and not math.isfinite(confidence\_level):

&#x20;       raise AnalysisInputError("confidence\_level must be finite")

&#x20;   conf = (

&#x20;       confidence\_level

&#x20;       if isinstance(confidence\_level, Fraction)

&#x20;       else Fraction(str(confidence\_level))

&#x20;   )

&#x20;   if conf <= 0 or conf >= 1:

&#x20;       raise AnalysisInputError("confidence\_level must be strictly between 0 and 1")

&#x20;   return conf





def paired\_task\_bootstrap(

&#x20;   series\_list: Sequence\[TaskSeries],

&#x20;   \*,

&#x20;   replicates: int = DEFAULT\_BOOTSTRAP\_REPLICATES,

&#x20;   seed: int = 17,

&#x20;   confidence\_level: float | Fraction = Fraction(95, 100),

&#x20;   comparison\_pairs: Sequence\[tuple\[str, str]] | None = None,

&#x20;   sampled\_task\_indices: Sequence\[Sequence\[int]] | None = None,

) -> PairedBootstrapResult:

&#x20;   """WP3 paired task bootstrap across all supplied TaskSeries using shared task index draws."""

&#x20;   if not series\_list:

&#x20;       raise AnalysisInputError("series\_list must be non-empty")



&#x20;   n\_tasks = series\_list\[0].n\_tasks

&#x20;   task\_ids = tuple(tp.task\_id for tp in series\_list\[0].tasks)

&#x20;   series\_by\_id: dict\[str, TaskSeries] = {}

&#x20;   for s in series\_list:

&#x20;       if s.series\_id in series\_by\_id:

&#x20;           raise AnalysisInputError(f"Duplicate series\_id in bootstrap: {s.series\_id!r}")

&#x20;       if s.n\_tasks != n\_tasks or tuple(tp.task\_id for tp in s.tasks) != task\_ids:

&#x20;           raise AnalysisInputError(

&#x20;               f"Series {s.series\_id!r} task alignment does not match {series\_list\[0].series\_id!r}"

&#x20;           )

&#x20;       series\_by\_id\[s.series\_id] = s



&#x20;   if sampled\_task\_indices is not None:

&#x20;       if not sampled\_task\_indices:

&#x20;           raise AnalysisInputError("sampled\_task\_indices must be non-empty when provided")

&#x20;       effective\_replicates = len(sampled\_task\_indices)

&#x20;   else:

&#x20;       effective\_replicates = replicates



&#x20;   conf = \_validate\_bootstrap\_params(

&#x20;       effective\_replicates, n\_tasks, len(series\_list), confidence\_level

&#x20;   )



&#x20;   if sampled\_task\_indices is None:

&#x20;       if isinstance(seed, bool) or not isinstance(seed, int):

&#x20;           raise AnalysisInputError("seed must be an integer")

&#x20;       rng = random.Random(seed)

&#x20;       index\_draws: list\[tuple\[int, ...]] = \[

&#x20;           tuple(rng.randrange(n\_tasks) for \_ in range(n\_tasks))

&#x20;           for \_ in range(effective\_replicates)

&#x20;       ]

&#x20;       used\_seed: int | None = seed

&#x20;   else:

&#x20;       index\_draws = \[]

&#x20;       for draw in sampled\_task\_indices:

&#x20;           if len(draw) != n\_tasks:

&#x20;               raise AnalysisInputError(

&#x20;                   f"Each injected index draw must have length n\_tasks={n\_tasks}"

&#x20;               )

&#x20;           for idx in draw:

&#x20;               if isinstance(idx, bool) or not isinstance(idx, int) or idx < 0 or idx >= n\_tasks:

&#x20;                   raise AnalysisInputError(f"Invalid task index {idx!r} in sampled\_task\_indices")

&#x20;           index\_draws.append(tuple(draw))

&#x20;       used\_seed = None



&#x20;   if comparison\_pairs is None:

&#x20;       ordered\_ids = sorted(series\_by\_id)

&#x20;       pairs: list\[tuple\[str, str]] = \[]

&#x20;       for i in range(len(ordered\_ids)):

&#x20;           for j in range(i + 1, len(ordered\_ids)):

&#x20;               pairs.append((ordered\_ids\[i], ordered\_ids\[j]))

&#x20;   else:

&#x20;       pairs = list(comparison\_pairs)

&#x20;       for base\_id, targ\_id in pairs:

&#x20;           if base\_id not in series\_by\_id or targ\_id not in series\_by\_id:

&#x20;               raise AnalysisInputError(

&#x20;                   f"Unknown series in comparison\_pairs: ({base\_id!r}, {targ\_id!r})"

&#x20;               )



&#x20;   point\_by\_series: dict\[str, SeriesPoint] = {

&#x20;       s\_id: evaluate\_series\_point(s\_id, s.tasks, include\_actual\_spend=True)

&#x20;       for s\_id, s in series\_by\_id.items()

&#x20;   }



&#x20;   draws\_by\_series: dict\[str, list\[SeriesPoint]] = {s\_id: \[] for s\_id in series\_by\_id}

&#x20;   for indices in index\_draws:

&#x20;       for s\_id, s in series\_by\_id.items():

&#x20;           sampled\_points = \[s.tasks\[idx] for idx in indices]

&#x20;           draws\_by\_series\[s\_id].append(

&#x20;               evaluate\_series\_point(s\_id, sampled\_points, include\_actual\_spend=False)

&#x20;           )



&#x20;   series\_summaries: dict\[str, SeriesBootstrapSummary] = {}

&#x20;   for s\_id, pt in point\_by\_series.items():

&#x20;       s\_draws = draws\_by\_series\[s\_id]

&#x20;       zero\_solves = sum(1 for d in s\_draws if d.expected\_solved\_tasks == 0)

&#x20;       series\_summaries\[s\_id] = SeriesBootstrapSummary(

&#x20;           series\_id=s\_id,

&#x20;           pass\_at\_1=\_build\_bootstrap\_interval(

&#x20;               "pass\_at\_1",

&#x20;               pt.pass\_at\_1,

&#x20;               \[d.pass\_at\_1 for d in s\_draws],

&#x20;               conf,

&#x20;           ),

&#x20;           expected\_total\_cost\_nanos=\_build\_bootstrap\_interval(

&#x20;               "expected\_total\_cost\_nanos",

&#x20;               pt.expected\_total\_cost\_nanos,

&#x20;               \[d.expected\_total\_cost\_nanos for d in s\_draws],

&#x20;               conf,

&#x20;           ),

&#x20;           mean\_task\_cost\_nanos=\_build\_bootstrap\_interval(

&#x20;               "mean\_task\_cost\_nanos",

&#x20;               pt.mean\_task\_cost\_nanos,

&#x20;               \[d.mean\_task\_cost\_nanos for d in s\_draws],

&#x20;               conf,

&#x20;           ),

&#x20;           expected\_cost\_per\_solved\_nanos=\_build\_bootstrap\_interval(

&#x20;               "expected\_cost\_per\_solved\_nanos",

&#x20;               pt.expected\_cost\_per\_solved\_nanos,

&#x20;               \[d.expected\_cost\_per\_solved\_nanos for d in s\_draws],

&#x20;               conf,

&#x20;               zero\_solve\_draws=zero\_solves,

&#x20;           ),

&#x20;       )



&#x20;   paired\_diffs: list\[PairedDifferenceSummary] = \[]

&#x20;   for base\_id, targ\_id in pairs:

&#x20;       base\_pt = point\_by\_series\[base\_id]

&#x20;       targ\_pt = point\_by\_series\[targ\_id]

&#x20;       base\_draws = draws\_by\_series\[base\_id]

&#x20;       targ\_draws = draws\_by\_series\[targ\_id]



&#x20;       # 1. Delta pass@1

&#x20;       pt\_delta\_p = targ\_pt.pass\_at\_1 - base\_pt.pass\_at\_1

&#x20;       draws\_delta\_p = \[t.pass\_at\_1 - b.pass\_at\_1 for b, t in zip(base\_draws, targ\_draws)]



&#x20;       # 2. Delta expected total cost

&#x20;       if isinstance(base\_pt.expected\_total\_cost\_nanos, Fraction) and isinstance(

&#x20;           targ\_pt.expected\_total\_cost\_nanos, Fraction

&#x20;       ):

&#x20;           pt\_delta\_cost: Fraction | UndefinedValue = (

&#x20;               targ\_pt.expected\_total\_cost\_nanos - base\_pt.expected\_total\_cost\_nanos

&#x20;           )

&#x20;       else:

&#x20;           pt\_delta\_cost = UndefinedValue(reason="missing\_cost\_nano\_usd")



&#x20;       draws\_delta\_cost: list\[Fraction | UndefinedValue] = \[]

&#x20;       for b, t in zip(base\_draws, targ\_draws):

&#x20;           if isinstance(b.expected\_total\_cost\_nanos, Fraction) and isinstance(

&#x20;               t.expected\_total\_cost\_nanos, Fraction

&#x20;           ):

&#x20;               draws\_delta\_cost.append(

&#x20;                   t.expected\_total\_cost\_nanos - b.expected\_total\_cost\_nanos

&#x20;               )

&#x20;           else:

&#x20;               draws\_delta\_cost.append(UndefinedValue(reason="missing\_cost\_nano\_usd"))



&#x20;       # 3. Delta expected cost per solved

&#x20;       if isinstance(base\_pt.expected\_cost\_per\_solved\_nanos, Fraction) and isinstance(

&#x20;           targ\_pt.expected\_cost\_per\_solved\_nanos, Fraction

&#x20;       ):

&#x20;           pt\_delta\_cps: Fraction | UndefinedValue = (

&#x20;               targ\_pt.expected\_cost\_per\_solved\_nanos - base\_pt.expected\_cost\_per\_solved\_nanos

&#x20;           )

&#x20;       else:

&#x20;           pt\_delta\_cps = UndefinedValue(

&#x20;               reason=(

&#x20;                   "zero\_expected\_solves"

&#x20;                   if (base\_pt.expected\_solved\_tasks == 0 or targ\_pt.expected\_solved\_tasks == 0)

&#x20;                   else "missing\_cost\_nano\_usd"

&#x20;               )

&#x20;           )



&#x20;       draws\_delta\_cps: list\[Fraction | UndefinedValue] = \[]

&#x20;       pair\_zero\_solves = 0

&#x20;       for b, t in zip(base\_draws, targ\_draws):

&#x20;           if b.expected\_solved\_tasks == 0 or t.expected\_solved\_tasks == 0:

&#x20;               pair\_zero\_solves += 1

&#x20;           if isinstance(b.expected\_cost\_per\_solved\_nanos, Fraction) and isinstance(

&#x20;               t.expected\_cost\_per\_solved\_nanos, Fraction

&#x20;           ):

&#x20;               draws\_delta\_cps.append(

&#x20;                   t.expected\_cost\_per\_solved\_nanos - b.expected\_cost\_per\_solved\_nanos

&#x20;               )

&#x20;           else:

&#x20;               draws\_delta\_cps.append(

&#x20;                   UndefinedValue(

&#x20;                       reason=(

&#x20;                           "zero\_expected\_solves"

&#x20;                           if (b.expected\_solved\_tasks == 0 or t.expected\_solved\_tasks == 0)

&#x20;                           else "missing\_cost\_nano\_usd"

&#x20;                       )

&#x20;                   )

&#x20;               )



&#x20;       paired\_diffs.append(

&#x20;           PairedDifferenceSummary(

&#x20;               baseline\_id=base\_id,

&#x20;               target\_id=targ\_id,

&#x20;               delta\_pass\_at\_1=\_build\_bootstrap\_interval(

&#x20;                   "delta\_pass\_at\_1", pt\_delta\_p, draws\_delta\_p, conf

&#x20;               ),

&#x20;               delta\_expected\_total\_cost\_nanos=\_build\_bootstrap\_interval(

&#x20;                   "delta\_expected\_total\_cost\_nanos", pt\_delta\_cost, draws\_delta\_cost, conf

&#x20;               ),

&#x20;               delta\_expected\_cost\_per\_solved\_nanos=\_build\_bootstrap\_interval(

&#x20;                   "delta\_expected\_cost\_per\_solved\_nanos",

&#x20;                   pt\_delta\_cps,

&#x20;                   draws\_delta\_cps,

&#x20;                   conf,

&#x20;                   zero\_solve\_draws=pair\_zero\_solves,

&#x20;               ),

&#x20;           )

&#x20;       )



&#x20;   return PairedBootstrapResult(

&#x20;       method\_version=FOUNDATION\_METHOD\_VERSION,

&#x20;       estimand\_label="primary\_equal\_task\_weighted\_independent\_task\_bootstrap",

&#x20;       replicates=effective\_replicates,

&#x20;       seed=used\_seed,

&#x20;       confidence\_level=conf,

&#x20;       n\_tasks=n\_tasks,

&#x20;       quantile\_method=QUANTILE\_METHOD,

&#x20;       series\_summaries=series\_summaries,

&#x20;       paired\_differences=tuple(paired\_diffs),

&#x20;   )





def family\_cluster\_bootstrap(

&#x20;   series\_list: Sequence\[TaskSeries],

&#x20;   \*,

&#x20;   replicates: int = DEFAULT\_BOOTSTRAP\_REPLICATES,

&#x20;   seed: int = 17,

&#x20;   confidence\_level: float | Fraction = Fraction(95, 100),

&#x20;   comparison\_pairs: Sequence\[tuple\[str, str]] | None = None,

&#x20;   sampled\_family\_indices: Sequence\[Sequence\[int]] | None = None,

) -> FamilyBootstrapResult:

&#x20;   """WP4 sensitivity: resample task families with replacement and preserve original\_n cost target."""

&#x20;   if not series\_list:

&#x20;       raise AnalysisInputError("series\_list must be non-empty")



&#x20;   original\_n = series\_list\[0].n\_tasks

&#x20;   task\_ids = tuple(tp.task\_id for tp in series\_list\[0].tasks)

&#x20;   family\_ids\_by\_task = tuple(tp.family\_id for tp in series\_list\[0].tasks)



&#x20;   series\_by\_id: dict\[str, TaskSeries] = {}

&#x20;   for s in series\_list:

&#x20;       if s.series\_id in series\_by\_id:

&#x20;           raise AnalysisInputError(f"Duplicate series\_id: {s.series\_id!r}")

&#x20;       if (

&#x20;           s.n\_tasks != original\_n

&#x20;           or tuple(tp.task\_id for tp in s.tasks) != task\_ids

&#x20;           or tuple(tp.family\_id for tp in s.tasks) != family\_ids\_by\_task

&#x20;       ):

&#x20;           raise AnalysisInputError(

&#x20;               f"Series {s.series\_id!r} task/family alignment does not match {series\_list\[0].series\_id!r}"

&#x20;           )

&#x20;       series\_by\_id\[s.series\_id] = s



&#x20;   # Preserve deterministic family order by first appearance in expected\_plan.tasks

&#x20;   ordered\_families: list\[str] = \[]

&#x20;   family\_to\_task\_indices: dict\[str, list\[int]] = {}

&#x20;   for idx, fam\_id in enumerate(family\_ids\_by\_task):

&#x20;       if fam\_id not in family\_to\_task\_indices:

&#x20;           ordered\_families.append(fam\_id)

&#x20;           family\_to\_task\_indices\[fam\_id] = \[]

&#x20;       family\_to\_task\_indices\[fam\_id].append(idx)



&#x20;   n\_families = len(ordered\_families)

&#x20;   family\_sizes = {fam: len(indices) for fam, indices in family\_to\_task\_indices.items()}



&#x20;   if sampled\_family\_indices is not None:

&#x20;       if not sampled\_family\_indices:

&#x20;           raise AnalysisInputError("sampled\_family\_indices must be non-empty when provided")

&#x20;       effective\_replicates = len(sampled\_family\_indices)

&#x20;   else:

&#x20;       effective\_replicates = replicates



&#x20;   conf = \_validate\_bootstrap\_params(

&#x20;       effective\_replicates, original\_n, len(series\_list), confidence\_level

&#x20;   )



&#x20;   if sampled\_family\_indices is None:

&#x20;       if isinstance(seed, bool) or not isinstance(seed, int):

&#x20;           raise AnalysisInputError("seed must be an integer")

&#x20;       rng = random.Random(seed)

&#x20;       fam\_draws: list\[tuple\[int, ...]] = \[

&#x20;           tuple(rng.randrange(n\_families) for \_ in range(n\_families))

&#x20;           for \_ in range(effective\_replicates)

&#x20;       ]

&#x20;       used\_seed: int | None = seed

&#x20;   else:

&#x20;       fam\_draws = \[]

&#x20;       for draw in sampled\_family\_indices:

&#x20;           if len(draw) != n\_families:

&#x20;               raise AnalysisInputError(

&#x20;                   f"Each injected family draw must have length n\_families={n\_families}"

&#x20;               )

&#x20;           for f\_idx in draw:

&#x20;               if (

&#x20;                   isinstance(f\_idx, bool)

&#x20;                   or not isinstance(f\_idx, int)

&#x20;                   or f\_idx < 0

&#x20;                   or f\_idx >= n\_families

&#x20;               ):

&#x20;                   raise AnalysisInputError(f"Invalid family index {f\_idx!r}")

&#x20;           fam\_draws.append(tuple(draw))

&#x20;       used\_seed = None



&#x20;   if comparison\_pairs is None:

&#x20;       ordered\_ids = sorted(series\_by\_id)

&#x20;       pairs: list\[tuple\[str, str]] = \[]

&#x20;       for i in range(len(ordered\_ids)):

&#x20;           for j in range(i + 1, len(ordered\_ids)):

&#x20;               pairs.append((ordered\_ids\[i], ordered\_ids\[j]))

&#x20;   else:

&#x20;       pairs = list(comparison\_pairs)

&#x20;       for base\_id, targ\_id in pairs:

&#x20;           if base\_id not in series\_by\_id or targ\_id not in series\_by\_id:

&#x20;               raise AnalysisInputError(

&#x20;                   f"Unknown series in comparison\_pairs: ({base\_id!r}, {targ\_id!r})"

&#x20;               )



&#x20;   point\_by\_series: dict\[str, SeriesPoint] = {

&#x20;       s\_id: evaluate\_series\_point(

&#x20;           s\_id, s.tasks, target\_n\_tasks=original\_n, include\_actual\_spend=True

&#x20;       )

&#x20;       for s\_id, s in series\_by\_id.items()

&#x20;   }



&#x20;   draws\_by\_series: dict\[str, list\[SeriesPoint]] = {s\_id: \[] for s\_id in series\_by\_id}

&#x20;   resampled\_task\_counts: list\[int] = \[]



&#x20;   for f\_indices in fam\_draws:

&#x20;       expanded\_task\_indices: list\[int] = \[]

&#x20;       for f\_idx in f\_indices:

&#x20;           fam\_id = ordered\_families\[f\_idx]

&#x20;           expanded\_task\_indices.extend(family\_to\_task\_indices\[fam\_id])

&#x20;       resampled\_task\_counts.append(len(expanded\_task\_indices))



&#x20;       for s\_id, s in series\_by\_id.items():

&#x20;           sampled\_tasks = \[s.tasks\[t\_idx] for t\_idx in expanded\_task\_indices]

&#x20;           draws\_by\_series\[s\_id].append(

&#x20;               evaluate\_series\_point(

&#x20;                   s\_id,

&#x20;                   sampled\_tasks,

&#x20;                   target\_n\_tasks=original\_n,

&#x20;                   include\_actual\_spend=False,

&#x20;               )

&#x20;           )



&#x20;   series\_summaries: dict\[str, FamilySeriesSummary] = {}

&#x20;   for s\_id, pt in point\_by\_series.items():

&#x20;       s\_draws = draws\_by\_series\[s\_id]

&#x20;       zero\_solves = sum(1 for d in s\_draws if d.expected\_solved\_tasks == 0)

&#x20;       series\_summaries\[s\_id] = FamilySeriesSummary(

&#x20;           series\_id=s\_id,

&#x20;           pass\_at\_1=\_build\_bootstrap\_interval(

&#x20;               "pass\_at\_1",

&#x20;               pt.pass\_at\_1,

&#x20;               \[d.pass\_at\_1 for d in s\_draws],

&#x20;               conf,

&#x20;           ),

&#x20;           target\_n\_expected\_total\_cost\_nanos=\_build\_bootstrap\_interval(

&#x20;               "target\_n\_expected\_total\_cost\_nanos",

&#x20;               pt.expected\_total\_cost\_nanos,

&#x20;               \[d.expected\_total\_cost\_nanos for d in s\_draws],

&#x20;               conf,

&#x20;           ),

&#x20;           mean\_task\_cost\_nanos=\_build\_bootstrap\_interval(

&#x20;               "mean\_task\_cost\_nanos",

&#x20;               pt.mean\_task\_cost\_nanos,

&#x20;               \[d.mean\_task\_cost\_nanos for d in s\_draws],

&#x20;               conf,

&#x20;           ),

&#x20;           expected\_cost\_per\_solved\_nanos=\_build\_bootstrap\_interval(

&#x20;               "expected\_cost\_per\_solved\_nanos",

&#x20;               pt.expected\_cost\_per\_solved\_nanos,

&#x20;               \[d.expected\_cost\_per\_solved\_nanos for d in s\_draws],

&#x20;               conf,

&#x20;               zero\_solve\_draws=zero\_solves,

&#x20;           ),

&#x20;       )



&#x20;   paired\_diffs: list\[PairedDifferenceSummary] = \[]

&#x20;   for base\_id, targ\_id in pairs:

&#x20;       base\_pt = point\_by\_series\[base\_id]

&#x20;       targ\_pt = point\_by\_series\[targ\_id]

&#x20;       base\_draws = draws\_by\_series\[base\_id]

&#x20;       targ\_draws = draws\_by\_series\[targ\_id]



&#x20;       pt\_delta\_p = targ\_pt.pass\_at\_1 - base\_pt.pass\_at\_1

&#x20;       draws\_delta\_p = \[t.pass\_at\_1 - b.pass\_at\_1 for b, t in zip(base\_draws, targ\_draws)]



&#x20;       if isinstance(base\_pt.expected\_total\_cost\_nanos, Fraction) and isinstance(

&#x20;           targ\_pt.expected\_total\_cost\_nanos, Fraction

&#x20;       ):

&#x20;           pt\_delta\_cost: Fraction | UndefinedValue = (

&#x20;               targ\_pt.expected\_total\_cost\_nanos - base\_pt.expected\_total\_cost\_nanos

&#x20;           )

&#x20;       else:

&#x20;           pt\_delta\_cost = UndefinedValue(reason="missing\_cost\_nano\_usd")



&#x20;       draws\_delta\_cost: list\[Fraction | UndefinedValue] = \[]

&#x20;       for b, t in zip(base\_draws, targ\_draws):

&#x20;           if isinstance(b.expected\_total\_cost\_nanos, Fraction) and isinstance(

&#x20;               t.expected\_total\_cost\_nanos, Fraction

&#x20;           ):

&#x20;               draws\_delta\_cost.append(

&#x20;                   t.expected\_total\_cost\_nanos - b.expected\_total\_cost\_nanos

&#x20;               )

&#x20;           else:

&#x20;               draws\_delta\_cost.append(UndefinedValue(reason="missing\_cost\_nano\_usd"))



&#x20;       if isinstance(base\_pt.expected\_cost\_per\_solved\_nanos, Fraction) and isinstance(

&#x20;           targ\_pt.expected\_cost\_per\_solved\_nanos, Fraction

&#x20;       ):

&#x20;           pt\_delta\_cps: Fraction | UndefinedValue = (

&#x20;               targ\_pt.expected\_cost\_per\_solved\_nanos - base\_pt.expected\_cost\_per\_solved\_nanos

&#x20;           )

&#x20;       else:

&#x20;           pt\_delta\_cps = UndefinedValue(

&#x20;               reason=(

&#x20;                   "zero\_expected\_solves"

&#x20;                   if (base\_pt.expected\_solved\_tasks == 0 or targ\_pt.expected\_solved\_tasks == 0)

&#x20;                   else "missing\_cost\_nano\_usd"

&#x20;               )

&#x20;           )



&#x20;       draws\_delta\_cps: list\[Fraction | UndefinedValue] = \[]

&#x20;       pair\_zero\_solves = 0

&#x20;       for b, t in zip(base\_draws, targ\_draws):

&#x20;           if b.expected\_solved\_tasks == 0 or t.expected\_solved\_tasks == 0:

&#x20;               pair\_zero\_solves += 1

&#x20;           if isinstance(b.expected\_cost\_per\_solved\_nanos, Fraction) and isinstance(

&#x20;               t.expected\_cost\_per\_solved\_nanos, Fraction

&#x20;           ):

&#x20;               draws\_delta\_cps.append(

&#x20;                   t.expected\_cost\_per\_solved\_nanos - b.expected\_cost\_per\_solved\_nanos

&#x20;               )

&#x20;           else:

&#x20;               draws\_delta\_cps.append(

&#x20;                   UndefinedValue(

&#x20;                       reason=(

&#x20;                           "zero\_expected\_solves"

&#x20;                           if (b.expected\_solved\_tasks == 0 or t.expected\_solved\_tasks == 0)

&#x20;                           else "missing\_cost\_nano\_usd"

&#x20;                       )

&#x20;                   )

&#x20;               )



&#x20;       paired\_diffs.append(

&#x20;           PairedDifferenceSummary(

&#x20;               baseline\_id=base\_id,

&#x20;               target\_id=targ\_id,

&#x20;               delta\_pass\_at\_1=\_build\_bootstrap\_interval(

&#x20;                   "delta\_pass\_at\_1", pt\_delta\_p, draws\_delta\_p, conf

&#x20;               ),

&#x20;               delta\_expected\_total\_cost\_nanos=\_build\_bootstrap\_interval(

&#x20;                   "delta\_target\_n\_expected\_total\_cost\_nanos",

&#x20;                   pt\_delta\_cost,

&#x20;                   draws\_delta\_cost,

&#x20;                   conf,

&#x20;               ),

&#x20;               delta\_expected\_cost\_per\_solved\_nanos=\_build\_bootstrap\_interval(

&#x20;                   "delta\_expected\_cost\_per\_solved\_nanos",

&#x20;                   pt\_delta\_cps,

&#x20;                   draws\_delta\_cps,

&#x20;                   conf,

&#x20;                   zero\_solve\_draws=pair\_zero\_solves,

&#x20;               ),

&#x20;           )

&#x20;       )



&#x20;   mean\_n\_star = Fraction(sum(resampled\_task\_counts), len(resampled\_task\_counts))

&#x20;   return FamilyBootstrapResult(

&#x20;       is\_primary=False,

&#x20;       estimand\_label="sensitivity\_family\_cluster\_bootstrap\_task\_weighted\_within\_resampled\_clusters",

&#x20;       weighting\_method=(

&#x20;           "Resample m=n\_families clusters with replacement; include all tasks in each selected "

&#x20;           "family occurrence (retaining all seeds) and weight included task occurrences equally."

&#x20;       ),

&#x20;       total\_cost\_scaling\_rule=(

&#x20;           "Report original\_n \* resampled\_mean\_task\_cost so total-cost intervals remain on the "

&#x20;           "n-task target scale even when resampled task count n\* varies across cluster draws."

&#x20;       ),

&#x20;       replicates=effective\_replicates,

&#x20;       seed=used\_seed,

&#x20;       confidence\_level=conf,

&#x20;       original\_n\_tasks=original\_n,

&#x20;       n\_families=n\_families,

&#x20;       family\_sizes=family\_sizes,

&#x20;       min\_resampled\_tasks=min(resampled\_task\_counts),

&#x20;       max\_resampled\_tasks=max(resampled\_task\_counts),

&#x20;       mean\_resampled\_tasks=mean\_n\_star,

&#x20;       series\_summaries=series\_summaries,

&#x20;       paired\_differences=tuple(paired\_diffs),

&#x20;   )





def seed\_sensitivity\_analysis(

&#x20;   envelope: NormalizedEnvelope,

&#x20;   \*,

&#x20;   seed\_positions: Sequence\[int] | None = None,

&#x20;   seed\_subsets\_by\_config: Mapping\[str, Sequence\[Sequence\[int]]] | None = None,

) -> SeedSensitivityResult:

&#x20;   """WP4 non-primary seed-position and predeclared seed-subset sensitivity analysis."""

&#x20;   \_require\_headline\_or\_success\_allowed(envelope, require\_costs=False)

&#x20;   seeds\_map = envelope.expected\_plan.seeds\_map()

&#x20;   config\_ids = sorted(seeds\_map)



&#x20;   min\_seed\_count = min(len(seeds) for seeds in seeds\_map.values())

&#x20;   common\_positions = tuple(range(min\_seed\_count))



&#x20;   shared\_seeds\_set = set(seeds\_map\[config\_ids\[0]])

&#x20;   for cfg in config\_ids\[1:]:

&#x20;       shared\_seeds\_set \&= set(seeds\_map\[cfg])

&#x20;   shared\_exact\_seeds = tuple(sorted(shared\_seeds\_set))



&#x20;   entries: list\[SeedSensitivityEntry] = \[]



&#x20;   # 1. Full declared seed list per config (reference baseline within sensitivity table)

&#x20;   for cfg in config\_ids:

&#x20;       declared = seeds\_map\[cfg]

&#x20;       series = build\_config\_task\_series(

&#x20;           envelope, cfg, seed\_subset=declared, series\_id=f"{cfg}:all\_declared\_seeds"

&#x20;       )

&#x20;       pt = evaluate\_series\_point(series.series\_id, series.tasks, include\_actual\_spend=True)

&#x20;       entries.append(

&#x20;           SeedSensitivityEntry(

&#x20;               config\_id=cfg,

&#x20;               slice\_label="all\_declared\_seeds",

&#x20;               selected\_seeds=declared,

&#x20;               point=pt,

&#x20;           )

&#x20;       )



&#x20;   # 2. Predeclared single-seed positions (default: all positions available per config)

&#x20;   for cfg in config\_ids:

&#x20;       declared = seeds\_map\[cfg]

&#x20;       positions = (

&#x20;           tuple(range(len(declared)))

&#x20;           if seed\_positions is None

&#x20;           else tuple(p for p in seed\_positions if 0 <= p < len(declared))

&#x20;       )

&#x20;       for pos in positions:

&#x20;           chosen = (declared\[pos],)

&#x20;           label = f"position\_{pos}\_seed\_{declared\[pos]}"

&#x20;           series = build\_config\_task\_series(

&#x20;               envelope, cfg, seed\_subset=chosen, series\_id=f"{cfg}:{label}"

&#x20;           )

&#x20;           pt = evaluate\_series\_point(series.series\_id, series.tasks, include\_actual\_spend=True)

&#x20;           entries.append(

&#x20;               SeedSensitivityEntry(

&#x20;                   config\_id=cfg,

&#x20;                   slice\_label=label,

&#x20;                   selected\_seeds=chosen,

&#x20;                   point=pt,

&#x20;               )

&#x20;           )



&#x20;   # 3. Caller-supplied explicit seed subsets per config

&#x20;   if seed\_subsets\_by\_config is not None:

&#x20;       for cfg in sorted(seed\_subsets\_by\_config):

&#x20;           if cfg not in seeds\_map:

&#x20;               raise AnalysisInputError(f"Unknown config\_id in seed\_subsets\_by\_config: {cfg!r}")

&#x20;           for subset in seed\_subsets\_by\_config\[cfg]:

&#x20;               subset\_tuple = tuple(subset)

&#x20;               if not subset\_tuple:

&#x20;                   raise AnalysisInputError(f"Empty seed subset for config {cfg!r}")

&#x20;               label = "subset\_" + "\_".join(str(s) for s in subset\_tuple)

&#x20;               series = build\_config\_task\_series(

&#x20;                   envelope, cfg, seed\_subset=subset\_tuple, series\_id=f"{cfg}:{label}"

&#x20;               )

&#x20;               pt = evaluate\_series\_point(

&#x20;                   series.series\_id, series.tasks, include\_actual\_spend=True

&#x20;               )

&#x20;               entries.append(

&#x20;                   SeedSensitivityEntry(

&#x20;                       config\_id=cfg,

&#x20;                       slice\_label=label,

&#x20;                       selected\_seeds=subset\_tuple,

&#x20;                       point=pt,

&#x20;                   )

&#x20;               )



&#x20;   note = (

&#x20;       "Non-primary diagnostic only: never select a winning seed or headline metric on held-out. "

&#x20;       "When configs declare unequal seed counts, cross-config single-seed comparisons are valid "

&#x20;       "at predeclared ordinal positions 0..min(k\_c)-1 or on shared\_exact\_seeds, while "

&#x20;       "within-config slices show variance across repetitions."

&#x20;   )



&#x20;   return SeedSensitivityResult(

&#x20;       is\_primary=False,

&#x20;       estimand\_label="sensitivity\_predeclared\_seed\_positions\_and\_subsets",

&#x20;       declared\_seeds\_by\_config=seeds\_map,

&#x20;       common\_seed\_positions=common\_positions,

&#x20;       shared\_exact\_seeds=shared\_exact\_seeds,

&#x20;       comparison\_rules\_note=note,

&#x20;       entries=tuple(entries),

&#x20;   )



```



\---



\## FILE: dojo/bench/frontier.py



```python

"""WP5: Exact rational cost/success Pareto frontiers and tie-group tables on both cost axes."""



from \_\_future\_\_ import annotations



from collections.abc import Sequence

from dataclasses import dataclass

from fractions import Fraction

from typing import Any



from dojo.bench.records import (

&#x20;   AnalysisInputError,

&#x20;   NormalizedEnvelope,

&#x20;   UndefinedValue,

&#x20;   format\_fraction\_Or\_undef,

)

from dojo.bench.stats import ConfigMetrics, SeriesPoint, compute\_all\_config\_metrics



COST\_AXIS\_COST\_PER\_SOLVED: str = "cost\_per\_solved"

COST\_AXIS\_MEAN\_TASK\_COST: str = "mean\_task\_cost"

VALID\_COST\_AXES: frozenset\[str] = frozenset(

&#x20;   {COST\_AXIS\_COST\_PER\_SOLVED, COST\_AXIS\_MEAN\_TASK\_COST}

)



\_\_all\_\_ = \[

&#x20;   "COST\_AXIS\_COST\_PER\_SOLVED",

&#x20;   "COST\_AXIS\_MEAN\_TASK\_COST",

&#x20;   "FrontierRow",

&#x20;   "FrontierTable",

&#x20;   "VALID\_COST\_AXES",

&#x20;   "compute\_both\_frontiers",

&#x20;   "compute\_frontier",

&#x20;   "compute\_frontiers\_from\_envelope",

]





@dataclass(frozen=True)

class FrontierRow:

&#x20;   """Single row in a cost-vs-pass@1 Pareto non-dominance table."""



&#x20;   series\_id: str

&#x20;   cost\_axis: str

&#x20;   pass\_at\_1: Fraction

&#x20;   cost\_value\_nanos: Fraction | UndefinedValue

&#x20;   status: str  # "non\_dominated" | "dominated" | "undefined\_cost"

&#x20;   is\_on\_frontier: bool

&#x20;   tie\_group\_id: str | None

&#x20;   tied\_with: tuple\[str, ...]

&#x20;   dominated\_by: tuple\[str, ...]



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "series\_id": self.series\_id,

&#x20;           "cost\_axis": self.cost\_axis,

&#x20;           "pass\_at\_1": format\_fraction\_Or\_undef(self.pass\_at\_1),

&#x20;           "cost\_value\_nanos": format\_fraction\_Or\_undef(self.cost\_value\_nanos),

&#x20;           "status": self.status,

&#x20;           "is\_on\_frontier": self.is\_on\_frontier,

&#x20;           "tie\_group\_id": self.tie\_group\_id,

&#x20;           "tied\_with": list(self.tied\_with),

&#x20;           "dominated\_by": list(self.dominated\_by),

&#x20;       }





@dataclass(frozen=True)

class FrontierTable:

&#x20;   """Complete chart-ready Pareto frontier table for one explicit cost axis."""



&#x20;   cost\_axis: str

&#x20;   is\_headline\_axis: bool

&#x20;   objective\_rule: str

&#x20;   tie\_handling\_rule: str

&#x20;   undefined\_handling\_rule: str

&#x20;   frontier\_series\_ids: tuple\[str, ...]

&#x20;   dominated\_series\_ids: tuple\[str, ...]

&#x20;   undefined\_series\_ids: tuple\[str, ...]

&#x20;   rows: tuple\[FrontierRow, ...]



&#x20;   def to\_dict(self) -> dict\[str, Any]:

&#x20;       return {

&#x20;           "cost\_axis": self.cost\_axis,

&#x20;           "is\_headline\_axis": self.is\_headline\_axis,

&#x20;           "objective\_rule": self.objective\_rule,

&#x20;           "tie\_handling\_rule": self.tie\_handling\_rule,

&#x20;           "undefined\_handling\_rule": self.undefined\_handling\_rule,

&#x20;           "frontier\_series\_ids": list(self.frontier\_series\_ids),

&#x20;           "dominated\_series\_ids": list(self.dominated\_series\_ids),

&#x20;           "undefined\_series\_ids": list(self.undefined\_series\_ids),

&#x20;           "rows": \[r.to\_dict() for r in self.rows],

&#x20;       }





def \_extract\_point(item: SeriesPoint | ConfigMetrics) -> SeriesPoint:

&#x20;   if isinstance(item, ConfigMetrics):

&#x20;       return item.primary

&#x20;   if isinstance(item, SeriesPoint):

&#x20;       return item

&#x20;   raise TypeError(f"Expected SeriesPoint or ConfigMetrics, got {type(item).\_\_name\_\_}")





def \_extract\_cost(pt: SeriesPoint, cost\_axis: str) -> Fraction | UndefinedValue:

&#x20;   if cost\_axis == COST\_AXIS\_COST\_PER\_SOLVED:

&#x20;       return pt.expected\_cost\_per\_solved\_nanos

&#x20;   if cost\_axis == COST\_AXIS\_MEAN\_TASK\_COST:

&#x20;       return pt.mean\_task\_cost\_nanos

&#x20;   raise AnalysisInputError(

&#x20;       f"Unsupported cost\_axis {cost\_axis!r}; must be one of {sorted(VALID\_COST\_AXES)}"

&#x20;   )





def \_dominates(

&#x20;   cost\_a: Fraction,

&#x20;   pass\_a: Fraction,

&#x20;   cost\_b: Fraction,

&#x20;   pass\_b: Fraction,

) -> bool:

&#x20;   """Return True iff A Pareto-dominates B (cost minimized, pass@1 maximized)."""

&#x20;   return (cost\_a <= cost\_b and pass\_a >= pass\_b) and (cost\_a < cost\_b or pass\_a > pass\_b)





def compute\_frontier(

&#x20;   items: Sequence\[SeriesPoint | ConfigMetrics],

&#x20;   \*,

&#x20;   cost\_axis: str = COST\_AXIS\_COST\_PER\_SOLVED,

) -> FrontierTable:

&#x20;   """Compute exact rational Pareto frontier for `cost\_axis` vs `pass\_at\_1`."""

&#x20;   if cost\_axis not in VALID\_COST\_AXES:

&#x20;       raise AnalysisInputError(

&#x20;           f"Unsupported cost\_axis {cost\_axis!r}; must be one of {sorted(VALID\_COST\_AXES)}"

&#x20;       )



&#x20;   points = \[\_extract\_point(x) for x in items]

&#x20;   seen\_ids: set\[str] = set()

&#x20;   for pt in points:

&#x20;       if pt.series\_id in seen\_ids:

&#x20;           raise AnalysisInputError(f"Duplicate series\_id in frontier input: {pt.series\_id!r}")

&#x20;       seen\_ids.add(pt.series\_id)



&#x20;   defined\_pts: list\[tuple\[SeriesPoint, Fraction]] = \[]

&#x20;   undefined\_pts: list\[tuple\[SeriesPoint, UndefinedValue]] = \[]



&#x20;   for pt in points:

&#x20;       c\_val = \_extract\_cost(pt, cost\_axis)

&#x20;       if isinstance(c\_val, UndefinedValue):

&#x20;           undefined\_pts.append((pt, c\_val))

&#x20;       else:

&#x20;           defined\_pts.append((pt, c\_val))



&#x20;   # Sort defined points by (cost ascending, pass\_at\_1 descending, series\_id ascending)

&#x20;   defined\_pts.sort(key=lambda pair: (pair\[1], -pair\[0].pass\_at\_1, pair\[0].series\_id))

&#x20;   undefined\_pts.sort(key=lambda pair: pair\[0].series\_id)



&#x20;   # Assign deterministic tie\_group\_id to exact (cost, pass\_at\_1) coordinate pairs

&#x20;   coord\_groups: dict\[tuple\[Fraction, Fraction], list\[str]] = {}

&#x20;   for pt, c\_val in defined\_pts:

&#x20;       coord = (c\_val, pt.pass\_at\_1)

&#x20;       coord\_groups.setdefault(coord, \[]).append(pt.series\_id)



&#x20;   coord\_to\_group\_id: dict\[tuple\[Fraction, Fraction], str] = {}

&#x20;   for idx, coord in enumerate(coord\_groups, start=1):

&#x20;       coord\_to\_group\_id\[coord] = f"tie\_group\_{idx}"



&#x20;   defined\_rows: list\[FrontierRow] = \[]

&#x20;   frontier\_ids: list\[str] = \[]

&#x20;   dominated\_ids: list\[str] = \[]



&#x20;   for pt\_i, cost\_i in defined\_pts:

&#x20;       dominators: list\[str] = \[]

&#x20;       for pt\_j, cost\_j in defined\_pts:

&#x20;           if pt\_j.series\_id == pt\_i.series\_id:

&#x20;               continue

&#x20;           if \_dominates(cost\_j, pt\_j.pass\_at\_1, cost\_i, pt\_i.pass\_at\_1):

&#x20;               dominators.append(pt\_j.series\_id)



&#x20;       dominators.sort()

&#x20;       coord = (cost\_i, pt\_i.pass\_at\_1)

&#x20;       tied\_peers = tuple(s\_id for s\_id in coord\_groups\[coord] if s\_id != pt\_i.series\_id)

&#x20;       group\_id = coord\_to\_group\_id\[coord] if len(coord\_groups\[coord]) > 1 else None



&#x20;       if not dominators:

&#x20;           status = "non\_dominated"

&#x20;           is\_front = True

&#x20;           frontier\_ids.append(pt\_i.series\_id)

&#x20;       else:

&#x20;           status = "dominated"

&#x20;           is\_front = False

&#x20;           dominated\_ids.append(pt\_i.series\_id)



&#x20;       defined\_rows.append(

&#x20;           FrontierRow(

&#x20;               series\_id=pt\_i.series\_id,

&#x20;               cost\_axis=cost\_axis,

&#x20;               pass\_at\_1=pt\_i.pass\_at\_1,

&#x20;               cost\_value\_nanos=cost\_i,

&#x20;               status=status,

&#x20;               is\_on\_frontier=is\_front,

&#x20;               tie\_group\_id=group\_id,

&#x20;               tied\_with=tied\_peers,

&#x20;               dominated\_by=tuple(dominators),

&#x20;           )

&#x20;       )



&#x20;   undefined\_rows: list\[FrontierRow] = \[]

&#x20;   undefined\_ids: list\[str] = \[]

&#x20;   for pt\_u, undef\_val in undefined\_pts:

&#x20;       undefined\_ids.append(pt\_u.series\_id)

&#x20;       undefined\_rows.append(

&#x20;           FrontierRow(

&#x20;               series\_id=pt\_u.series\_id,

&#x20;               cost\_axis=cost\_axis,

&#x20;               pass\_at\_1=pt\_u.pass\_at\_1,

&#x20;               cost\_value\_nanos=undef\_val,

&#x20;               status="undefined\_cost",

&#x20;               is\_on\_frontier=False,

&#x20;               tie\_group\_id=None,

&#x20;               tied\_with=(),

&#x20;               dominated\_by=(),

&#x20;           )

&#x20;       )



&#x20;   all\_rows = tuple(defined\_rows + undefined\_rows)

&#x20;   return FrontierTable(

&#x20;       cost\_axis=cost\_axis,

&#x20;       is\_headline\_axis=(cost\_axis == COST\_AXIS\_COST\_PER\_SOLVED),

&#x20;       objective\_rule="Minimize exact rational cost\_value\_nanos; maximize exact rational pass\_at\_1.",

&#x20;       tie\_handling\_rule=(

&#x20;           "Retain all tied non-dominated series on the frontier and link identical "

&#x20;           "(cost, pass\_at\_1) coordinates via deterministic tie\_group\_id and tied\_with lists."

&#x20;       ),

&#x20;       undefined\_handling\_rule=(

&#x20;           "Points with undefined cost (e.g., zero\_expected\_solves on cost\_per\_solved or "

&#x20;           "missing\_cost\_nano\_usd) are labeled status='undefined\_cost', excluded from the "

&#x20;           "valid frontier, and never dominate or get dominated by valid points."

&#x20;       ),

&#x20;       frontier\_series\_ids=tuple(frontier\_ids),

&#x20;       dominated\_series\_ids=tuple(dominated\_ids),

&#x20;       undefined\_series\_ids=tuple(undefined\_ids),

&#x20;       rows=all\_rows,

&#x20;   )





def compute\_both\_frontiers(

&#x20;   items: Sequence\[SeriesPoint | ConfigMetrics],

) -> dict\[str, FrontierTable]:

&#x20;   """Compute both headline (`cost\_per\_solved`) and diagnostic (`mean\_task\_cost`) frontiers."""

&#x20;   return {

&#x20;       COST\_AXIS\_COST\_PER\_SOLVED: compute\_frontier(

&#x20;           items, cost\_axis=COST\_AXIS\_COST\_PER\_SOLVED

&#x20;       ),

&#x20;       COST\_AXIS\_MEAN\_TASK\_COST: compute\_frontier(

&#x20;           items, cost\_axis=COST\_AXIS\_MEAN\_TASK\_COST

&#x20;       ),

&#x20;   }





def compute\_frontiers\_from\_envelope(

&#x20;   envelope: NormalizedEnvelope,

) -> dict\[str, FrontierTable]:

&#x20;   """Validate cost completeness on `envelope` and compute both frontier tables."""

&#x20;   if not envelope.audit.cost\_comparison\_allowed:

&#x20;       raise AnalysisInputError(

&#x20;           f"Cannot compute cost frontiers when panel audit status is {envelope.audit.status!r}"

&#x20;       )

&#x20;   metrics\_map = compute\_all\_config\_metrics(envelope)

&#x20;   return compute\_both\_frontiers(list(metrics\_map.values()))



```



\---



\## FILE: tests/fixtures/analysis/valid\_panel.json



```json

{

&#x20; "schema\_version": 1,

&#x20; "evidence\_kind": "synthetic",

&#x20; "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20; "expected\_plan": {

&#x20;   "tasks": \[

&#x20;     "synthetic\_stats\_1",

&#x20;     "synthetic\_stats\_2",

&#x20;     "synthetic\_stats\_3",

&#x20;     "synthetic\_stats\_4"

&#x20;   ],

&#x20;   "seeds\_by\_config": {

&#x20;     "A": \[

&#x20;       0

&#x20;     ],

&#x20;     "B": \[

&#x20;       0

&#x20;     ]

&#x20;   }

&#x20; },

&#x20; "records": \[

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_1",

&#x20;     "config\_id": "A",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_1",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "solved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "passed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 1000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": true,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_1",

&#x20;     "config\_id": "B",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_1",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "solved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "passed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 10000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": null,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_2",

&#x20;     "config\_id": "A",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_2",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "unsolved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "failed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 2000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": false,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_2",

&#x20;     "config\_id": "B",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_2",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "solved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "passed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 10000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": null,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_3",

&#x20;     "config\_id": "A",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_3",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "unsolved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "failed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 1000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": null,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_3",

&#x20;     "config\_id": "B",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_3",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "unsolved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "failed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 10000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": null,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_4",

&#x20;     "config\_id": "A",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_4",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "solved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "passed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 2000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": true,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_4",

&#x20;     "config\_id": "B",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_4",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "unsolved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "failed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 10000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": null,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   }

&#x20; ]

}



```



\---



\## FILE: tests/fixtures/analysis/unequal\_seed\_panel.json



```json

{

&#x20; "schema\_version": 1,

&#x20; "evidence\_kind": "synthetic",

&#x20; "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20; "expected\_plan": {

&#x20;   "tasks": \[

&#x20;     "synthetic\_unequal\_1"

&#x20;   ],

&#x20;   "seeds\_by\_config": {

&#x20;     "A": \[

&#x20;       0,

&#x20;       1

&#x20;     ],

&#x20;     "B": \[

&#x20;       0

&#x20;     ]

&#x20;   }

&#x20; },

&#x20; "records": \[

&#x20;   {

&#x20;     "task\_id": "synthetic\_unequal\_1",

&#x20;     "config\_id": "A",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_1",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "solved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "passed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 2,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": true,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_unequal\_1",

&#x20;     "config\_id": "A",

&#x20;     "seed": 1,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_1",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "unsolved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "failed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 4,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": false,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_unequal\_1",

&#x20;     "config\_id": "B",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_1",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "unsolved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "failed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 10,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": null,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   }

&#x20; ]

}



```



\---



\## FILE: tests/fixtures/analysis/invalid\_panel.json



```json

{

&#x20; "schema\_version": 1,

&#x20; "evidence\_kind": "synthetic",

&#x20; "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20; "expected\_plan": {

&#x20;   "tasks": \[

&#x20;     "synthetic\_stats\_1",

&#x20;     "synthetic\_stats\_2",

&#x20;     "synthetic\_stats\_3",

&#x20;     "synthetic\_stats\_4"

&#x20;   ],

&#x20;   "seeds\_by\_config": {

&#x20;     "A": \[

&#x20;       0

&#x20;     ],

&#x20;     "B": \[

&#x20;       0

&#x20;     ]

&#x20;   }

&#x20; },

&#x20; "records": \[

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_1",

&#x20;     "config\_id": "A",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_1",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "solved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "passed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 1000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": true,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_1",

&#x20;     "config\_id": "B",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_1",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "solved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "passed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 10000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": null,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_2",

&#x20;     "config\_id": "A",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_2",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "unsolved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "failed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 2000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": false,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_2",

&#x20;     "config\_id": "B",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_2",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "solved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "passed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 10000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": null,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_3",

&#x20;     "config\_id": "A",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_3",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "unsolved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "failed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 1000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": null,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_3",

&#x20;     "config\_id": "B",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_3",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "unsolved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "failed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 10000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": null,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_4",

&#x20;     "config\_id": "A",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_4",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "solved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "passed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 2000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": true,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "task\_id": "synthetic\_stats\_1",

&#x20;     "config\_id": "A",

&#x20;     "seed": 0,

&#x20;     "split": "train",

&#x20;     "family\_id": "synthetic\_family\_1",

&#x20;     "dataset\_id": "synthetic\_stats\_fixture\_v1",

&#x20;     "evidence\_kind": "synthetic",

&#x20;     "registration\_id": null,

&#x20;     "execution\_complete": true,

&#x20;     "outcome": "solved",

&#x20;     "evidence\_validity": "valid",

&#x20;     "scorer\_status": "passed",

&#x20;     "baseline\_verified": false,

&#x20;     "cost\_nano\_usd": 1000000,

&#x20;     "signals": {

&#x20;       "has\_patch": true,

&#x20;       "visible\_tests\_pass": true,

&#x20;       "hit\_step\_cap": false,

&#x20;       "no\_command\_rate": 0.0,

&#x20;       "agent\_self\_reports\_done": true

&#x20;     }

&#x20;   }

&#x20; ]

}



```



\---



\## FILE: tests/test\_analysis\_records.py



```python

"""WP1 tests: normalized records, expected plan, bounded JSON parser, and panel audit."""



from \_\_future\_\_ import annotations



import copy

import json

from fractions import Fraction

from pathlib import Path



import pytest



from dojo.bench.records import (

&#x20;   MAX\_INPUT\_BYTES,

&#x20;   MAX\_JSON\_DEPTH,

&#x20;   AnalysisInputError,

&#x20;   parse\_analysis\_envelope,

&#x20;   parse\_analysis\_json,

)



FIXTURES\_DIR = Path(\_\_file\_\_).resolve().parent / "fixtures" / "analysis"





def \_load\_fixture\_dict(name: str) -> dict:

&#x20;   return json.loads((FIXTURES\_DIR / name).read\_text(encoding="utf-8"))





def test\_valid\_panel\_fixture\_parses\_and\_passes\_audit() -> None:

&#x20;   raw = (FIXTURES\_DIR / "valid\_panel.json").read\_bytes()

&#x20;   env = parse\_analysis\_json(raw)



&#x20;   assert env.schema\_version == 1

&#x20;   assert env.dataset\_id == "synthetic\_stats\_fixture\_v1"

&#x20;   assert env.evidence\_kind == "synthetic"

&#x20;   assert env.eligibility\_status.status == "UNVERIFIED"

&#x20;   assert env.eligibility\_status.publishable is False

&#x20;   assert env.audit.status == "valid"

&#x20;   assert env.audit.headline\_Comparison\_allowed is True

&#x20;   assert env.audit.cost\_comparison\_allowed is True

&#x20;   assert env.audit.expected\_cell\_count == 8

&#x20;   assert env.audit.valid\_cell\_count == 8

&#x20;   assert env.audit.findings == ()





def test\_invalid\_panel\_fixture\_reports\_missing\_and\_duplicate\_cells() -> None:

&#x20;   raw = (FIXTURES\_DIR / "invalid\_panel.json").read\_bytes()

&#x20;   env = parse\_analysis\_json(raw)



&#x20;   assert env.audit.status == "blocked"

&#x20;   assert env.audit.headline\_Comparison\_allowed is False

&#x20;   assert env.audit.cost\_comparison\_allowed is False

&#x20;   messages = \[f.message for f in env.audit.findings]

&#x20;   assert any("missing B/synthetic\_stats\_4/seed0" in m for m in messages)

&#x20;   assert any("duplicate A/synthetic\_stats\_1/seed0" in m for m in messages)





def test\_record\_order\_invariance\_and\_expected\_plan\_order\_sensitivity() -> None:

&#x20;   data1 = \_load\_fixture\_dict("valid\_panel.json")

&#x20;   data2 = copy.deepcopy(data1)

&#x20;   data2\["records"] = list(reversed(data2\["records"]))



&#x20;   env1 = parse\_analysis\_envelope(data1)

&#x20;   env2 = parse\_analysis\_envelope(data2)

&#x20;   assert env1.input\_sha256 == env2.input\_sha256

&#x20;   assert env1.expected\_plan\_hash == env2.expected\_plan\_hash



&#x20;   # Changing declared task order in expected\_plan MUST change expected\_plan\_hash

&#x20;   data3 = copy.deepcopy(data1)

&#x20;   data3\["expected\_plan"]\["tasks"] = list(reversed(data3\["expected\_plan"]\["tasks"]))

&#x20;   env3 = parse\_analysis\_envelope(data3)

&#x20;   assert env3.expected\_plan\_hash != env1.expected\_plan\_hash





def test\_rejects\_test\_harness\_expected\_annotation\_in\_envelope() -> None:

&#x20;   data = \_load\_fixture\_dict("valid\_panel.json")

&#x20;   data\["expected"] = {"a\_pass\_rate": "1/2"}

&#x20;   with pytest.raises(AnalysisInputError, match="expected"):

&#x20;       parse\_analysis\_envelope(data)





def test\_rejects\_duplicate\_json\_keys\_and\_nonfinite\_numbers() -> None:

&#x20;   dup\_json = (

&#x20;       '{"schema\_version": 1, "schema\_version": 1, "evidence\_kind": "synthetic", '

&#x20;       '"dataset\_id": "d1", "expected\_plan": {"tasks": \["t1"], "seeds\_by\_config": {"A": \[0]}}, '

&#x20;       '"records": \[]}'

&#x20;   )

&#x20;   with pytest.raises(AnalysisInputError, match="Duplicate JSON key"):

&#x20;       parse\_analysis\_json(dup\_json)



&#x20;   nan\_json = dup\_json.replace('"schema\_version": 1, "schema\_version": 1', '"schema\_version": NaN')

&#x20;   with pytest.raises(AnalysisInputError, match="Non-finite"):

&#x20;       parse\_analysis\_json(nan\_json)





def test\_rejects\_lone\_surrogates\_and\_extreme\_exponents() -> None:

&#x20;   data = \_load\_fixture\_dict("valid\_panel.json")

&#x20;   raw\_text = json.dumps(data)



&#x20;   surrogate\_json = raw\_text.replace("synthetic\_stats\_1", "bad\\\\ud800id")

&#x20;   with pytest.raises(AnalysisInputError, match="surrogate"):

&#x20;       parse\_analysis\_json(surrogate\_json)



&#x20;   huge\_exp\_json = raw\_text.replace("1000000", "1e9999")

&#x20;   with pytest.raises(AnalysisInputError, match="exponent"):

&#x20;       parse\_analysis\_json(huge\_exp\_json)





def test\_rejects\_oversized\_input\_and\_excessive\_nesting\_depth() -> None:

&#x20;   oversized = b" " \* (MAX\_INPUT\_BYTES + 1)

&#x20;   with pytest.raises(AnalysisInputError, match="exceeds limit"):

&#x20;       parse\_analysis\_json(oversized)



&#x20;   nested: dict = {"a": 1}

&#x20;   for \_ in range(MAX\_JSON\_DEPTH + 2):

&#x20;       nested = {"nested": nested}

&#x20;   with pytest.raises(AnalysisInputError, match="depth"):

&#x20;       parse\_analysis\_json(json.dumps(nested))





def test\_rejects\_bool\_as\_seed\_money\_or\_count() -> None:

&#x20;   data = \_load\_fixture\_dict("valid\_panel.json")

&#x20;   bad\_seed = copy.deepcopy(data)

&#x20;   bad\_seed\["records"]\[0]\["seed"] = False

&#x20;   with pytest.raises(AnalysisInputError, match="seed"):

&#x20;       parse\_analysis\_envelope(bad\_seed)



&#x20;   bad\_cost = copy.deepcopy(data)

&#x20;   bad\_cost\["records"]\[0]\["cost\_nano\_usd"] = True

&#x20;   with pytest.raises(AnalysisInputError, match="cost\_nano\_usd"):

&#x20;       parse\_analysis\_envelope(bad\_cost)



&#x20;   bad\_turns = copy.deepcopy(data)

&#x20;   bad\_turns\["records"]\[0]\["turns"] = True

&#x20;   with pytest.raises(AnalysisInputError, match="turns"):

&#x20;       parse\_analysis\_envelope(bad\_turns)





def test\_candidate\_error\_baseline\_verified\_rule() -> None:

&#x20;   data = \_load\_fixture\_dict("valid\_panel.json")

&#x20;   # Record 2 is A/synthetic\_stats\_2/seed0 (unsolved)

&#x20;   data\["records"]\[2]\["scorer\_status"] = "candidate\_error"

&#x20;   data\["records"]\[2]\["baseline\_verified"] = False



&#x20;   env\_blocked = parse\_analysis\_envelope(data)

&#x20;   assert env\_blocked.audit.status == "blocked"

&#x20;   assert any(

&#x20;       f.code == "unverified\_candidate\_error\_baseline" for f in env\_blocked.audit.findings

&#x20;   )



&#x20;   # When baseline\_verified is True, candidate\_error is a valid unsolved outcome

&#x20;   data\["records"]\[2]\["baseline\_verified"] = True

&#x20;   env\_valid = parse\_analysis\_envelope(data)

&#x20;   assert env\_valid.audit.status == "valid"

&#x20;   assert env\_valid.audit.headline\_Comparison\_allowed is True





def test\_invalid\_evidence\_and\_infrastructure\_error\_block\_headline() -> None:

&#x20;   data = \_load\_fixture\_dict("valid\_panel.json")

&#x20;   data\["records"]\[2]\["scorer\_status"] = "invalid\_evidence"

&#x20;   data\["records"]\[2]\["outcome"] = "undetermined"

&#x20;   data\["records"]\[2]\["evidence\_validity"] = "invalid"



&#x20;   env = parse\_analysis\_envelope(data)

&#x20;   assert env.audit.status == "blocked"

&#x20;   assert env.audit.headline\_Comparison\_allowed is False

&#x20;   assert any(f.code == "invalid\_evidence\_cell" for f in env.audit.findings)



&#x20;   data\_infra = \_load\_fixture\_dict("valid\_panel.json")

&#x20;   data\_infra\["records"]\[2]\["scorer\_status"] = "infrastructure\_error"

&#x20;   data\_infra\["records"]\[2]\["outcome"] = "undetermined"

&#x20;   data\_infra\["records"]\[2]\["evidence\_validity"] = "unknown"



&#x20;   env\_infra = parse\_analysis\_envelope(data\_infra)

&#x20;   assert env\_infra.audit.status == "blocked"

&#x20;   assert any(f.code == "infrastructure\_error\_cell" for f in env\_infra.audit.findings)





def test\_missing\_cost\_allows\_success\_only\_but\_blocks\_cost\_comparisons() -> None:

&#x20;   data = \_load\_fixture\_dict("valid\_panel.json")

&#x20;   data\["records"]\[0]\["cost\_nano\_usd"] = None



&#x20;   env = parse\_analysis\_envelope(data)

&#x20;   assert env.audit.status == "cost\_incomplete"

&#x20;   assert env.audit.headline\_Comparison\_allowed is False

&#x20;   assert env.audit.cost\_comparison\_allowed is False

&#x20;   assert env.audit.success\_only\_allowed is True

&#x20;   assert env.audit.missing\_cost\_configs == ("A",)





def test\_optional\_secondary\_fields\_accepted\_and\_unknown\_fields\_rejected() -> None:

&#x20;   data = \_load\_fixture\_dict("valid\_panel.json")

&#x20;   for r in data\["records"]:

&#x20;       r\["turns"] = 5

&#x20;       r\["commands"] = 4

&#x20;       r\["actual\_prompt\_tokens"] = 1200

&#x20;       r\["actual\_completion\_tokens"] = 300

&#x20;       r\["wall\_seconds"] = 12.5



&#x20;   env = parse\_analysis\_envelope(data)

&#x20;   assert env.records\[0].turns == 5

&#x20;   assert env.records\[0].wall\_seconds == Fraction(25, 2)



&#x20;   data\["records"]\[0]\["secret\_unknown\_field"] = 123

&#x20;   with pytest.raises(AnalysisInputError, match="field mismatch"):

&#x20;       parse\_analysis\_envelope(data)





def test\_nonempty\_registration\_id\_never\_grants\_publishable\_eligibility() -> None:

&#x20;   data = \_load\_fixture\_dict("valid\_panel.json")

&#x20;   for r in data\["records"]:

&#x20;       r\["registration\_id"] = "stage\_b\_fake\_registration\_digest"

&#x20;   env = parse\_analysis\_envelope(data)

&#x20;   assert env.eligibility\_status.status == "UNVERIFIED"

&#x20;   assert env.eligibility\_status.publishable is False



```



\---



\## FILE: tests/test\_statistics.py



```python

"""WP2, WP3, WP4, WP5 tests: known answers, bootstrap pairing, sensitivity, and frontiers."""



from \_\_future\_\_ import annotations



import copy

import json

import random

from fractions import Fraction

from pathlib import Path



import pytest



from dojo.bench.frontier import (

&#x20;   COST\_AXIS\_COST\_PER\_SOLVED,

&#x20;   COST\_AXIS\_MEAN\_TASK\_COST,

&#x20;   compute\_both\_frontiers,

&#x20;   compute\_frontier,

&#x20;   compute\_frontiers\_from\_envelope,

)

from dojo.bench.records import (

&#x20;   AnalysisInputError,

&#x20;   UndefinedValue,

&#x20;   parse\_analysis\_envelope,

&#x20;   parse\_analysis\_json,

)

from dojo.bench.stats import (

&#x20;   MAX\_BOOTSTRAP\_WORKLOAD,

&#x20;   SeriesPoint,

&#x20;   TaskPoint,

&#x20;   TaskSeries,

&#x20;   build\_config\_task\_series,

&#x20;   compute\_all\_config\_metrics,

&#x20;   compute\_config\_metrics,

&#x20;   evaluate\_series\_point,

&#x20;   family\_cluster\_bootstrap,

&#x20;   paired\_task\_bootstrap,

&#x20;   seed\_sensitivity\_analysis,

)



FIXTURES\_DIR = Path(\_\_file\_\_).resolve().parent / "fixtures" / "analysis"





def test\_wp2\_known\_answers\_on\_valid\_panel\_fixture() -> None:

&#x20;   env = parse\_analysis\_json((FIXTURES\_DIR / "valid\_panel.json").read\_bytes())

&#x20;   metrics = compute\_all\_config\_metrics(env)



&#x20;   m\_a = metrics\["A"]

&#x20;   assert m\_a.n\_tasks == 4

&#x20;   assert m\_a.declared\_seeds == (0,)

&#x20;   assert m\_a.primary.pass\_at\_1 == Fraction(1, 2)

&#x20;   assert m\_a.primary.expected\_solved\_tasks == Fraction(2, 1)

&#x20;   assert m\_a.primary.expected\_total\_cost\_nanos == Fraction(6\_000\_000, 1)

&#x20;   assert m\_a.primary.mean\_task\_cost\_nanos == Fraction(1\_500\_000, 1)

&#x20;   assert m\_a.primary.expected\_cost\_per\_solved\_nanos == Fraction(3\_000\_000, 1)

&#x20;   assert m\_a.primary.actual\_all\_repetitions\_spend\_nanos == 6\_000\_000



&#x20;   # Optional secondary metrics default to UndefinedValue when absent, never 0

&#x20;   assert isinstance(m\_a.secondary\_metrics\["turns"].task\_weighted\_mean, UndefinedValue)

&#x20;   assert m\_a.secondary\_metrics\["turns"].known\_runs == 0

&#x20;   assert m\_a.secondary\_metrics\["turns"].missing\_runs == 4



&#x20;   m\_b = metrics\["B"]

&#x20;   assert m\_b.primary.pass\_at\_1 == Fraction(1, 2)

&#x20;   assert m\_b.primary.expected\_total\_cost\_nanos == Fraction(40\_000\_000, 1)

&#x20;   assert m\_b.primary.expected\_cost\_per\_solved\_nanos == Fraction(20\_000\_000, 1)

&#x20;   assert m\_b.primary.actual\_all\_repetitions\_spend\_nanos == 40\_000\_000





def test\_wp2\_unequal\_seed\_fixture\_and\_zero\_solve\_undefined\_denominator() -> None:

&#x20;   env = parse\_analysis\_json((FIXTURES\_DIR / "unequal\_seed\_panel.json").read\_bytes())

&#x20;   metrics = compute\_all\_config\_metrics(env)



&#x20;   # Config A has 2 seeds on 1 task: seed 0 solved (cost 2), seed 1 unsolved (cost 4)

&#x20;   # Expected 1-seed total cost = (2 + 4)/2 = 3; actual all-repeat spend = 6

&#x20;   m\_a = metrics\["A"]

&#x20;   assert m\_a.declared\_seeds == (0, 1)

&#x20;   assert m\_a.primary.pass\_at\_1 == Fraction(1, 2)

&#x20;   assert m\_a.primary.expected\_total\_cost\_nanos == Fraction(3, 1)

&#x20;   assert m\_a.primary.actual\_all\_repetitions\_spend\_nanos == 6

&#x20;   assert m\_a.primary.expected\_cost\_per\_solved\_nanos == Fraction(6, 1)



&#x20;   # Config B has 1 seed on 1 task: seed 0 unsolved (cost 10) -> zero expected solves

&#x20;   m\_b = metrics\["B"]

&#x20;   assert m\_b.primary.pass\_at\_1 == Fraction(0, 1)

&#x20;   assert m\_b.primary.expected\_total\_cost\_nanos == Fraction(10, 1)

&#x20;   assert m\_b.primary.actual\_all\_repetitions\_spend\_nanos == 10

&#x20;   assert isinstance(m\_b.primary.expected\_cost\_per\_solved\_nanos, UndefinedValue)

&#x20;   assert m\_b.primary.expected\_cost\_per\_solved\_nanos.reason == "zero\_expected\_solves"

&#x20;   assert m\_b.primary.to\_dict()\["expected\_cost\_per\_solved\_nanos"]\["value"] is None





def test\_wp3\_paired\_bootstrap\_injectable\_indices\_and\_zero\_solve\_accounting() -> None:

&#x20;   env = parse\_analysis\_json((FIXTURES\_DIR / "valid\_panel.json").read\_bytes())

&#x20;   series\_a = build\_config\_task\_series(env, "A")

&#x20;   series\_b = build\_config\_task\_series(env, "B")



&#x20;   # Task outcomes (0-indexed):

&#x20;   # task 0: A=1 (cost 1M), B=1 (cost 10M)

&#x20;   # task 1: A=0 (cost 2M), B=1 (cost 10M)

&#x20;   # task 2: A=0 (cost 1M), B=0 (cost 10M)

&#x20;   # task 3: A=1 (cost 2M), B=0 (cost 10M)

&#x20;   injected\_draws = \[

&#x20;       (0, 0, 0, 0),  # Both A and B solve 4/4 -> delta pass@1 = 0

&#x20;       (1, 1, 1, 1),  # A solves 0/4 (zero solve!), B solves 4/4 -> delta pass@1 = +1

&#x20;       (2, 2, 2, 2),  # Both A and B solve 0/4 (zero solve!) -> delta pass@1 = 0

&#x20;       (0, 1, 2, 3),  # Original panel -> A=1/2, B=1/2 -> delta pass@1 = 0

&#x20;   ]



&#x20;   res = paired\_task\_bootstrap(

&#x20;       \[series\_a, series\_b],

&#x20;       sampled\_task\_indices=injected\_draws,

&#x20;       confidence\_level=Fraction(95, 100),

&#x20;   )



&#x20;   sum\_a = res.series\_summaries\["A"]

&#x20;   assert sum\_a.expected\_cost\_per\_solved\_nanos.zero\_solve\_draws == 2

&#x20;   assert sum\_a.expected\_cost\_per\_solved\_nanos.defined\_draws == 2

&#x20;   assert sum\_a.expected\_cost\_per\_solved\_nanos.undefined\_draws == 2

&#x20;   # Because zero-solve draws occurred, unconditional CI for cost/solve must be blocked (UndefinedValue)

&#x20;   assert isinstance(sum\_a.expected\_cost\_per\_solved\_nanos.lower, UndefinedValue)

&#x20;   assert (

&#x20;       sum\_a.expected\_cost\_per\_solved\_nanos.lower.reason

&#x20;       == "unconditional\_interval\_blocked\_by\_zero\_solve\_draws"

&#x20;   )



&#x20;   diff\_ab = res.paired\_differences\[0]

&#x20;   assert diff\_ab.baseline\_id == "A"

&#x20;   assert diff\_ab.target\_id == "B"

&#x20;   assert diff\_ab.delta\_pass\_at\_1.point\_estimate == Fraction(0, 1)

&#x20;   assert diff\_ab.delta\_expected\_total\_cost\_nanos.point\_estimate == Fraction(34\_000\_000, 1)





def test\_wp3\_pairing\_cancels\_variance\_for\_identical\_series\_and\_isolates\_global\_rng() -> None:

&#x20;   env = parse\_analysis\_json((FIXTURES\_DIR / "valid\_panel.json").read\_bytes())

&#x20;   series\_a1 = build\_config\_task\_series(env, "A", series\_id="A\_copy\_1")

&#x20;   series\_a2 = build\_config\_task\_series(env, "A", series\_id="A\_copy\_2")



&#x20;   random.seed(99999)

&#x20;   expected\_next\_random = random.random()

&#x20;   random.seed(99999)



&#x20;   res = paired\_task\_bootstrap(\[series\_a1, series\_a2], replicates=200, seed=42)

&#x20;   # Global random state must be completely untouched by paired\_task\_bootstrap

&#x20;   assert random.random() == expected\_next\_random



&#x20;   # Because both series share the exact same sampled task indices on every draw,

&#x20;   # their paired difference on every draw is identically 0!

&#x20;   diff = res.paired\_differences\[0]

&#x20;   assert diff.delta\_pass\_at\_1.lower == Fraction(0, 1)

&#x20;   assert diff.delta\_pass\_at\_1.upper == Fraction(0, 1)

&#x20;   assert diff.delta\_expected\_total\_cost\_nanos.lower == Fraction(0, 1)

&#x20;   assert diff.delta\_expected\_total\_cost\_nanos.upper == Fraction(0, 1)





def test\_wp3\_bootstrap\_workload\_cap\_rejects\_oversized\_requests() -> None:

&#x20;   env = parse\_analysis\_json((FIXTURES\_DIR / "valid\_panel.json").read\_bytes())

&#x20;   # Create enough synthetic series so replicates \* n\_tasks \* n\_series > 10,000,000

&#x20;   many\_series = \[

&#x20;       build\_config\_task\_series(env, "A", series\_id=f"S\_{i}") for i in range(30)

&#x20;   ]

&#x20;   with pytest.raises(AnalysisInputError, match="workload"):

&#x20;       paired\_task\_bootstrap(many\_series, replicates=100\_000)





def test\_wp4\_family\_cluster\_bootstrap\_unbalanced\_clusters\_preserve\_original\_n\_cost() -> None:

&#x20;   # Build an unbalanced 3-task, 2-family series:

&#x20;   # fam\_small (1 task): pass=1, mean\_cost=100

&#x20;   # fam\_large (2 tasks): pass=0, mean\_cost=400 each

&#x20;   # Original n = 3 tasks.

&#x20;   tasks = (

&#x20;       TaskPoint("t1", "fam\_small", 1, Fraction(1, 1), Fraction(100, 1), 100),

&#x20;       TaskPoint("t2", "fam\_large", 1, Fraction(0, 1), Fraction(400, 1), 400),

&#x20;       TaskPoint("t3", "fam\_large", 1, Fraction(0, 1), Fraction(400, 1), 400),

&#x20;   )

&#x20;   series = TaskSeries("A", "config", tasks, declared\_seed\_count=1, has\_complete\_costs=True)



&#x20;   # Inject family draws (0 = fam\_small, 1 = fam\_large):

&#x20;   # Draw 0: (0, 0) -> 2 tasks total, all cost 100 -> mean\_task\_cost = 100, target\_n\_total\_cost = 3 \* 100 = 300

&#x20;   # Draw 1: (1, 1) -> 4 tasks total, all cost 400 -> mean\_task\_cost = 400, target\_n\_total\_cost = 3 \* 400 = 1200

&#x20;   fam\_res = family\_cluster\_bootstrap(

&#x20;       \[series],

&#x20;       sampled\_family\_indices=\[(0, 0), (1, 1)],

&#x20;   )



&#x20;   assert fam\_res.is\_primary is False

&#x20;   assert fam\_res.original\_n\_tasks == 3

&#x20;   assert fam\_res.n\_families == 2

&#x20;   assert fam\_res.min\_resampled\_tasks == 2

&#x20;   assert fam\_res.max\_resampled\_tasks == 4

&#x20;   assert fam\_res.mean\_resampled\_tasks == Fraction(3, 1)



&#x20;   s\_sum = fam\_res.series\_summaries\["A"]

&#x20;   assert s\_sum.target\_n\_expected\_total\_cost\_nanos.lower == Fraction(300, 1)

&#x20;   assert s\_sum.target\_n\_expected\_total\_cost\_nanos.upper == Fraction(1200, 1)





def test\_wp4\_seed\_sensitivity\_on\_asymmetric\_seeds() -> None:

&#x20;   env = parse\_analysis\_json((FIXTURES\_DIR / "unequal\_seed\_panel.json").read\_bytes())

&#x20;   sens = seed\_sensitivity\_analysis(

&#x20;       env,

&#x20;       seed\_subsets\_by\_config={"A": \[(0,), (1,), (0, 1)]},

&#x20;   )



&#x20;   assert sens.is\_primary is False

&#x20;   assert sens.common\_seed\_positions == (0,)

&#x20;   assert sens.shared\_exact\_seeds == (0,)



&#x20;   by\_label = {(e.config\_id, e.slice\_label): e for e in sens.entries}

&#x20;   assert by\_label\[("A", "position\_0\_seed\_0")].point.pass\_at\_1 == Fraction(1, 1)

&#x20;   assert by\_label\[("A", "position\_1\_seed\_1")].point.pass\_at\_1 == Fraction(0, 1)

&#x20;   assert by\_label\[("A", "all\_declared\_seeds")].point.pass\_at\_1 == Fraction(1, 2)





def test\_wp5\_frontiers\_dominated\_tied\_and\_undefined\_zero\_solve\_points() -> None:

&#x20;   # Hand-calculated points:

&#x20;   # C\_fast\_good: pass=3/4, mean\_cost=100, expected\_total=400 (n=4), cost/solve = 400/3 = 133.33

&#x20;   # C\_tied:      pass=3/4, mean\_cost=100, expected\_total=400 (n=4), cost/solve = 400/3

&#x20;   # C\_cheap\_low: pass=1/4, mean\_cost=50,  expected\_total=200 (n=4), cost/solve = 200/1 = 200

&#x20;   #   -> Notice: On mean\_task\_cost (50 < 100), C\_cheap\_low is NON-DOMINATED!

&#x20;   #   -> On cost\_per\_solved (200 > 400/3 and pass 1/4 < 3/4), C\_cheap\_low IS DOMINATED by C\_fast\_good!

&#x20;   # C\_zero\_solve: pass=0, mean\_cost=10, expected\_total=40, cost/solve = UndefinedValue("zero\_expected\_solves")

&#x20;   #   -> On cost\_per\_solved, C\_zero\_solve is status="undefined\_cost" and CANNOT dominate anything.

&#x20;   #   -> On mean\_task\_cost, C\_zero\_solve has defined cost=10 (lowest cost!) so it is non-dominated on mean\_task\_cost.



&#x20;   p\_fast = SeriesPoint(

&#x20;       series\_id="C\_fast\_good",

&#x20;       n\_tasks=4,

&#x20;       pass\_at\_1=Fraction(3, 4),

&#x20;       expected\_solved\_tasks=Fraction(3, 1),

&#x20;       expected\_total\_cost\_nanos=Fraction(400, 1),

&#x20;       mean\_task\_cost\_nanos=Fraction(100, 1),

&#x20;       expected\_cost\_per\_solved\_nanos=Fraction(400, 3),

&#x20;       actual\_all\_repetitions\_spend\_nanos=400,

&#x20;   )

&#x20;   p\_tied = SeriesPoint(

&#x20;       series\_id="C\_tied",

&#x20;       n\_tasks=4,

&#x20;       pass\_at\_1=Fraction(3, 4),

&#x20;       expected\_solved\_tasks=Fraction(3, 1),

&#x20;       expected\_total\_cost\_nanos=Fraction(400, 1),

&#x20;       mean\_task\_cost\_nanos=Fraction(100, 1),

&#x20;       expected\_cost\_per\_solved\_nanos=Fraction(400, 3),

&#x20;       actual\_all\_repetitions\_spend\_nanos=400,

&#x20;   )

&#x20;   p\_cheap = SeriesPoint(

&#x20;       series\_id="C\_cheap\_low",

&#x20;       n\_tasks=4,

&#x20;       pass\_at\_1=Fraction(1, 4),

&#x20;       expected\_solved\_tasks=Fraction(1, 1),

&#x20;       expected\_total\_cost\_nanos=Fraction(200, 1),

&#x20;       mean\_task\_cost\_nanos=Fraction(50, 1),

&#x20;       expected\_cost\_per\_solved\_nanos=Fraction(200, 1),

&#x20;       actual\_all\_repetitions\_spend\_nanos=200,

&#x20;   )

&#x20;   p\_zero = SeriesPoint(

&#x20;       series\_id="C\_zero\_solve",

&#x20;       n\_tasks=4,

&#x20;       pass\_at\_1=Fraction(0, 1),

&#x20;       expected\_solved\_tasks=Fraction(0, 1),

&#x20;       expected\_total\_cost\_nanos=Fraction(40, 1),

&#x20;       mean\_task\_cost\_nanos=Fraction(10, 1),

&#x20;       expected\_cost\_per\_solved\_nanos=UndefinedValue(reason="zero\_expected\_solves"),

&#x20;       actual\_all\_repetitions\_spend\_nanos=40,

&#x20;   )



&#x20;   both = compute\_both\_frontiers(\[p\_fast, p\_tied, p\_cheap, p\_zero])



&#x20;   headline = both\[COST\_AXIS\_COST\_PER\_SOLVED]

&#x20;   assert headline.is\_headline\_axis is True

&#x20;   assert headline.frontier\_series\_ids == ("C\_fast\_good", "C\_tied")

&#x20;   assert headline.dominated\_series\_ids == ("C\_cheap\_low",)

&#x20;   assert headline.undefined\_series\_ids == ("C\_zero\_solve",)



&#x20;   rows\_cps = {r.series\_id: r for r in headline.rows}

&#x20;   assert rows\_cps\["C\_fast\_good"].tie\_group\_id == "tie\_group\_1"

&#x20;   assert rows\_cps\["C\_fast\_good"].tied\_with == ("C\_tied",)

&#x20;   assert rows\_cps\["C\_cheap\_low"].dominated\_by == ("C\_fast\_good", "C\_tied")

&#x20;   assert rows\_cps\["C\_zero\_solve"].status == "undefined\_cost"

&#x20;   assert rows\_cps\["C\_zero\_solve"].is\_on\_frontier is False



&#x20;   diag = both\[COST\_AXIS\_MEAN\_TASK\_COST]

&#x20;   assert diag.is\_headline\_axis is False

&#x20;   assert diag.frontier\_series\_ids == ("C\_zero\_solve", "C\_cheap\_low", "C\_fast\_good", "C\_tied")

&#x20;   assert diag.dominated\_series\_ids == ()

&#x20;   assert diag.undefined\_series\_ids == ()





def test\_wp5\_valid\_panel\_fixture\_frontiers() -> None:

&#x20;   env = parse\_analysis\_json((FIXTURES\_DIR / "valid\_panel.json").read\_bytes())

&#x20;   frontiers = compute\_frontiers\_from\_envelope(env)



&#x20;   # A has pass@1=1/2, cost/solve=3M; B has pass@1=1/2, cost/solve=20M -> A dominates B

&#x20;   cps\_table = frontiers\[COST\_AXIS\_COST\_PER\_SOLVED]

&#x20;   assert cps\_table.frontier\_series\_ids == ("A",)

&#x20;   assert cps\_table.dominated\_series\_ids == ("B",)



```



\---



\## FILE: docs/analysis-foundation-methods.md



```markdown

\# Dojo Statistics Foundation Methods Reference (Batch A: WP1–WP5)



\## 1. Scope and Governance Boundary



This document specifies the mathematical definitions, normalization rules, bootstrap resampling algorithms, sensitivity analyses, and Pareto frontier constructions implemented in `dojo/bench/records.py`, `dojo/bench/stats.py`, and `dojo/bench/frontier.py`.



\- \*\*No Implicit Publication Authority:\*\* Every input envelope is assigned `EligibilityStatus(status="UNVERIFIED", publishable=False, development\_only=True)`. Passing a non-null `registration\_id` or `evidence\_kind="real"` never flips `publishable` to `True`. Stage B registration and real held-out governance require a separate trusted protocol verifier.

\- \*\*No Usage/Price Inference:\*\* Provider spend is taken strictly from validated integer `cost\_nano\_usd` fields ($10^{-9}\\text{ USD}$). Missing cost (`null`) is never coerced to `0`, and missing token/step/wall-clock counters are never inferred from cost or from other runs.

\- \*\*Owner Learning Boundary:\*\* This library is the reference implementation for task 9b/9g3 and does not replace the project owner's required handwritten exercise in 16c.



\---



\## 2. Panel Validation and Outcome Normalization (WP1)



Given an `ExpectedPlan` with ordered task list $T = (t\_1, \\dots, t\_n)$ and declared seed tuples $S\_c = (s\_{c,1}, \\dots, s\_{c,k\_c})$ for each configuration $c \\in C$, a complete panel must contain \*\*exactly one\*\* valid record for every expected cell:



$$\\mathcal{E} = \\{ (c, t, s) \\mid t \\in T,\\; c \\in C,\\; s \\in S\_c \\}, \\quad |\\mathcal{E}| = n \\sum\_{c \\in C} k\_c$$



\### Scorer Status and Evidence Validity Matrix



| `scorer\_status` | Required `outcome` | Required `evidence\_validity` | Additional Invariant | Effect on Headline Aggregation |

|---|---|---|---|---|

| `passed` | `solved` | `valid` | `execution\_complete is True` | Included ($y\_{c,t,r} = 1$) |

| `failed` | `unsolved` | `valid` | `execution\_complete is True` | Included ($y\_{c,t,r} = 0$) |

| `candidate\_error` | `unsolved` | `valid` | `baseline\_verified is True` and `execution\_complete is True` | Included ($y\_{c,t,r} = 0$) iff `baseline\_verified=True`; otherwise \*\*blocked\*\* |

| `invalid\_evidence` | `undetermined` | `invalid` | — | \*\*Blocked\*\* (`audit.status = "blocked"`) |

| `infrastructure\_error` | `undetermined` | `unknown` | — | \*\*Blocked\*\* (`audit.status = "blocked"`) |



Any missing cell, duplicate cell, unexpected cell, mixed split (`train` mixed with `held\_out`), conflicting task `family\_id`, or blocker finding sets `audit.status = "blocked"` and prevents all headline metric calculations. If all cells are valid for outcomes but one or more cells have `cost\_nano\_usd = null`, `audit.status` is `"cost\_incomplete"` (`success\_only\_allowed = True`, `cost\_comparison\_allowed = False`).



\---



\## 3. Primary Estimands and Cost Semantics (WP2)



Let $n = |T|$ be the number of tasks and $k\_c = |S\_c|$ be the declared repetition count for configuration $c$. For each task $t \\in T$ and seed $r \\in S\_c$, let $y\_{c,t,r} \\in \\{0, 1\\}$ denote whether the run solved the task, and $\\text{cost}\_{c,t,r} \\in \\mathbb{Z}\_{\\ge 0}$ denote the measured cost in nano-USD.



1\. \*\*Per-task pass rate and mean single-seed cost:\*\*

&#x20;  $$p\_{c,t} = \\frac{1}{k\_c} \\sum\_{r \\in S\_c} y\_{c,t,r}, \\qquad m\_{c,t} = \\frac{1}{k\_c} \\sum\_{r \\in S\_c} \\text{cost}\_{c,t,r}$$



2\. \*\*Equal-task-weighted $\\text{pass@1}$:\*\*

&#x20;  $$\\text{pass@1}(c) = \\frac{1}{n} \\sum\_{t \\in T} p\_{c,t}$$

&#x20;  Unequal seed counts $k\_c$ refine the per-task estimate $p\_{c,t}$ without overweighting tasks or configurations. This is $\\text{pass@1}$ (expected success of one randomly chosen seed), not $\\text{pass@}k$.



3\. \*\*Expected solved tasks (single random seed per task):\*\*

&#x20;  $$S\_{\\text{exp}}(c) = \\sum\_{t \\in T} p\_{c,t} = n \\cdot \\text{pass@1}(c)$$



4\. \*\*Expected total cost of one random-seed run per task (`expected\_total\_cost\_nanos`):\*\*

&#x20;  $$C\_{\\text{exp}}(c) = \\sum\_{t \\in T} m\_{c,t}, \\qquad \\bar{m}(c) = \\frac{1}{n} C\_{\\text{exp}}(c)$$



5\. \*\*Expected cost per solved task (`expected\_cost\_per\_solved\_nanos`):\*\*

&#x20;  $$\\text{CPS}(c) = \\begin{cases} \\dfrac{C\_{\\text{exp}}(c)}{S\_{\\text{exp}}(c)} = \\dfrac{\\sum\_{t \\in T} m\_{c,t}}{\\sum\_{t \\in T} p\_{c,t}} \& \\text{if } S\_{\\text{exp}}(c) > 0 \\\\\[8pt] \\text{UndefinedValue}(\\texttt{"zero\\\_expected\\\_solves"}) \& \\text{if } S\_{\\text{exp}}(c) = 0 \\end{cases}$$

&#x20;  Measured costs of failed runs remain in the numerator $C\_{\\text{exp}}(c)$.



6\. \*\*Actual all-repetition spend (`actual\_all\_repetitions\_spend\_nanos`):\*\*

&#x20;  $$C\_{\\text{actual}}(c) = \\sum\_{t \\in T} \\sum\_{r \\in S\_c} \\text{cost}\_{c,t,r}$$

&#x20;  Reported separately as an exact integer; never divided by single-seed expected solves $S\_{\\text{exp}}(c)$.



All intermediate calculations use Python `fractions.Fraction` and exact `int` nano-USD, completely independent of floating-point rounding or ambient `decimal` context.



\---



\## 4. Paired Task Bootstrap (WP3)



\- \*\*Resampling unit:\*\* Tasks $t \\in \\{0, \\dots, n-1\\}$.

\- \*\*Default replicates:\*\* $B = 10,000$ using an isolated `random.Random(seed)` instance.

\- \*\*Pairing invariant:\*\* In replicate $b \\in \\{1, \\dots, B\\}$, a single multiset of $n$ task indices $I^{(b)} = (i^{(b)}\_1, \\dots, i^{(b)}\_n)$ is drawn uniformly with replacement from $\\{0, \\dots, n-1\\}$. Every compared configuration (and future cascade policy) is evaluated on the \*\*exact same\*\* sampled task indices $I^{(b)}$, retaining all $k\_c$ seed runs of each sampled task.

\- \*\*Quantile convention (`sorted\_empirical\_nearest\_rank\_linear\_endpoints`):\*\* Given $B$ sorted exact `Fraction` draws $x\_{(0)} \\le x\_{(1)} \\le \\dots \\le x\_{(B-1)}$ and quantile $q \\in \[0, 1]$ (where $q\_{\\text{low}} = (1-\\alpha)/2$ and $q\_{\\text{high}} = 1 - (1-\\alpha)/2$):

&#x20; $$h = q (B - 1), \\quad \\ell = \\lfloor h \\rfloor, \\quad u = \\lceil h \\rceil, \\quad Q(q) = x\_{(\\ell)} + (h - \\ell)\\bigl(x\_{(u)} - x\_{(\\ell)}\\bigr)$$

\- \*\*Zero-solve draw rule:\*\* For ratio metrics ($\\text{CPS}(c)$ and $\\Delta \\text{CPS}$), if any bootstrap replicate $b$ has zero expected solves ($\\sum\_{j=1}^n p\_{c, i^{(b)}\_j} = 0$), the replicate is counted in `zero\_solve\_draws` and `undefined\_draws`, and the unconditional confidence interval endpoints (`lower`, `upper`) are returned as `UndefinedValue(reason="unconditional\_interval\_blocked\_by\_zero\_solve\_draws")`. Zero-solve draws are never silently discarded to fabricate a narrower conditional interval.



\---



\## 5. Sensitivity Analyses (WP4)



\### 5.1 Family-Cluster Bootstrap (`family\_cluster\_bootstrap`)

\- \*\*Non-primary label:\*\* `is\_primary = False`, `estimand\_label = "sensitivity\_family\_cluster\_bootstrap\_task\_weighted\_within\_resampled\_clusters"`.

\- \*\*Resampling rule:\*\* Let $F = (f\_1, \\dots, f\_M)$ be the $M$ distinct `family\_id` clusters. Each replicate draws $M$ families with replacement, includes all tasks belonging to each drawn family occurrence (retaining all seeds), and weights included task occurrences equally.

\- \*\*Sample-size variation and total-cost scaling:\*\* When family sizes $|T\_f|$ vary, the resampled task count $n^{\*(b)} = \\sum\_{m=1}^M |T\_{f^{(b)}\_m}|$ varies across draws. To keep total-cost intervals comparable to the original $n$-task benchmark rather than reflecting random cluster-size fluctuations, the estimator reports:

&#x20; $$\\hat{C}^{\*(b)}\_{\\text{target-}n}(c) = n \\cdot \\bar{m}^{\*(b)}(c) = \\frac{n}{n^{\*(b)}} \\sum\_{j=1}^{n^{\*(b)}} m\_{c, t^{(b)}\_j}$$

&#x20; alongside `min\_resampled\_tasks`, `max\_resampled\_tasks`, and `mean\_resampled\_tasks`.



\### 5.2 Seed-Position and Seed-Subset Sensitivity (`seed\_sensitivity\_analysis`)

\- Evaluates predeclared ordinal seed positions (`position\_0`, `position\_1`, ...) and explicit caller-supplied seed subsets with full task coverage.

\- When configurations have asymmetric seed lists (e.g., $S\_A = (0, 1)$, $S\_B = (0)$), cross-config single-seed comparisons are valid at `common\_seed\_positions` ($0 \\dots \\min\_c k\_c - 1$) or on `shared\_exact\_seeds` ($S\_A \\cap S\_B$), whereas additional seeds in $S\_A$ quantify within-config seed variance.



\---



\## 6. Cost-vs-Success Pareto Frontiers (WP5)



`compute\_frontier` supports two explicit cost axes (minimizing cost, maximizing $\\text{pass@1}$):

1\. `cost\_per\_solved` (headline axis: $\\text{CPS}(c)$ vs $\\text{pass@1}(c)$)

2\. `mean\_task\_cost` (diagnostic axis: $\\bar{m}(c)$ vs $\\text{pass@1}(c)$)



Configuration $A$ Pareto-dominates $B$ on cost axis $X$ iff both are defined and:

$$(X\_A \\le X\_B \\text{ and } \\text{pass@1}\_A \\ge \\text{pass@1}\_B) \\quad \\text{and} \\quad (X\_A < X\_B \\text{ or } \\text{pass@1}\_A > \\text{pass@1}\_B)$$



\- \*\*Exact Ties:\*\* Configurations with identical rational $(X, \\text{pass@1})$ are all retained on the frontier if non-dominated and linked via a shared `tie\_group\_id` and `tied\_with` peer tuple.

\- \*\*Undefined Points:\*\* Any configuration with `UndefinedValue` on the chosen cost axis (such as a zero-solve configuration on `cost\_per\_solved`) receives `status = "undefined\_cost"`, `is\_on\_frontier = False`, and cannot dominate or be dominated by valid configurations.



\---



\## 7. Known Answers on Synthetic Fixtures



1\. \*\*`valid\_panel.json` (4 tasks, 1 seed each for A and B):\*\*

&#x20;  - Config A: $\\text{pass@1} = 1/2$, $C\_{\\text{exp}} = 6,000,000\\text{ nanos}$, $\\bar{m} = 1,500,000\\text{ nanos}$, $\\text{CPS} = 3,000,000\\text{ nanos}$, $C\_{\\text{actual}} = 6,000,000\\text{ nanos}$.

&#x20;  - Config B: $\\text{pass@1} = 1/2$, $C\_{\\text{exp}} = 40,000,000\\text{ nanos}$, $\\bar{m} = 10,000,000\\text{ nanos}$, $\\text{CPS} = 20,000,000\\text{ nanos}$, $C\_{\\text{actual}} = 40,000,000\\text{ nanos}$.

&#x20;  - Frontier: `A` dominates `B` on both `cost\_per\_solved` and `mean\_task\_cost`.

2\. \*\*`unequal\_seed\_panel.json` (1 task, A has seeds `\[0, 1]`, B has seed `\[0]`):\*\*

&#x20;  - Config A: $\\text{pass@1} = 1/2$, $C\_{\\text{exp}} = 3\\text{ nanos}$, $\\text{CPS} = 6\\text{ nanos}$, $C\_{\\text{actual}} = 6\\text{ nanos}$.

&#x20;  - Config B: $\\text{pass@1} = 0$, $C\_{\\text{exp}} = 10\\text{ nanos}$, $\\text{CPS} = \\text{UndefinedValue}(\\texttt{"zero\\\_expected\\\_solves"})$, $C\_{\\text{actual}} = 10\\text{ nanos}$.



```



\---



\## FILE: docs/analysis-foundation-api.md



```markdown

\# Dojo Statistics Foundation API \& Batch B Integration Guide (WP1–WP5)



\## 1. Module Overview \& Public Symbols



Batch A delivers three pure standard-library modules under `dojo/bench/` with zero circular imports and explicit `\_\_all\_\_` exports:



| Module | Primary Public Types \& Functions |

|---|---|

| `dojo.bench.records` | `SCHEMA\_VERSION`, `FOUNDATION\_METHOD\_VERSION`, `MAX\_INPUT\_BYTES`, `MAX\_JSON\_DEPTH`, `MAX\_RECORDS`, `AnalysisInputError`, `UndefinedValue`, `EligibilityStatus`, `ExpectedPlan`, `NormalizedRecord`, `AuditFinding`, `PanelAudit`, `NormalizedEnvelope`, `loads\_bounded\_json`, `parse\_analysis\_envelope`, `parse\_analysis\_json`, `validate\_panel`, `compute\_expected\_plan\_hash`, `compute\_input\_sha256`, `format\_fraction\_Or\_undef` |

| `dojo.bench.stats` | `DEFAULT\_BOOTSTRAP\_REPLICATES`, `MAX\_BOOTSTRAP\_REPLICATES`, `MAX\_BOOTSTRAP\_WORKLOAD`, `QUANTILE\_METHOD`, `TaskPoint`, `TaskSeries`, `SeriesPoint`, `SecondaryMetricSummary`, `ConfigMetrics`, `BootstrapInterval`, `SeriesBootstrapSummary`, `PairedDifferenceSummary`, `PairedBootstrapResult`, `FamilySeriesSummary`, `FamilyBootstrapResult`, `SeedSensitivityEntry`, `SeedSensitivityResult`, `evaluate\_series\_point`, `build\_config\_task\_series`, `compute\_config\_metrics`, `compute\_all\_config\_metrics`, `compute\_empirical\_quantile`, `paired\_task\_bootstrap`, `family\_cluster\_bootstrap`, `seed\_sensitivity\_analysis` |

| `dojo.bench.frontier` | `COST\_AXIS\_COST\_PER\_SOLVED`, `COST\_AXIS\_MEAN\_TASK\_COST`, `VALID\_COST\_AXES`, `FrontierRow`, `FrontierTable`, `compute\_frontier`, `compute\_both\_frontiers`, `compute\_frontiers\_from\_envelope` |



\---



\## 2. Exact Function Signatures



```python

\# dojo/bench/records.py

def loads\_bounded\_json(raw: str | bytes) -> dict\[str, Any]: ...

def parse\_analysis\_envelope(data: Mapping\[str, Any]) -> NormalizedEnvelope: ...

def parse\_analysis\_json(raw: str | bytes) -> NormalizedEnvelope: ...

def validate\_panel(

&#x20;   expected\_plan: ExpectedPlan,

&#x20;   records: Sequence\[NormalizedRecord],

&#x20;   \*,

&#x20;   dataset\_id: str,

&#x20;   evidence\_kind: str,

) -> PanelAudit: ...

def compute\_expected\_plan\_hash(expected\_plan: ExpectedPlan) -> str: ...

def compute\_input\_sha256(

&#x20;   \*,

&#x20;   schema\_version: int,

&#x20;   dataset\_id: str,

&#x20;   evidence\_kind: str,

&#x20;   expected\_plan: ExpectedPlan,

&#x20;   records: Sequence\[NormalizedRecord],

) -> str: ...

def format\_fraction\_Or\_undef(value: Fraction | UndefinedValue) -> dict\[str, Any]: ...



\# dojo/bench/stats.py

def evaluate\_series\_point(

&#x20;   series\_id: str,

&#x20;   task\_points: Sequence\[TaskPoint],

&#x20;   \*,

&#x20;   target\_n\_tasks: int | None = None,

&#x20;   include\_actual\_spend: bool = True,

) -> SeriesPoint: ...

def build\_config\_task\_series(

&#x20;   envelope: NormalizedEnvelope,

&#x20;   config\_id: str,

&#x20;   \*,

&#x20;   seed\_subset: Sequence\[int] | None = None,

&#x20;   series\_id: str | None = None,

) -> TaskSeries: ...

def compute\_config\_metrics(envelope: NormalizedEnvelope, config\_id: str) -> ConfigMetrics: ...

def compute\_all\_config\_metrics(envelope: NormalizedEnvelope) -> dict\[str, ConfigMetrics]: ...

def paired\_task\_bootstrap(

&#x20;   series\_list: Sequence\[TaskSeries],

&#x20;   \*,

&#x20;   replicates: int = 10\_000,

&#x20;   seed: int = 17,

&#x20;   confidence\_level: float | Fraction = Fraction(95, 100),

&#x20;   comparison\_pairs: Sequence\[tuple\[str, str]] | None = None,

&#x20;   sampled\_task\_indices: Sequence\[Sequence\[int]] | None = None,

) -> PairedBootstrapResult: ...

def family\_cluster\_bootstrap(

&#x20;   series\_list: Sequence\[TaskSeries],

&#x20;   \*,

&#x20;   replicates: int = 10\_000,

&#x20;   seed: int = 17,

&#x20;   confidence\_level: float | Fraction = Fraction(95, 100),

&#x20;   comparison\_pairs: Sequence\[tuple\[str, str]] | None = None,

&#x20;   sampled\_family\_indices: Sequence\[Sequence\[int]] | None = None,

) -> FamilyBootstrapResult: ...

def seed\_sensitivity\_analysis(

&#x20;   envelope: NormalizedEnvelope,

&#x20;   \*,

&#x20;   seed\_positions: Sequence\[int] | None = None,

&#x20;   seed\_subsets\_by\_config: Mapping\[str, Sequence\[Sequence\[int]]] | None = None,

) -> SeedSensitivityResult: ...



\# dojo/bench/frontier.py

def compute\_frontier(

&#x20;   items: Sequence\[SeriesPoint | ConfigMetrics],

&#x20;   \*,

&#x20;   cost\_axis: str = "cost\_per\_solved",

) -> FrontierTable: ...

def compute\_both\_frontiers(

&#x20;   items: Sequence\[SeriesPoint | ConfigMetrics],

) -> dict\[str, FrontierTable]: ...

def compute\_frontiers\_from\_envelope(

&#x20;   envelope: NormalizedEnvelope,

) -> dict\[str, FrontierTable]: ...



```



\---



\## 3. How Batch B (Cascades, Policies \& Report Export) Reuses Batch A



Batch A is intentionally structured around `TaskPoint`, `TaskSeries`, and `SeriesPoint` so Batch B (`dojo/cascade/simulate.py` and `dojo/bench/report.py`) can plug cold-restart cascades directly into the existing bootstrap, sensitivity, and frontier engines without duplicating math:



1\. \*\*Cascade-to-`TaskSeries` Seam:\*\* For each task $t$ in `envelope.expected\_plan.tasks`, a cold-restart cascade $A \\to B$ computes its exact analytical cross-product task success rate $p\_{\\text{cascade}, t}$ (`Fraction`) and task expected cost $m\_{\\text{cascade}, t}$ (`Fraction`) and constructs a `TaskPoint(task\_id=t, family\_id=..., seed\_count=k\_A \* k\_B, pass\_rate=p\_cascade\_t, mean\_cost\_nanos=m\_cascade\_t, actual\_all\_seeds\_cost\_nanos=None)`.

2\. \*\*Point Estimates:\*\* Calling `evaluate\_series\_point("cascade\_A\_to\_B", cascade\_task\_points, include\_actual\_spend=False)` returns a `SeriesPoint` with exact rational `pass\_at\_1`, `expected\_total\_cost\_nanos`, and `expected\_cost\_per\_solved\_nanos`.

3\. \*\*Paired Bootstrap \& Sensitivity:\*\* Passing `\[series\_A, series\_B, series\_cascade]` to `paired\_task\_bootstrap` or `family\_cluster\_bootstrap` resamples tasks (or families) using the \*\*exact same task indices\*\* across `A`, `B`, and `cascade`, automatically producing paired differences (`cascade - A`, `cascade - B`).

4\. \*\*Pareto Frontiers:\*\* Passing `\[metrics\_A.primary, metrics\_B.primary, cascade\_point]` to `compute\_both\_frontiers` places the cascade directly onto both cost-vs-success frontier tables alongside baseline configurations.



\---



\## 4. Executable Usage Example



```python

from fractions import Fraction

from pathlib import Path



from dojo.bench.frontier import COST\_AXIS\_COST\_PER\_SOLVED, compute\_frontiers\_from\_envelope

from dojo.bench.records import parse\_analysis\_json

from dojo.bench.stats import (

&#x20;   build\_config\_task\_series,

&#x20;   compute\_all\_config\_metrics,

&#x20;   family\_cluster\_bootstrap,

&#x20;   paired\_task\_bootstrap,

&#x20;   seed\_sensitivity\_analysis,

)



raw = Path("tests/fixtures/analysis/valid\_panel.json").read\_bytes()

envelope = parse\_analysis\_json(raw)

assert envelope.audit.status == "valid"



metrics = compute\_all\_config\_metrics(envelope)

assert metrics\["A"].primary.pass\_at\_1 == Fraction(1, 2)

assert metrics\["A"].primary.expected\_cost\_per\_solved\_nanos == Fraction(3\_000\_000, 1)



series\_a = build\_config\_task\_series(envelope, "A")

series\_b = build\_config\_task\_series(envelope, "B")



boot = paired\_task\_bootstrap(\[series\_a, series\_b], replicates=1000, seed=17)

fam\_boot = family\_cluster\_bootstrap(\[series\_a, series\_b], replicates=1000, seed=17)

seed\_sens = seed\_sensitivity\_analysis(envelope)

frontiers = compute\_frontiers\_from\_envelope(envelope)



assert frontiers\[COST\_AXIS\_COST\_PER\_SOLVED].frontier\_series\_ids == ("A",)



```



\---



\## 5. What Is Deferred to Batch B



\* `dojo/cascade/policies.py` (WP6: observable-only policy AST, canonical hash, and train-only selection)

\* `dojo/cascade/simulate.py` (WP7: cold-restart cascade composition and trigger TP/FP/FN/TN confusion diagnostics)

\* `dojo/bench/report.py` (WP8: top-level JSON report export envelope)

\* `dojo/bench/analyze.py` (WP9: standalone `python -m dojo.bench.analyze` CLI)

\* `tests/test\_cascade.py`, `tests/test\_analysis\_report.py`, `tests/test\_analysis\_cli.py` (WP10 Batch B test suites)



```



\---



\## Verification Commands \& Honest Execution Ledger\[cite: 2]



\### Primary Workspace Verification Commands\[cite: 2]



Run these commands in the primary workspace after integrating the files above:



```powershell

.venv\\Scripts\\python.exe -m pytest tests/test\_analysis\_records.py tests/test\_statistics.py -q --tb=short

.venv\\Scripts\\ruff.exe check dojo/bench/records.py dojo/bench/stats.py dojo/bench/frontier.py tests/test\_analysis\_records.py tests/test\_statistics.py

.venv\\Scripts\\python.exe -m pytest -q --tb=short



```



\### Honest Execution Ledger







\* \*\*Executed in this chat environment:\*\* `0` pytest suites, `0` ruff runs, `0` subprocesses (this web chat environment has no local shell, Python interpreter, or repository checkout).





\* \*\*Statically verified against packet specifications:\*\*

\* All imports, public symbols (`\_\_all\_\_`), type annotations, and function signatures across `dojo/bench/records.py`, `dojo/bench/stats.py`, `dojo/bench/frontier.py`, `tests/test\_analysis\_records.py`, `tests/test\_statistics.py`, and `docs/analysis-foundation-api.md` match 1-to-1 with zero phantom helpers.





\* Fixture JSON files (`valid\_panel.json`, `unequal\_seed\_panel.json`, `invalid\_panel.json`) have their test-only `"expected"` annotation removed as required.





\* Hand-verified arithmetic matches every required known answer (`A` pass@1 = `1/2`, total cost = `6,000,000`, cost/solve = `3,000,000`; `B` pass@1 = `1/2`, total cost = `40,000,000`, cost/solve = `20,000,000`; unequal-seed `A` pass@1 = `1/2`, expected 1-seed total cost = `3`, actual all-repeat spend = `6`, cost/solve = `6`; `B` cost/solve = `UndefinedValue("zero\_expected\_solves")`).











END OF BATCH A DELIVERY

