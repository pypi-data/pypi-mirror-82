#!/usr/bin/env python
"""Is object in the list of ATLAS exposures?

Usage:
  %s <atlasCentresFile> <inputCoordsFile> 
  %s (-h | --help)
  %s --version

Options:
  -h --help                    Show this screen.
  --version                    Show version.


Example:
   %s atlas_coordinates.tst test_coordinates.tst

"""
import sys
__doc__ = __doc__ % (sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0])
from docopt import docopt
import os, MySQLdb, shutil, re
from generalutils import Struct, cleanOptions, readGenericDataFile, coords_sex_to_dec, bruteForceGenericConeSearch, isObjectInsideATLASFootprint

def main(argv = None):
    opts = docopt(__doc__, version='0.1')
    opts = cleanOptions(opts)

    # Use utils.Struct to convert the dict into an object for compatibility with old optparse code.
    options = Struct(**opts)

    print(options.atlasCentresFile)
    print(options.inputCoordsFile)

    atlasCentres = readGenericDataFile(options.atlasCentresFile, delimiter='\t')
    inputCoords = readGenericDataFile(options.inputCoordsFile, delimiter=',')

    for row in inputCoords:
        try:
            ra = float(row['ra'])
            dec = float(row['dec'])
        except ValueError as e:
            ra, dec = coords_sex_to_dec(row['ra'], row['dec'])

        #header, results = bruteForceGenericConeSearch(options.atlasCentresFile, [[ra, dec]], 7.71*3600.0, raIndex = 'ra_deg', decIndex = 'dec_deg')
        header, results = bruteForceGenericConeSearch(options.atlasCentresFile, [[ra, dec]], 20*3600.0, raIndex = 'ra_deg', decIndex = 'dec_deg')
        for r in results:
            print (r)

    # Alternatively - try a simple check to see which exposures our objects lie within.
    for row in inputCoords:
        try:
            ra = float(row['ra'])
            dec = float(row['dec'])
        except ValueError as e:
            ra, dec = coords_sex_to_dec(row['ra'], row['dec'])

        for r in atlasCentres:
            if isObjectInsideATLASFootprint(ra, dec, float(r['ra_deg']), float(r['dec_deg'])):
                print(row['name'], r['expname'])


        


if __name__=='__main__':
    main()
    
