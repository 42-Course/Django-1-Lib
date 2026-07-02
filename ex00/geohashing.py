#!/usr/bin/python3
import sys
import antigravity


def geohashing(latitude, longitude, datedow):
    """Compute and print a geohash using xkcd's Munroe algorithm.

    antigravity.geohash does the heavy lifting (and the printing).
    """
    antigravity.geohash(latitude, longitude, datedow)


if __name__ == '__main__':
    try:
        # Expected: latitude longitude date djia
        #   ex: ./geohashing.py 37.421542 -122.085589 2005-05-26 10458.68
        if len(sys.argv) != 5:
            raise ValueError("usage: geohashing.py <lat> <lon> <date> <djia>")
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
        date = sys.argv[3]
        djia = sys.argv[4]
        datedow = "{}-{}".format(date, djia).encode('utf-8')
        geohashing(latitude, longitude, datedow)
    except Exception as error:
        print("Error: {}".format(error), file=sys.stderr)
        sys.exit(1)
