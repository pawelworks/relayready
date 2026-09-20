"""Ordered Stafeta 0.1 lint rule registry."""

from __future__ import annotations

from collections.abc import Callable

from stafeta.models import Document, Finding, RuleContext
from stafeta.rules import (
    s001,
    s002,
    s003,
    s004,
    s005,
    s006,
    s007,
    s008,
    s009,
    s010,
    s011,
    s012,
    s013,
)

Rule = Callable[[Document, RuleContext], list[Finding]]

RULES: tuple[Rule, ...] = (
    s001.check,
    s002.check,
    s003.check,
    s004.check,
    s005.check,
    s006.check,
    s007.check,
    s008.check,
    s009.check,
    s010.check,
    s011.check,
    s012.check,
    s013.check,
)


def run(document: Document, context: RuleContext) -> list[Finding]:
    """Run every rule in stable rule-id order."""
    return [finding for rule in RULES for finding in rule(document, context)]

