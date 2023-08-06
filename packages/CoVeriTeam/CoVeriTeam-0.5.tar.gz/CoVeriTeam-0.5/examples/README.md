<!--
This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
https://gitlab.com/sosy-lab/software/coveriteam

SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>

SPDX-License-Identifier: Apache-2.0
-->

# Tutorial
This folder contains a few example compositions that can
be executed on test inputs using the script [./run_examples.sh](run_examples.sh).

**The examples can be executed individually by copying the command-lines from [run_examples.sh](run_examples.sh).**

## Validating Verifier
The CoVeriTest program [validating-verifier.cvt](validating-verifier.cvt)
runs `UAutomizer` as a verifier on an example C program taken from the `sv-benchmarks` collection and
a reachability specification.
Then it runs `CPAchecker` as a validator using the verification witness produced by the verifier.

## Execution-Based Validation
Execution-based validation is an approach to result validation based on a violaion witness for a
reachability specification.
First, it transforms the given violation witness to a test case and then
executes the C program on the extracted test case to see if an `error` state is reached.
The file [execution-based-validation.cvt](execution-based-validation.cvt) contains
the CoVeriTeam program as discussed in the [literature](https://doi.org/10.1007/978-3-319-92994-1_1).

## Reducer-Based Construction of a Conditional Model Checker
Conditional model checkers produce and consume conditions in additon to consuming only programs and specifications,
and producing only verdict and witness. [Reducers](https://doi.org/10.1145/3180155.3180259) can
be used to construct a conditonal model checker from an existing model checker, thus saving implementation effort.
The CoVeriTeam program [cmc-reducer.cvt](cmc-reducer.cvt) constructs and executes a
reducer-based conditional model checker.

## Conditional Testing à la CondTest
The CoVeriTeam programs [condtest.cvt](condtest.cvt), and [repeat-condtest.cvt](repeat-condtest.cvt)
contain implementations of conditional testers as described in the [literature](https://doi.org/10.1007/978-3-030-31784-3\_11).

The CondTest program [condtest.cvt](condtest.cvt) takes three arguments:
- a tester to generate test cases,
- a program to generate test cases for, and
- test specification.

It can be executed on test data by using the following command:

```bash
 ../bin/coveriteam condtest.cvt \
     --input tester_yml="../actors/klee.yml" \
     --input prog="c/test.c" \
     --input spec="properties/coverage-branches.prp"
```

Other CoVeriTeam programs can be executed similarly on different inputs.

## Verification-Based Validation à la MetaVal
This approach uses verifiers as validators.
To achieve this, it first instruments the input program with information from the witness,
and then uses an off-the-shelf verifier to verify the instrumented program.
It chooses the verifier based on the specification.
The CoVeriTeam program [metaval.cvt](metaval.cvt)
constructs an actor that behavs similar to [MetaVal](https://gitlab.com/sosy-lab/software/metaval).

