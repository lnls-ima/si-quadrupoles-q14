#!/usr/bin/env python-sirius

import sys
from lnls.rotcoil import RotCoilMeas_SIQuadQ14Trim, MagnetsAnalysis


def multipole_trim(curr_main_coil):
    serials = ['003']

    # Load all data
    # data = MagnetsAnalysis(RotCoilMeas_SIQuadQ14, serials)
    data = MagnetsAnalysis(
        RotCoilMeas_SIQuadQ14Trim, serials, curr_main_coil=curr_main_coil)
    data.init()

    curr_str = str(curr_main_coil)

    # Print README Files
    # currents = data.tmpl.get_trim_currents('M1')
    currents, _ = data.tmpl.get_rampup('M1')
    idx0 = 16
    # idx0 = 0
    # currents = currents[idx0:6]      # 0A -> 10A
    # currents = currents[idx0:11]    # 10A -> 0A
    # currents = currents[idx0:16]   # 0A -> -10A
    currents = currents[idx0:]     # -10A -> 0A

    # idx0 = 5
    # currents = currents[idx0:16]    # 10A -> -10A
    # print(currents)
    stdout = sys.stdout
    for cidx in range(0, len(currents)):
        if abs(currents[cidx]) < 1:
            currents[cidx] = 0
        sys.stdout = open(
            'main_' + curr_str + 'A/README-{:.0f}A.md'.format(
                currents[cidx]), 'w')
        data.readme_print('M1', cidx+idx0)
        sys.stdout.flush()
    sys.stdout = stdout

    # Print Multipoles Files
    # currents, _ = data.tmpl.get_rampup('M1')
    # currents_down, _ = data.tmpl.get_rampdown('M1')
    stdout = sys.stdout
    for cidx in range(0, len(currents)):
        if abs(currents[cidx]) < 1:
            currents[cidx] = 0
        sys.stdout = open(
            'main_' + curr_str + 'A/up2MULTIPOLES-{:.0f}A.txt'.format(
                currents[cidx]), 'w')
        data.readme_multipoles_print('M1', cidx+idx0)
        sys.stdout.flush()
    sys.stdout = stdout


multipole_trim(curr_main_coil=60)
multipole_trim(curr_main_coil=80)
multipole_trim(curr_main_coil=95)
multipole_trim(curr_main_coil=110)
multipole_trim(curr_main_coil=120)
multipole_trim(curr_main_coil=140)
