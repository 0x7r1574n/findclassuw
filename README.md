# findclassuw

A simple script for grabbing information from University of Washington time schedule by year and quarter.

Optional arguments can filter meeting days/building/meeting time.

## Usage

    find_class_uw.py [-h] [-d DAYS] [-t TIME] [-b BUILDING] year quarter
	
    positional arguments:
        year                  4-digit academic year (e.g. 2015)
        quarter               first 3 letters of the quarter (e.g. SPR)
	
    optional arguments:
        -h, --help            show this help message and exit
        -d DAYS, --days DAYS  abbreviated meeting days (e.g. MWF)
        -t TIME, --time TIME  non-24hr meeting time interval/starting/ending time
  	                          (e.g. 1230-120 or 1230 or 120)
        -b BUILDING, --building BUILDING
  	                          abbreviated building code (e.g. KNE)
