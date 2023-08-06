# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

from coveriteam.actors.misc import TestCriterionInstrumentor
from coveriteam.actors.testers import ProgramTester
from coveriteam.actors.analyzers import ProgramVerifier, ProgramValidator
from coveriteam.language.artifact import (
    TestGoal,
    CProgram,
    BehaviorSpecification,
    TestSpecification,
)
from coveriteam.example_compositions import (
    validated_verifier,
    metaval_prototype,
    conditional_tester,
    verifier_based_tester,
    conditional_tester_verifier_based,
    atva_paper_fig_14,
)
from nose.tools import nottest
from pathlib import Path
import sys
import coveriteam.util as util

conditional_tester = nottest(conditional_tester)
verifier_based_tester = nottest(verifier_based_tester)
conditional_tester_verifier_based = nottest(conditional_tester_verifier_based)

# Taking the test data from examples folder
TEST_DATA_DIR = f'{Path(sys.path[0]) / "../examples/"}/'

property_path_reach_safety = TEST_DATA_DIR + "properties/unreach-call.prp"
property_path_termination = TEST_DATA_DIR + "properties/termination.prp"
property_path_mem_safety = TEST_DATA_DIR + "properties/valid-memsafety.prp"
property_path_no_overflow = TEST_DATA_DIR + "properties/no-overflow.prp"
property_path_branch_coverage = TEST_DATA_DIR + "properties/coverage-branches.prp"

program_path_reach_safety_false = TEST_DATA_DIR + "c/Problem02_label16.c"
program_path_reach_safety_true = TEST_DATA_DIR + "c/Problem01_label00.c"
program_path_termination_false = TEST_DATA_DIR + "c/Madrid.c"
program_path_mem_safety_false = TEST_DATA_DIR + "c/cstrcat_unsafe.c"
program_path_no_overflow_false = TEST_DATA_DIR + "c/AdditionIntMax.c"
program_path_no_overflow_true = TEST_DATA_DIR + "c/ConversionToSignedInt.c"
program_path_verifier_based_tester = TEST_DATA_DIR + "c/Problem01_label15.c"


def setup_module():
    util.set_cache_directories()


def test_validated_verifier_cpachecker():
    ver = ProgramVerifier("actors/cpa-seq.yml")
    val = ProgramValidator("actors/cpa-validate-violation-witnesses.yml")
    vv = validated_verifier(ver, val)

    spec = BehaviorSpecification(property_path_reach_safety)
    cprogram = CProgram(program_path_reach_safety_false)
    res = vv.act(program=cprogram, spec=spec)
    assert res["verdict"] == "false"
    cprogram = CProgram(program_path_reach_safety_true)
    res = vv.act(program=cprogram, spec=spec)
    assert res["verdict"] == "true"


@nottest
def test_validated_verifier_ultimate():
    ver = ProgramVerifier("actors/uautomizer.yml")
    val = ProgramValidator("actors/cpa-validate-violation-witnesses.yml")
    vv = validated_verifier(ver, val)
    spec = BehaviorSpecification(property_path_reach_safety)
    cprogram = CProgram(program_path_reach_safety_false)
    res = vv.act(program=cprogram, spec=spec)
    assert res["verdict"] == "false"
    cprogram = CProgram(program_path_reach_safety_true)
    res = vv.act(program=cprogram, spec=spec)
    assert res["verdict"] == "true"


@nottest
def test_validated_verifier_produce_xml(ver, val):
    vv = validated_verifier(ver, val)
    spec = BehaviorSpecification(property_path_reach_safety)
    cprogram = CProgram(program_path_reach_safety_false)
    res = vv.act_and_save_xml(program=cprogram, spec=spec)
    print("Exected: False, Actual: {}".format(res["verdict"]))


@nottest
def test_validated_verifier_metaval(ver):
    vv = validated_verifier(ver, metaval_prototype())
    print("Testing unreach call.......")
    spec = BehaviorSpecification(property_path_reach_safety)
    cprogram = CProgram(program_path_reach_safety_false)
    res = vv.act(program=cprogram, spec=spec)
    print("Exected: FALSE, Actual: {}".format(res["verdict"]))

    print("Testing unreach call.......")
    cprogram = CProgram(program_path_reach_safety_true)
    res = vv.act(program=cprogram, spec=spec)
    print("Exected: TRUE, Actual: {}".format(res["verdict"]))

    print("Testing overflow.......")
    spec = BehaviorSpecification(property_path_no_overflow)
    cprogram = CProgram(program_path_no_overflow_false)
    res = vv.act(program=cprogram, spec=spec)
    print("Exected: FALSE, Actual: {}".format(res["verdict"]))

    print("Testing overflow.......")
    spec = BehaviorSpecification(property_path_no_overflow)
    cprogram = CProgram(program_path_no_overflow_true)
    res = vv.act(program=cprogram, spec=spec)
    print("Exected: TRUE, Actual: {}".format(res["verdict"]))

    print("Testing memory safety......")
    spec = BehaviorSpecification(property_path_mem_safety)
    cprogram = CProgram(program_path_mem_safety_false)
    res = vv.act(program=cprogram, spec=spec)
    print("Exected: FALSE, Actual: {}".format(res["verdict"]))

    print("Testing Termination.......")
    spec = BehaviorSpecification(property_path_termination)
    cprogram = CProgram(program_path_termination_false)
    res = vv.act(program=cprogram, spec=spec)
    print("Exected: FALSE, Actual: {}".format(res["verdict"]))


@nottest
def test_verifier_based_tester():
    ver = ProgramVerifier("actors/cpa-seq.yml")
    print("...............Testing Verifier based tester")
    spec = BehaviorSpecification(property_path_reach_safety)
    cprogram = CProgram(program_path_verifier_based_tester)
    verifier_based_tester(ver).act(program=cprogram, spec=spec)


@nottest
def test_conditional_testing():
    print("...............Testing Conditional Tester with klee")
    spec = TestSpecification(property_path_branch_coverage)
    cprogram = CProgram(TEST_DATA_DIR + "c/test.c")
    ct = conditional_tester(ProgramTester("actors/klee.yml"))
    instrumented_program = TestCriterionInstrumentor(
        "actors/test-criterion-instrumentor.yml"
    ).act(program=cprogram, test_spec=spec)
    # It could also be a sequence but instrumenter is kind of separate. So, not sure.
    ct.act_and_save_xml(
        program=instrumented_program["program"],
        test_spec=spec,
        covered_goals=TestGoal(""),
    )


@nottest
def test_conditional_testing_verifier_based(ver):
    print("...............Testing Conditional Tester -- Verifier based")
    spec = TestSpecification(property_path_branch_coverage)
    cprogram = CProgram(program_path_verifier_based_tester)
    ct = conditional_tester_verifier_based(ver)
    instrumented_program = TestCriterionInstrumentor(
        "actors/test-criterion-instrumentor.yml"
    ).act(program=cprogram, test_spec=spec)
    # It could also be a sequence but instrumenter is kind of separate. So, not sure.
    ct.act_and_save_xml(
        program=instrumented_program["program"],
        test_spec=spec,
        covered_goals=TestGoal(""),
    )


@nottest
def test_atva_paper_fig_14(ver):
    print("...............Testing ATVA paper fig 14")
    spec = TestSpecification(property_path_branch_coverage)
    cprogram = CProgram(program_path_verifier_based_tester)
    ct = atva_paper_fig_14(ver)
    # It could also be a sequence but instrumenter is kind of separate. So, not sure.
    ct.act_and_save_xml(program=cprogram, test_spec=spec, covered_goals=TestGoal(""))
