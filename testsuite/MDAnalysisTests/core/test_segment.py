# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8
#
# MDAnalysis --- http://www.mdanalysis.org
# Copyright (c) 2006-2017 The MDAnalysis Development Team and contributors
# (see the file AUTHORS for the full list of names)
#
# Released under the GNU Public Licence, v2 or any higher version
#
# Please cite your use of MDAnalysis in published work:
#
# R. J. Gowers, M. Linke, J. Barnoud, T. J. E. Reddy, M. N. Melo, S. L. Seyler,
# D. L. Dotson, J. Domanski, S. Buchoux, I. M. Kenney, and O. Beckstein.
# MDAnalysis: A Python package for the rapid analysis of molecular dynamics
# simulations. In S. Benthall and S. Rostrup editors, Proceedings of the 15th
# Python in Science Conference, pages 102-109, Austin, TX, 2016. SciPy.
#
# N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and O. Beckstein.
# MDAnalysis: A Toolkit for the Analysis of Molecular Dynamics Simulations.
# J. Comput. Chem. 32 (2011), 2319--2327, doi:10.1002/jcc.21787
#
from __future__ import absolute_import

from unittest import TestCase

from numpy.testing import (
    dec,
    assert_,
    assert_equal,
)
import pytest

import MDAnalysis as mda
from MDAnalysis.core.dummy import make_Universe

from MDAnalysisTests import parser_not_found
from MDAnalysis.tests.datafiles import PSF, DCD


class TestSegment(TestCase):
    def setUp(self):
        self.universe = make_Universe(('segids',))
        self.sB = self.universe.segments[1]

    def test_type(self):
        assert_(isinstance(self.sB, mda.core.groups.Segment))
        assert_equal(self.sB.segid, "SegB")

    def test_index(self):
        s = self.sB
        res = s.residues[3]
        assert_(isinstance(res, mda.core.groups.Residue))

    def test_slicing(self):
        res = self.sB.residues[:3]
        assert_equal(len(res), 3)
        assert_(isinstance(res, mda.core.groups.ResidueGroup))

    def test_advanced_slicing(self):
        res = self.sB.residues[[2, 1, 0, 2]]
        assert_equal(len(res), 4)
        assert_(isinstance(res, mda.core.groups.ResidueGroup))

    def test_atom_order(self):
        assert_equal(self.universe.segments[0].atoms.indices,
                     sorted(self.universe.segments[0].atoms.indices))

@pytest.mark.skipif(parser_not_found('DCD'),
            reason='DCD parser not available. Are you using python 3?')
def test_generated_residueselection():
    """Test that a generated residue group always returns a ResidueGroup (Issue 47)
    unless there is a single residue (Issue 363 change)"""
    universe = mda.Universe(PSF, DCD)
    # only a single Cys in AdK
    cys = universe.s4AKE.CYS
    assert_(isinstance(cys, mda.core.groups.Residue),
            "Single Cys77 is NOT returned as a single Residue (Issue 47)")

    # multiple Met
    met = universe.s4AKE.MET
    assert_(isinstance(met, mda.core.groups.ResidueGroup),
            "Met selection does not return a ResidueGroup")

    del universe


