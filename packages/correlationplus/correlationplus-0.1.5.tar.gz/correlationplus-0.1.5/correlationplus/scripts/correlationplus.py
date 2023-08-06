###############################################################################
# correlationplus - A Python package to calculate, visualize and analyze      #
#                    dynamical correlations maps of proteins.                 #
# Authors: Mustafa Tekpinar                                                   #
# Copyright Mustafa Tekpinar 2017-2018                                        #
# Copyright CNRS-UMR3528, 2019                                                #
# Copyright Institut Pasteur Paris, 2020                                      #
#                                                                             #
# This file is part of correlationplus.                                       #
#                                                                             #
# correlationplus is free software: you can redistribute it and/or modify     #
# it under the terms of the GNU Lesser General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# correlationplus is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU LESSER General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the GNU Lesser General Public License    #
# along with correlationplus.  If not, see <https://www.gnu.org/licenses/>.   #
###############################################################################

import sys

# cannot use relative imports
# as it does not work in tests/run_test
# ImportError: attempted relative import with no known parent package
from correlationplus.scripts.calculate import calculateApp
from correlationplus.scripts.visualizemap import visualizemapApp
from correlationplus.scripts.diffMap import diffMapApp
from correlationplus.scripts.centralAnalysis import centralityAnalysisApp

#TODO:
# There are a bunch of things one can add to this script:
# 1-Plot nDCC maps or normalized linear mutual information maps!: Done!
# 2-Project (high) correlations onto PDB structure.
#   a) as a Pymol script output
#   b) as a VMD script output: Done!
# 3-Project secondary structures on x and y axes of a correlation map.
# 4-Difference maps: Done!
# 5-Combining two correlation plots as upper triangle and lower triangle.
# 6-Filter correlations lower than a certain (absolute) value.: Done!
# 7-Filter correlations for residues that are very close.: Done!
# 8-Add centrality calculations: Done
# 9-Add centrality visualizations: Done


def usage_main():
    """
    Show how to use this program!
    """
    print("""
Example usage:

correlationplus -h

CorrelationPlus contains four analysis apps:
 - calculate
 - visualizemap
 - diffMap
 - centralityAnalysis

You can get more information about each individual app as follows:

correlationplus centralityAnalysis -h
""")


def main():

    print("""

|------------------------------Correlation Plus------------------------------|
|                                                                            |
|        A Python package to calculate, visualize and analyze protein        |
|                           correlation maps.                                |
|                   Copyright Mustafa Tekpinar 2017-2018                     |
|                   Copyright CNRS-UMR3528, 2019                             |
|                   Copyright Institut Pasteur Paris, 2020                   |
|                         Author Mustafa Tekpinar                            |
|                       Email: tekpinar@buffalo.edu                          |
|                          Licence: GNU Lesser GPL                           |
|--------------------------------------------------------------------------- |

""")

    if len(sys.argv) > 1:
        if sys.argv[1] == "calculate":
            calculateApp()
        elif sys.argv[1] == "visualizemap":
            visualizemapApp()
        elif sys.argv[1] == "diffMap":
            diffMapApp()
        elif sys.argv[1] == "centralityAnalysis":
            centralityAnalysisApp()
        elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
            usage_main()
        else:
            usage_main()
            sys.exit(-1)
    else:
        usage_main()
        sys.exit(-1)


if __name__ == "__main__":
    main()
