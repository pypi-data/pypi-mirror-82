// This file is redistributed as part of CoVeriTeam, a tool for on-demand composition of cooperative verification systems:
// https://gitlab.com/sosy-lab/software/coveriteam
//
// This file has been taken from the sv-benchmarks repository: https://github.com/sosy-lab/sv-benchmarks
//
// SPDX-FileCopyrightText: 2008-2020 SV-Benchmarks community
//
// SPDX-License-Identifier: Apache-2.0

extern void __VERIFIER_error(void);
extern void abort(void); 
void assume_abort_if_not(int cond) { 
  if(!cond) {abort();}
}
void __VERIFIER_assert(int cond) {
  if (!(cond)) {
      ERROR: __VERIFIER_error();
  }
  return;
}
int __VERIFIER_nondet_int();
int main() {
    int x,y,z,w;
    x = y = z = w = 0;
    while (__VERIFIER_nondet_int() && y < 10000) {
 if (__VERIFIER_nondet_int()) {
     x = x + 1;
     y = y + 100;
 } else if (__VERIFIER_nondet_int()) {
     if (x >= 4) {
  x = x + 1;
  y = y + 1;
     }
 } else if (y > 10*w && z >= 100*x) {
     y = -y;
 }
 w = w + 1;
 z = z + 10;
    }
    __VERIFIER_assert(x >= 4 && y <= 2);
    return 0;
}
