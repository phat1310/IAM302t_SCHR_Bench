# Function Index — SCHR-Bench Pilot v1

> **Supervisor-only index.** Keep IDs, mutation operators and expected outputs out of prompts. All functions have the signature `int target(int a, int b, int c)` and perform **local calculations only**.

| ID | Level | Category | Controlled change | Skill stressed |
|---|---|---|---|---|
| A01 | Easy | Mock debugger policy | `!=` → `==` | Branch direction |
| A02 | Easy | Mock debugger policy | Bit condition inverted | Masked branch |
| A03 | Medium | Mock debugger policy | `>` → `>=` | Boundary check |
| A04 | Medium | Mock debugger policy | `&&` → `||` | Boolean semantics |
| A05 | Medium | Mock debugger policy | `>=2` → `>2` | Threshold equality |
| A06 | Tricky | Mock debugger policy | Omit second check | Early-return reasoning |
| A07 | Tricky | Mock debugger policy | `==1` → `!=1` | Derived flag reasoning |
| A08 | Tricky | Mock debugger policy | `<5` → `<=5` | Nested branch boundary |
| S01 | Easy | Toy decoder | XOR constant | Decode-key sensitivity |
| S02 | Easy | Toy decoder | XOR constant | Typed bitwise expression |
| S03 | Medium | Toy decoder | Offset `+7` → `+8` | Computed keys |
| S04 | Medium | Toy decoder | `^0x10` → `^0x11` | Hybrid arithmetic/bitwise |
| S05 | Medium | Toy decoder | `==` → `!=` | Reversed validation |
| S06 | Tricky | Toy decoder | Second-byte XOR key | Multi-byte conjunction |
| S07 | Tricky | Toy decoder | Add → subtract | Multi-stage transform |
| S08 | Tricky | Toy decoder | XOR → addition | Key derivation semantics |
| P01 | Easy | Persistence mock | Set bit → clear bit | Local state model |
| P02 | Easy | Persistence mock | Set service bit → clear | Bitmask changes |
| P03 | Medium | Persistence mock | Fallback constant | Missing-state handling |
| P04 | Medium | Persistence mock | Switch branch action | State machine |
| P05 | Medium | Persistence mock | Condition inverted | Conditional state change |
| P06 | Tricky | Persistence mock | Local mock API swap | Callee semantics |
| P07 | Tricky | Persistence mock | Bit set vs bit clear | Conditional bitmask |
| P08 | Tricky | Persistence mock | Omit cleanup step | Sequential updates |
| E01 | Easy | Environment mock | Predicate inverted | Boolean decision |
| E02 | Easy | Environment mock | Score threshold | Boundary at 2 |
| E03 | Medium | Environment mock | `<2048` → `<=2048` | Memory threshold |
| E04 | Medium | Environment mock | `>20` → `>=20` | Timing threshold |
| E05 | Medium | Environment mock | Mask `0xF0` → `0xE0` | Subtle masked comparison |
| E06 | Tricky | Environment mock | `||` → `&&` | Combined sensor flags |
| E07 | Tricky | Environment mock | XOR → OR | Non-equivalent bit logic |
| E08 | Tricky | Environment mock | Omit second condition | Exception logic |
| C01 | Easy | Control flow | `>` → `>=` | Boundary |
| C02 | Easy | Control flow | `==` → `!=` | Equality inversion |
| C03 | Medium | Control flow | Remove decrement | Sequential state update |
| C04 | Medium | Control flow | Outer branch `a` → `a||b` | Nested branches |
| C05 | Medium | Control flow | Loop `<` → `<=` | Off-by-one |
| C06 | Tricky | Control flow | Relax mask | Bitfield acceptance |
| C07 | Tricky | Control flow | Re-parenthesize boolean logic | Operator grouping |
| C08 | Tricky | Control flow | State transition `+1` → `-1` | Loop / state-machine tracing |

## Suggested Report 2 checkpoint evidence

1. **E0:** Run `python3 tools/check_suite.py` and attach test output. Show the original and mutant results for `A03`, `P06`, and `C08` to illustrate easy-to-tricky cases.
2. **Ghidra pilot:** Cross-compile selected pairs, import separately into Ghidra and capture two pseudocode outputs. Record if function logic can be recovered. Don't claim this was completed until screenshots exist.
3. **Mutation manifest:** Provide aggregate counts by category/operator/level without providing the answer key to the LLM.
4. **LLM pilot:** Use one fixed prompt and at least one pre-registered question for each selected pair. Do not show the model the original-vs-mutant distinction.
5. **Next milestone:** Extend test coverage, add teacher-prescribed light obfuscation under separate documented levels, and then run CT1–CT3 for a balanced gold set.

## Language for reporting

“Version 1 of the synthetic benchmark contains 40 manually designed security-critical **simulation functions**, each with one controlled mutated variant. Each original-mutant pair has predefined test vectors that permit behavior-grounded E0 checks. This suite does not implement real malware behaviors or Windows persistence. It is not yet evidence of LLM robustness or a full-scale SCHR-Bench result.”
