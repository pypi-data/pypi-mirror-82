<!--
This file is part of CoVeriTeam,
a tool for on-demand composition of cooperative verification systems:
https://gitlab.com/sosy-lab/software/coveriteam

SPDX-FileCopyrightText: 2020 Dirk Beyer <https://www.sosy-lab.org>

SPDX-License-Identifier: Apache-2.0
-->

## CoVeriTeam 0.5
* Added actor definitions for the verifiers from software verification competition 2020
* Renamed the folder containing actor definitions from config to actors

## CoVeriTeam 0.4
* Execution with [BencheExec](https://github.com/sosy-lab/benchexec)
* MetaVal implemented using CoVeriTeam
* Template for input artifacts in the actorsuration YAML file.

## CoVeriTeam 0.3
* New Actors:
  1. algorithm selection actor,
  2. dynamic (or lazy) actor which instantiates the concrete actor during runtime based on an actor definition.
* Grammar:
  1. support for print statement
  2. unicode characters in comments.
* YAML: support for include in yaml files.
* Tool Info module can now be also provided by a url.

## CoVeriTeam 0.2
* New formal for YAML file
* setting up PyPi release

## CoVeriTeam 0.1
Initial version of CoVeriTeam as available on Zenodo: https://doi.org/10.5281/zenodo.3818283
