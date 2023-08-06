# This file is part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
# https://gitlab.com/sosy-lab/software/coveriteam
#
# SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

from coveriteam.language.actor import Transformer, Verifier, Validator
from coveriteam.language.atomicactor import AtomicActor
from coveriteam.language.artifact import (
    Program,
    Specification,
    Witness,
    Verdict,
    TestSuite,
    TestSpecification,
)
import logging
from coveriteam.language import CoVeriLangException
from coveriteam.util import create_archive
import os


def extract_verdict(self):
    try:
        with open(self.log_file(), "rt", errors="ignore") as outputFile:
            output = outputFile.readlines()
            # first 6 lines are for logging, rest is output of subprocess, see runexecutor.py for details
            output = output[6:]
    except IOError as e:
        logging.warning("Cannot read log file: %s", e.strerror)
        output = []

    return Verdict(self._tool.determine_result(0, 0, output, False))


def extract_witness(self, pattern):
    witness_list = list(self.log_dir().glob(pattern))

    if not witness_list:
        return Witness("")
    elif len(witness_list) != 1:
        msg = "Found more than 1 witnesses." + "\n".join(witness_list)
        raise CoVeriLangException(msg)
    else:
        return Witness(witness_list[0])


class ProgramVerifier(Verifier, AtomicActor):
    _input_artifacts = {"program": Program, "spec": Specification}
    _output_artifacts = {"verdict": Verdict, "witness": Witness}
    _result_files_patterns = ["**/*.graphml"]

    # It is a deliberate decision to not have the init function. We do not want anyone to
    # create instances of this class.

    def _prepare_args(self, program, spec):
        return [program.path, spec.path]

    def _extract_result(self):
        return {
            "verdict": extract_verdict(self),
            "witness": extract_witness(self, "**/*.graphml"),
        }


class ProgramValidator(Validator, AtomicActor):
    _input_artifacts = {
        "program": Program,
        "spec": Specification,
        "witness": Witness,
        "verdict": Verdict,
    }
    _output_artifacts = {"verdict": Verdict, "witness": Witness}
    _result_files_patterns = ["**/*.graphml"]

    def _get_arg_substitutions(self, program, spec, witness, verdict):
        return {"witness": self._get_relative_path_to_tool(witness.path)}

    def _prepare_args(self, program, spec, witness, verdict):
        return [program.path, spec.path]

    def _extract_result(self):
        return {
            "verdict": extract_verdict(self),
            "witness": extract_witness(self, "**/*.graphml"),
        }


class TestValidator(Transformer, AtomicActor):
    _input_artifacts = {
        "program": Program,
        "test_suite": TestSuite,
        "test_spec": TestSpecification,
    }
    _output_artifacts = {"verdict": Verdict}
    _result_files_patterns = []

    def _prepare_args(self, program, test_suite, test_spec):
        options_spec = ["--goal", self._get_relative_path_to_tool(test_spec.path)]
        testzip = os.path.join(os.path.dirname(test_suite.path), "test_suite.zip")
        create_archive(test_suite.path, testzip)
        testzip = self._get_relative_path_to_tool(testzip)
        options_test_suite = ["--test-suite", testzip]
        options = options_test_suite + options_spec
        return [program.path, "", options]

    def _extract_result(self):
        return {"verdict": extract_verdict(self)}
