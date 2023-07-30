from typing import TypedDict, Any, List, Dict, Optional


# Type Definitions
class EvalResult(TypedDict):
    result: bool
    reason: str


class Test(TypedDict):
    description: str
    eval: Any
    prompt_vars: Dict[str, str]
    failure_labels: List[str]


class TestRunStats(TypedDict):
    number_of_runs: int
    passed: int
    failed: int
    error: int
    pass_rate: Optional[float]
    flakiness: Optional[float]
    runtime: Optional[int]  # in milliseconds


class TestRunDetails(TypedDict):
    result: Optional[bool]
    reason: Optional[str]
    failure_labels: Optional[List[str]]
    prompt: str
    prompt_response: str


class TestRunResult(TypedDict):
    test: Test
    run_stats: TestRunStats
    run_details: List[TestRunDetails]


class IndividualTestRunResult(TypedDict):
    test: Test
    run_details: TestRunDetails


TestSuiteResults = Dict[str, TestRunResult]
