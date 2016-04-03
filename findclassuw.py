#
# findclassuw.py
#   A simple script for grabbing information from University of Washington time schedule by year and quarter.
#   Optional arguments can filter meeting days/building/meeting time.
#
# Copyright (c) 2016 Cechi Shi <cechishi@uw.edu>
#
# examples:
#   python findclassuw.py -d MWF -t 1230-120 -b KNE 2016 SPR
#   python findclassuw.py -days MWF -time 1230-120 -building KNE 2016 SPR
#   python findclassuw.py -t 120 -b KNE 2016 SPR
#   python findclassuw.py -d M -t 1230 2016 SPR
#   python findclassuw.py 2016 SPR
#

from bs4 import BeautifulSoup
import requests
import argparse

__author__ = 'cechishi@uw.edu'

BASE_URL = "http://www.washington.edu/students/timeschd/"


def fetch_program_urls(year, quarter):
    program_urls = set()
    url = BASE_URL + quarter + year
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.select('li > a'):
        a = str(link.get('href'))
        # remove id and social links
        if not (a.startswith('http') or a.startswith('/') or a.startswith('#')):
            program_urls.add(url + '/' + a)

    return program_urls


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("year", help="4-digit academic year (e.g. 2015)")
    parser.add_argument("quarter", help="first 3 letters of the quarter (e.g. SPR)")
    parser.add_argument("-d", "--days", help="abbreviated meeting days (e.g. MWF)")
    parser.add_argument("-t", "--time",
                        help="non-24hr meeting time interval/starting/ending time (e.g. 1230-120 or 1230 or 120)")
    parser.add_argument("-b", "--building", help="abbreviated building code (e.g. KNE)")

    arguments = parser.parse_args()

    return arguments


def print_result(course, url):
    print(" ".join(course))
    print(url+'\n\n')  # formatting


def search(url, days, building, time):
    response = requests.get(url=url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        courses = soup.select('tr > td > pre')
        if len(courses) != 0:
            del courses[0]  # remove table headers
            for course in courses:
                parts = course.text.split()
                if time:
                    time_node = ""
                    for part in parts:
                        if "-" in part:
                            time_node = part
                            break
                    if building and days:
                        if (building.upper() in parts) and (time in time_node) and (days in parts):
                            print_result(parts, url)
                    elif building and not days:
                        if (building.upper() in parts) and (time in time_node):
                            print_result(parts, url)
                    elif days and not building:
                        if (days in parts) and (time in time_node):
                            print_result(parts, url)
                    else:
                        if time in time_node:
                            print_result(parts, url)
                elif days:
                    if building:
                        if (days in parts) and (building.upper() in parts):
                            print_result(parts, url)
                    else:
                        if days in parts:
                            print_result(parts, url)
                elif building:
                    if building.upper() in parts:
                        print_result(parts, url)
                else:
                    print_result(parts, url)


if __name__ == '__main__':
    args = parse_args()
    y = args.year
    q = args.quarter
    d = args.days
    b = args.building
    t = args.time

    urls = fetch_program_urls(y, q.upper())
    for u in urls:
        search(u, d, b, t)
