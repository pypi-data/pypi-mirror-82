<!--
This file is part of CoVeriTeam,
a tool for on-demand composition of cooperative verification systems:
https://gitlab.com/sosy-lab/software/coveriteam

SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>

SPDX-License-Identifier: Apache-2.0
-->

# CoVeriTeam

## A Tool for On-Demand Composition of Cooperative Verification Systems

[![Apache 2.0 License](https://img.shields.io/badge/license-Apache--2-brightgreen.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.3818283.svg)](https://doi.org/10.5281/zenodo.3818283)

CoVeriTeam consists of a language for on-the-fly composition
of cooperative verification tools from existing components; and its execution engine.
The concept is based on
verification artifacts (programs, specifications, witnesses, results) as basic objects,
verification actors (verifiers, validators, testers, transformers) as basic operations, and
defines composition operators that make it possible to easily describe new compositions,
taking verification artifacts as interface between the verification actors.

CoVeriTeam is available under the Apache 2.0 license.

## Installation

### Dependencies

CoVeriTeam requires a machine with:
- Linux
- Python 3.6
- [BenchExec](https://github.com/sosy-lab/benchexec) 2.6 or later (to execute the atomic actors)

Please make sure that namespaces and cgroups are actorsured as described in the 
BenchExec [documentation](https://github.com/sosy-lab/benchexec/blob/master/doc/INSTALL.md).

### Virtual Machine
We have prepared a virtual machine with the required dependencies to ease the effort
to execute the examples, which is available at Zenodo [[DOI: 10.5281/zenodo.3813199](https://doi.org/10.5281/zenodo.3813199)].
Login credentials are: `userid: coveriteam-user` and `password: pass`.
There is a folder named `coveriteam/` in the home directory which contains everything needed to run the example programs.

We have prepared a virtual machine from an ISO image of standard [Ubuntu 1804](https://releases.ubuntu.com/18.04.4/ubuntu-18.04.4-desktop-amd64.iso) and applying the following steps:
* install Java 11 (for CPAchecker): `sudo apt install openjdk-11-jre-headless`
* install Java 8 (for UAutomizer): `sudo apt install openjdk-8-jre-headless`
* install clang 6.0 (for KLEE): `sudo apt install clang-6.0`
* install pyutil (for CondTest): `sudo apt install python3-psutil`
* install gcc-multiutil (for TestCov): `sudo apt install gcc-multilib`
* setup namespaces and cgroup actorsuration for BenchExec ([documentation](https://github.com/sosy-lab/benchexec/blob/master/doc/INSTALL.md))

### Directory Structure
The CoVeriTeam directory is structured as follows:
```
    .
    |-- bin                # script to execute CoVeriTeam
    |-- actors             # YAML actor-definition files for atomic actors
    |-- contrib            # script to create an independent archive packaging all dependencies
    |-- coveriteam         # Python source code
        |-- actors         # atomic actors like ProgramVerifier, ProgramTester, etc.
        |-- interpreter    # interpreter for the CoVeriTeam language
        |-- language       # core concepts of the CoVeriTeam language: actors, artifacts, composition
        |-- parser         # grammar and generated parser
    |-- examples           # tutorial examples
    |-- test_data          # test data for the examples
    |-- utils              # external libraries required for development
    |-- run_examples.sh    # script to execute all the tutorial examples
    |-- smoke_test_all_tools.sh   # report tool information from all atomic actors in the actors/ folder
    |-- LICENSE            # Apache 2.0 license file
```

## Usage
Run `bin/coveriteam --help` to see available command line arguments. 
The values required by the CoVeriTeam program are passed using the `--input` parameter followed by 
a `key=value` pair and the CoVeriTeam program file.

```bash
bin/coveriteam
    --input key1=val1   (pass input parameters to the program)
    --input key2=val2   (... and so on)
    --gen-code          (print the generated python code instead of executing)
    --debug             (print debug messages)
    <program_file>      (CoVeriTest program)
```

On successful execution a uniquely named folder is created in the folder `cvt-output`.
This folder contains 1) the artifacts produced during the execution of the actor, 
and 2) an xml file named `execution_trace.xml` containing the execution trace of the composition,
i.e., the resource measurements for atomic actors and paths to the artifacts produced.

In addition to this, a symbolic link named `lastexecution` pointing to the directory containing the artifacts
produced in the latest execution is also created.

### Atomic Actors
CoVeriTeam is based on using off-the-shelf verification and testing tools for cooperative verification
as atomic actors.
On its first execution, CoVeriTeam automatically downloads and unzips the archives that contain
the atomic actors used in the CoVeriTeam program.
The source URL is specified in the YAML atomic-actor definition.
The atomic actors that we use in the tutorial examples are available in the [actors/](actors/) folder.

`bin/coveriteam --tool-info <YAML actor-definition file>`
prints information (including name and version) about the actor defined in the YAML file.
This can be used to test if the atomic actor was successfully installed.
The script `smoke_test_all_tools.sh` prints the tool info for each actor defined in the `actors/` folder.

### Tutorial
The [examples/](examples/) folder contains a few example compositions that can
be executed on test inputs using the script [examples/run_examples.sh](examples/run_examples.sh).
A description is available on the [tutorial page](examples/README.md).

