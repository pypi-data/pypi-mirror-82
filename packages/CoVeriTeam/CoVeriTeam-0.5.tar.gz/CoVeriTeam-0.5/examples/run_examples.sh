#! /bin/bash

# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

cd $(dirname $0)

echo "Running a verifier"
echo
echo "Verifier"
../bin/coveriteam verifier.cvt \
  --input ver_path=../actors/cpa-seq.yml \
  --input prog_path=c/Problem02_label16.c \
  --input spec_path=properties/unreach-call.prp
echo

echo "Running CPAchecker"
echo
echo "Verifier"
../bin/coveriteam cpachecker.cvt \
  --input prog_path=c/Problem02_label16.c \
  --input spec_path=properties/unreach-call.prp
echo

echo "Constructing and Executing Example Actors"
echo
echo "Validating Verifier"
../bin/coveriteam validating-verifier.cvt \
  --input prog_path=c/Problem02_label16.c \
  --input spec_path=properties/unreach-call.prp
echo

echo "Execution-Based Validation"
../bin/coveriteam execution-based-validation.cvt \
  --input prog_path="c/Problem01_label15.c" \
  --input spec_path=properties/unreach-call.prp \
  --input witness_path="witnesses/Problem01_label15_reach_safety.graphml"
echo

echo "Execution-Based Validation Using a Witness Instrumentor"
../bin/coveriteam exe-validator-witness-instrument.cvt \
  --input prog_path=c/gcnr2008.i \
  --input spec_path=properties/unreach-call.prp \
  --input witness_path="witnesses/gcnr2008_violation_witness.graphml"
echo

echo "Reducer-Based Construction of a Conditional Model Checker"
../bin/coveriteam cmc-reducer.cvt \
  --input prog_path=c/slicingReducer-example.c \
  --input spec_path=properties/unreach-call.prp \
  --input cond_path="c/slicingCondition.txt"
echo

echo "Conditional Testing"
../bin/coveriteam condtest.cvt \
  --input prog_path="c/test.c" \
  --input tester_yml="../actors/klee.yml" \
  --input spec_path="properties/coverage-branches.prp"
echo

echo "Verifier-Based Tester"
../bin/coveriteam verifier-based-tester.cvt \
  --input prog_path="c/Problem01_label15.c" \
  --input spec_path=properties/unreach-call.prp
echo

echo "Cyclic Conditional Testing"
../bin/coveriteam repeat-condtest.cvt \
  --input prog_path="c/Problem01_label15.c" \
  --input spec_path="properties/coverage-branches.prp"
echo

echo "Verification-Based Validation. MetaVal with algorithm selection."
../bin/coveriteam metaval.cvt \
  --input prog_path="c/ConversionToSignedInt.i" \
  --input spec_path="properties/no-overflow.prp" \
  --input witness_path="witnesses/ConversionToSignedInt_nooverflow_witness.graphml"
echo
