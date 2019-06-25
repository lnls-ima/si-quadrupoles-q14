#!/usr/bin/env python-sirius
"""."""

import numpy as np
import matplotlib.pyplot as plt
from lnls import rotcoil as r



RotCoilMeas = r.RotCoilMeas_SIQuadQ14


qda = {
    'SI-01M2:MA-QDA': 'Q14-081',
    'SI-05M1:MA-QDA': 'Q14-077',
    'SI-05M2:MA-QDA': 'Q14-028',
    'SI-09M1:MA-QDA': 'Q14-059',
    'SI-09M2:MA-QDA': 'Q14-062',
    'SI-13M1:MA-QDA': 'Q14-058',
    'SI-13M2:MA-QDA': 'Q14-040',
    'SI-17M1:MA-QDA': 'Q14-034',
    'SI-17M2:MA-QDA': 'Q14-068',
    'SI-01M1:MA-QDA': 'Q14-018',
}

qdb1 = {
    'SI-02M1:MA-QDB1': 'Q14-010',
    'SI-02M2:MA-QDB1': 'Q14-017',
    'SI-04M1:MA-QDB1': 'Q14-011',
    'SI-04M2:MA-QDB1': 'Q14-008',
    'SI-06M1:MA-QDB1': 'Q14-023',
    'SI-06M2:MA-QDB1': 'Q14-035',
    'SI-08M1:MA-QDB1': 'Q14-048',
    'SI-08M2:MA-QDB1': 'Q14-075',
    'SI-10M1:MA-QDB1': 'Q14-021',
    'SI-10M2:MA-QDB1': 'Q14-055',
    'SI-12M1:MA-QDB1': 'Q14-014',
    'SI-12M2:MA-QDB1': 'Q14-033',
    'SI-14M1:MA-QDB1': 'Q14-026',
    'SI-14M2:MA-QDB1': 'Q14-067',
    'SI-16M1:MA-QDB1': 'Q14-057',
    'SI-16M2:MA-QDB1': 'Q14-027',
    'SI-18M1:MA-QDB1': 'Q14-079',
    'SI-18M2:MA-QDB1': 'Q14-009',
    'SI-20M1:MA-QDB1': 'Q14-025',
    'SI-20M2:MA-QDB1': 'Q14-053',
}

qdb2 = {
    'SI-02M1:MA-QDB2': 'Q14-039',
    'SI-02M2:MA-QDB2': 'Q14-050',
    'SI-04M1:MA-QDB2': 'Q14-038',
    'SI-04M2:MA-QDB2': 'Q14-020',
    'SI-06M1:MA-QDB2': 'Q14-045',
    'SI-06M2:MA-QDB2': 'Q14-047',
    'SI-08M1:MA-QDB2': 'Q14-064',
    'SI-08M2:MA-QDB2': 'Q14-046',
    'SI-10M1:MA-QDB2': 'Q14-032',
    'SI-10M2:MA-QDB2': 'Q14-030',
    'SI-12M1:MA-QDB2': 'Q14-065',
    'SI-12M2:MA-QDB2': 'Q14-056',
    'SI-14M1:MA-QDB2': 'Q14-049',
    'SI-14M2:MA-QDB2': 'Q14-054',
    'SI-16M1:MA-QDB2': 'Q14-063',
    'SI-16M2:MA-QDB2': 'Q14-004',
    'SI-18M1:MA-QDB2': 'Q14-015',
    'SI-18M2:MA-QDB2': 'Q14-066',
    'SI-20M1:MA-QDB2': 'Q14-060',
    'SI-20M2:MA-QDB2': 'Q14-052',
}

qdp1 = {
    'SI-03M1:MA-QDP1': 'Q14-069',
    'SI-03M2:MA-QDP1': 'Q14-072',
    'SI-07M1:MA-QDP1': 'Q14-019',
    'SI-07M2:MA-QDP1': 'Q14-031',
    'SI-11M1:MA-QDP1': 'Q14-041',
    'SI-11M2:MA-QDP1': 'Q14-070',
    'SI-15M1:MA-QDP1': 'Q14-051',
    'SI-15M2:MA-QDP1': 'Q14-042',
    'SI-19M1:MA-QDP1': 'Q14-029',
    'SI-19M2:MA-QDP1': 'Q14-061',
}

qdp2 = {
    'SI-03M1:MA-QDP2': 'Q14-012',
    'SI-03M2:MA-QDP2': 'Q14-005',
    'SI-07M1:MA-QDP2': 'Q14-078',
    'SI-07M2:MA-QDP2': 'Q14-071',
    'SI-11M1:MA-QDP2': 'Q14-007',
    'SI-11M2:MA-QDP2': 'Q14-006',
    'SI-15M1:MA-QDP2': 'Q14-073',
    'SI-15M2:MA-QDP2': 'Q14-016',
    'SI-19M1:MA-QDP2': 'Q14-037',
    'SI-19M2:MA-QDP2': 'Q14-002',
}


def select_dataset(serial):
    """."""
    data = RotCoilMeas(serial)
    maxc_idx = data.get_max_current_index()
    data = data.get_data_set_measurements('M1')
    return data[maxc_idx]


def get_serials(magnet_family):
    """."""
    serials = []
    for magnet in magnet_family:
        serial = magnet_family[magnet]
        serials.append(serial.replace('Q14-', ''))
    return serials


def get_analysis_data(family):
    """."""
    serials = get_serials(family)
    current = []
    xcenter = []
    ycenter = []
    quadrupole = []
    roterror = []
    for serial in serials:
        data = select_dataset(serial)
        c = data.main_coil_current_avg
        h = data.harmonics
        main_idx = h.index(RotCoilMeas.main_harmonic)
        x = data.magnetic_center_x
        y = data.magnetic_center_y
        n = data.intmpole_normal_avg[main_idx]
        s = data.intmpole_skew_avg[main_idx]
        e = data.rotation_error
        current.append(c)
        xcenter.append(x)
        ycenter.append(y)
        quadrupole.append(n)
        roterror.append(e)
        sfmt = '{}  {:.3f} A  {:+.4f} T  {:+5.1f} um  {:+5.1f} um  {:06.3f}'
        print(sfmt.format(serial, c, n, x, y, e))

    q = np.array(quadrupole)
    m, s, maxmin = np.mean(q), np.std(q), np.max(q) - np.min(q)
    print('- integrated quadrupole [T]: {:+.4f} ± {:.4f} ({:.3f} %), maxmin: {:.4f} ({:.3f} %)'.format(m, s, 100*s/m, maxmin, 100*maxmin/m))
    x = np.array(xcenter)
    m, s, maxmin = np.mean(x), np.std(x), np.max(x) - np.min(x)
    print('- xcenter [um]:               {:+.1f} ± {:.1f}, maxmin: {:.1f}'.format(m, s, maxmin))
    y = np.array(ycenter)
    m, s, maxmin = np.mean(y), np.std(y), np.max(y) - np.min(y)
    print('- ycenter [um]:               {:+.1f} ± {:.1f}, maxmin: {:.1f}'.format(m, s, maxmin))
    e = np.array(roterror)
    m, s, maxmin = np.mean(e), np.std(e), np.max(e) - np.min(e)
    print('- rotation error [mrad]:      {:+.1f} ± {:.1f}, maxmin: {:.1f} '.format(m, s, maxmin))
    print('')
    return serials, current, quadrupole, xcenter, ycenter, roterror



fams = [qda, qdb1, qdb2, qdp1, qdp2]



def plot_integrated_quadrupole():
    """."""

    n = 0
    serials = []

    label = 'QDA'
    print(label)
    serials0, current0, quadrupole0, xcenter0, ycenter0, roterror0 = \
        get_analysis_data(fams[0])
    plt.plot(len(serials) + np.arange(len(serials0)), quadrupole0, 'b-')
    plt.plot(len(serials) + np.arange(len(serials0)), quadrupole0, 'bo', label=label)
    avg0 = np.mean(quadrupole0)
    plt.plot(len(serials) + np.arange(len(serials0)),
            [avg0, ]*len(quadrupole0), '--b')
    serials += serials0

    label = 'QDB1'
    print(label)
    serials1, current1, quadrupole1, xcenter1, ycenter1, roterror1 = \
        get_analysis_data(fams[1])
    plt.plot(len(serials) + np.arange(len(serials1)), quadrupole1, 'g-')
    plt.plot(len(serials) + np.arange(len(serials1)), quadrupole1, 'go', label=label)
    avg1 = np.mean(quadrupole1)
    plt.plot(len(serials) + np.arange(len(serials1)),
            [avg1, ]*len(quadrupole1), '--g')
    serials += serials1

    label = 'QDB2'
    print(label)
    serials2, current2, quadrupole2, xcenter2, ycenter2, roterror2 = \
        get_analysis_data(fams[2])
    plt.plot(len(serials) + np.arange(len(serials2)), quadrupole2, 'r-')
    plt.plot(len(serials) + np.arange(len(serials2)),
             quadrupole2, 'ro', label=label)
    avg2 = np.mean(quadrupole2)
    plt.plot(len(serials) + np.arange(len(serials2)),
            [avg2, ]*len(quadrupole2), '--r')
    serials += serials2

    label = 'QDP1'
    print(label)
    serials3, current3, quadrupole3, xcenter3, ycenter3, roterror3 = \
        get_analysis_data(fams[3])
    plt.plot(len(serials) + np.arange(len(serials3)), quadrupole3, 'k-')
    plt.plot(len(serials) + np.arange(len(serials3)),
             quadrupole3, 'ko', label=label)
    avg3 = np.mean(quadrupole3)
    plt.plot(len(serials) + np.arange(len(serials3)),
            [avg3, ]*len(quadrupole3), '--k')
    serials += serials3

    label = 'QDP2'
    print(label)
    serials4, current4, quadrupole4, xcenter4, ycenter4, roterror4 = \
        get_analysis_data(fams[4])
    plt.plot(len(serials) + np.arange(len(serials4)), quadrupole4, 'y-')
    plt.plot(len(serials) + np.arange(len(serials4)),
             quadrupole4, 'yo', label=label)
    avg4 = np.mean(quadrupole4)
    plt.plot(len(serials) + np.arange(len(serials4)),
            [avg4, ]*len(quadrupole4), '--y')
    serials += serials4


    plt.xlabel('Serial Number')
    plt.ylabel('Integrated Quadrupole [T]')
    plt.title('Q14 Integrated Quadrupoles ({:+.2f} A)'.format(np.mean(current0)))
    plt.xticks(np.arange(len(serials)), serials, rotation='vertical')
    plt.legend()
    plt.grid()
    plt.show()


def plot_xcenter():
    """."""

    n = 0
    serials = []

    label = 'QDA'
    print(label)
    serials0, current0, quadrupole0, xcenter0, ycenter0, roterror0 = \
        get_analysis_data(fams[0])
    plt.plot(len(serials) + np.arange(len(serials0)), xcenter0, 'b-')
    plt.plot(len(serials) + np.arange(len(serials0)),
             xcenter0, 'bo', label=label)
    avg0 = np.mean(xcenter0)
    plt.plot(len(serials) + np.arange(len(serials0)),
             [avg0, ]*len(xcenter0), '--b')
    serials += serials0

    label = 'QDB1'
    print(label)
    serials1, current1, quadrupole1, xcenter1, ycenter1, roterror1 = \
        get_analysis_data(fams[1])
    plt.plot(len(serials) + np.arange(len(serials1)), xcenter1, 'g-')
    plt.plot(len(serials) + np.arange(len(serials1)),
             xcenter1, 'go', label=label)
    avg1 = np.mean(xcenter1)
    plt.plot(len(serials) + np.arange(len(serials1)),
             [avg1, ]*len(xcenter1), '--g')
    serials += serials1

    label = 'QDB2'
    print(label)
    serials2, current2, quadrupole2, xcenter2, ycenter2, roterror2 = \
        get_analysis_data(fams[2])
    plt.plot(len(serials) + np.arange(len(serials2)), xcenter2, 'r-')
    plt.plot(len(serials) + np.arange(len(serials2)),
             xcenter2, 'ro', label=label)
    avg2 = np.mean(xcenter2)
    plt.plot(len(serials) + np.arange(len(serials2)),
             [avg2, ]*len(xcenter2), '--r')
    serials += serials2

    label = 'QDP1'
    print(label)
    serials3, current3, quadrupole3, xcenter3, ycenter3, roterror3 = \
        get_analysis_data(fams[3])
    plt.plot(len(serials) + np.arange(len(serials3)), xcenter3, 'k-')
    plt.plot(len(serials) + np.arange(len(serials3)),
             xcenter3, 'ko', label=label)
    avg3 = np.mean(xcenter3)
    plt.plot(len(serials) + np.arange(len(serials3)),
             [avg3, ]*len(xcenter3), '--k')
    serials += serials3

    label = 'QDP2'
    print(label)
    serials4, current4, quadrupole4, xcenter4, ycenter4, roterror4 = \
        get_analysis_data(fams[4])
    plt.plot(len(serials) + np.arange(len(serials4)), xcenter4, 'y-')
    plt.plot(len(serials) + np.arange(len(serials4)),
             xcenter4, 'yo', label=label)
    avg4 = np.mean(xcenter4)
    plt.plot(len(serials) + np.arange(len(serials4)),
             [avg4, ]*len(xcenter4), '--y')
    serials += serials4

    plt.xlabel('Serial Number')
    plt.ylabel('Magnetic Center [um]')
    plt.title(
        'Q14 Horizontal Magnetic Center ({:+.2f} A)'.format(np.mean(current0)))
    plt.xticks(np.arange(len(serials)), serials, rotation='vertical')
    plt.legend()
    plt.grid()
    plt.show()


def plot_ycenter():
    """."""

    n = 0
    serials = []

    label = 'QDA'
    print(label)
    serials0, current0, quadrupole0, xcenter0, ycenter0, roterror0 = \
        get_analysis_data(fams[0])
    plt.plot(len(serials) + np.arange(len(serials0)), ycenter0, 'b-')
    plt.plot(len(serials) + np.arange(len(serials0)),
             ycenter0, 'bo', label=label)
    avg0 = np.mean(ycenter0)
    plt.plot(len(serials) + np.arange(len(serials0)),
             [avg0, ]*len(ycenter0), '--b')
    serials += serials0

    label = 'QDB1'
    print(label)
    serials1, current1, quadrupole1, xcenter1, ycenter1, roterror1 = \
        get_analysis_data(fams[1])
    plt.plot(len(serials) + np.arange(len(serials1)), ycenter1, 'g-')
    plt.plot(len(serials) + np.arange(len(serials1)),
             ycenter1, 'go', label=label)
    avg1 = np.mean(ycenter1)
    plt.plot(len(serials) + np.arange(len(serials1)),
             [avg1, ]*len(ycenter1), '--g')
    serials += serials1

    label = 'QDB2'
    print(label)
    serials2, current2, quadrupole2, xcenter2, ycenter2, roterror2 = \
        get_analysis_data(fams[2])
    plt.plot(len(serials) + np.arange(len(serials2)), ycenter2, 'r-')
    plt.plot(len(serials) + np.arange(len(serials2)),
             ycenter2, 'ro', label=label)
    avg2 = np.mean(ycenter2)
    plt.plot(len(serials) + np.arange(len(serials2)),
             [avg2, ]*len(ycenter2), '--r')
    serials += serials2

    label = 'QDP1'
    print(label)
    serials3, current3, quadrupole3, xcenter3, ycenter3, roterror3 = \
        get_analysis_data(fams[3])
    plt.plot(len(serials) + np.arange(len(serials3)), ycenter3, 'k-')
    plt.plot(len(serials) + np.arange(len(serials3)),
             ycenter3, 'ko', label=label)
    avg3 = np.mean(ycenter3)
    plt.plot(len(serials) + np.arange(len(serials3)),
             [avg3, ]*len(ycenter3), '--k')
    serials += serials3

    label = 'QDP2'
    print(label)
    serials4, current4, quadrupole4, xcenter4, ycenter4, roterror4 = \
        get_analysis_data(fams[4])
    plt.plot(len(serials) + np.arange(len(serials4)), ycenter4, 'y-')
    plt.plot(len(serials) + np.arange(len(serials4)),
             ycenter4, 'yo', label=label)
    avg4 = np.mean(ycenter4)
    plt.plot(len(serials) + np.arange(len(serials4)),
             [avg4, ]*len(ycenter4), '--y')
    serials += serials4

    plt.xlabel('Serial Number')
    plt.ylabel('Magnetic Center [um]')
    plt.title(
        'Q14 Vertical Magnetic Center ({:+.2f} A)'.format(np.mean(current0)))
    plt.xticks(np.arange(len(serials)), serials, rotation='vertical')
    plt.legend()
    plt.grid()
    plt.show()


def plot_roterror():
    """."""

    n = 0
    serials = []

    label = 'QDA'
    print(label)
    serials0, current0, quadrupole0, xcenter0, ycenter0, roterror0 = \
        get_analysis_data(fams[0])
    plt.plot(len(serials) + np.arange(len(serials0)), roterror0, 'b-')
    plt.plot(len(serials) + np.arange(len(serials0)),
             roterror0, 'bo', label=label)
    avg0 = np.mean(roterror0)
    plt.plot(len(serials) + np.arange(len(serials0)),
             [avg0, ]*len(roterror0), '--b')
    serials += serials0

    label = 'QDB1'
    print(label)
    serials1, current1, quadrupole1, xcenter1, ycenter1, roterror1 = \
        get_analysis_data(fams[1])
    plt.plot(len(serials) + np.arange(len(serials1)), roterror1, 'g-')
    plt.plot(len(serials) + np.arange(len(serials1)),
             roterror1, 'go', label=label)
    avg1 = np.mean(roterror1)
    plt.plot(len(serials) + np.arange(len(serials1)),
             [avg1, ]*len(roterror1), '--g')
    serials += serials1

    label = 'QDB2'
    print(label)
    serials2, current2, quadrupole2, xcenter2, ycenter2, roterror2 = \
        get_analysis_data(fams[2])
    plt.plot(len(serials) + np.arange(len(serials2)), roterror2, 'r-')
    plt.plot(len(serials) + np.arange(len(serials2)),
             roterror2, 'ro', label=label)
    avg2 = np.mean(roterror2)
    plt.plot(len(serials) + np.arange(len(serials2)),
             [avg2, ]*len(roterror2), '--r')
    serials += serials2

    label = 'QDP1'
    print(label)
    serials3, current3, quadrupole3, xcenter3, ycenter3, roterror3 = \
        get_analysis_data(fams[3])
    plt.plot(len(serials) + np.arange(len(serials3)), roterror3, 'k-')
    plt.plot(len(serials) + np.arange(len(serials3)),
             roterror3, 'ko', label=label)
    avg3 = np.mean(roterror3)
    plt.plot(len(serials) + np.arange(len(serials3)),
             [avg3, ]*len(roterror3), '--k')
    serials += serials3

    label = 'QDP2'
    print(label)
    serials4, current4, quadrupole4, xcenter4, ycenter4, roterror4 = \
        get_analysis_data(fams[4])
    plt.plot(len(serials) + np.arange(len(serials4)), roterror4, 'y-')
    plt.plot(len(serials) + np.arange(len(serials4)),
             roterror4, 'yo', label=label)
    avg4 = np.mean(roterror4)
    plt.plot(len(serials) + np.arange(len(serials4)),
             [avg4, ]*len(roterror4), '--y')
    serials += serials4

    plt.xlabel('Serial Number')
    plt.ylabel('Roll error [mrad]')
    plt.title(
        'Q14 Rotation Error ({:+.2f} A)'.format(np.mean(current0)))
    plt.xticks(np.arange(len(serials)), serials, rotation='vertical')
    plt.legend()
    plt.grid()
    plt.show()



plot_integrated_quadrupole()
plot_xcenter()
plot_ycenter()
plot_roterror()
