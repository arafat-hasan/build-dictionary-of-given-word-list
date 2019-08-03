#!/usr/bin/env python3
#
# FILE: main.py
#
# @author: Arafat Hasan Jenin <opendoor.arafat[at]gmail[dot]com>
#
# LINK:
#
# DATE CREATED: 22-07-19 22:49:59 (+06)
# LAST MODIFIED: 22-07-19 22:50:05 (+06)
#
# DEVELOPMENT HISTORY:
# Date         Version     Description
# --------------------------------------------------------------------
# 22-07-19     1.0         Deleted code is debugged code.
#
#               _/  _/_/_/_/  _/      _/  _/_/_/  _/      _/
#              _/  _/        _/_/    _/    _/    _/_/    _/
#             _/  _/_/_/    _/  _/  _/    _/    _/  _/  _/
#      _/    _/  _/        _/    _/_/    _/    _/    _/_/
#       _/_/    _/_/_/_/  _/      _/  _/_/_/  _/      _/
#
##############################################################################

import requests
import json
import sys
import io
import csv
import time
from requests.exceptions import Timeout

startTime = time.time()
try:
    jsonFileRead = io.open("dic.json", mode='r', encoding='utf-8')
except FileNotFoundError:
    fileData = {}
else:
    try:
        fileData = json.load(jsonFileRead)
    except json.decoder.JSONDecodeError:
        fileData = {}
        jsonFileRead.close()
    else:
        jsonFileRead.close()


def processWord(eng, ben, prep, example):
    if eng in fileData:
        for entry in fileData[eng]:
            if ben is not entry.get('bengali', ""):
                if ben:
                    entry.update({'bengali': ben})
                else:
                    del entry['bengali']
            if prep is not entry.get('prep', ""):
                if prep:
                    entry.update({'prep': prep})
                else:
                    del entry['prep']
            if example is not entry.get('example', ""):
                if example:
                    entry.update({'example': example})
                else:
                    del entry['example']
        return 0

    url = 'https://googledictionaryapi.eu-gb.mybluemix.net/'
    params = dict(define=eng)

    try:
        resp = requests.get(url=url, params=params, timeout=7)

    except Timeout:
        return 100
    else:
        if resp.status_code == 404:
            # print("Error! Word not found\nResponse code: %d\n"  % resp.status_code)
            entries = [{'word': eng, 'bengali': ben, 'prep': prep,
                    'example': example}]
            fileData.update({eng: entries})
            return 0

        elif resp.status_code != requests.codes.ok:
            return 4

        entries = resp.json()
        for entry in entries:
            if ben: entry.update({'bengali': ben})
            if prep: entry.update({'prep': prep})
            if example: entry.update({'example': example})
        fileData.update({entries[0]['word']: entries})
        return 0
    return 0



def main():

    with open('words.csv') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        lineCount = 0
        unmanagedWord = 0
        for row in csvReader:
            if lineCount == 0:
                lineCount += 1
            else:
                lineCount += 1
                if len(row) < 1:
                    continue
                ret = processWord(row[0], row[1], row[2], row[3])
                if ret == 100:
                    print("Request timed out")
                    print("Check internet connection")
                    break
                elif ret == 4:
                    unmanagedWord = unmanagedWord + 1
            sys.stdout.write("\r%d lines processed so far..." % lineCount)
            sys.stdout.flush()
        print(f'\nProcessed {lineCount} lines total, %d word(s) not processed\n'
                % unmanagedWord)


        with io.open("dic.json", mode='w+', encoding='utf-8') as jsonFile:
            json.dump(fileData, jsonFile, ensure_ascii=False, indent=4, sort_keys=True)
        jsonFile.close()

    print("Process Completed\n")
    print("--- %s seconds ---" % (time.time() - startTime))

if __name__ == '__main__':
    main()


