#!/usr/bin/env python3
#
# FILE: main.py
#
# @author: Arafat Hasan Jenin <opendoor.arafat[at]gmail[dot]com>
#
# LINK: https://github.com/arafat-hasan/build-dictionary-of-given-word-list/
#
# DATE CREATED: 22-07-19 22:49:59 (+06)
# LAST MODIFIED: 04-08-19 17:43:37 (+06)
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

from pylatex import Document, Section, Subsection, Command, UnsafeCommand, \
        PageStyle, Head, MiniPage, Foot, LargeText, MediumText, LineBreak, \
        simple_page_number
from pylatex.utils import italic, NoEscape, bold
from pylatex.package import Package
from pylatex.base_classes import Environment, CommandBase, Arguments

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
            fileData.update({eng.lower(): entries})
            return 0

        elif resp.status_code != requests.codes.ok:
            return 4

        entries = resp.json()
        for entry in entries:
            if ben: entry.update({'bengali': ben})
            if prep: entry.update({'prep': prep})
            if example: entry.update({'example': example})
        fileData.update({entries[0]['word'].lower(): entries})
        return 0
    return 0

def processLaTex():
    geometry_options = {"top":"2.3cm","bottom":"2.0cm", "left":"2.5cm",\
            "right":"2.0cm", "columnsep":"20pt"}
    doc = Document('basic', geometry_options=geometry_options)
    first_page = PageStyle("firstpage")
    doc.documentclass = Command(
            'documentclass',
            options=['10pt', 'a4paper', 'twoside'],
            arguments=['article'],
            )

    doc.packages.append(Package('palatino'))
    doc.packages.append(Package('microtype'))
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('fontspec'))
    doc.packages.append(Package('enumitem'))
    doc.packages.append(Package('titlesec', NoEscape('bf, sf, center')))
    doc.packages.append(Package('fancyhdr'))



    doc.preamble.append(Command('fancyhead', \
            NoEscape(r'\textsf{\rightmark}'), 'L'))
    doc.preamble.append(Command('fancyhead', \
            NoEscape(r'\textsf{\leftmark}'), 'R'))


    doc.preamble.append(Command('renewcommand', \
        arguments=Arguments(NoEscape(r'\headrulewidth'), '1.4pt')))

    doc.preamble.append(Command('fancyfoot', \
            NoEscape(r'\textbf{\textsf{\thepage}}'), 'C'))

    doc.preamble.append(Command('renewcommand', \
        arguments=Arguments(NoEscape(r'\footrulewidth'), '1.4pt')))

    doc.preamble.append(Command('pagestyle', 'fancy'))

    new_comm = UnsafeCommand('newcommand', '\entry', options=4, \
    # extra_arguments=NoEscape(r'\textbf{#1}\markboth{#1}{#1}\ {(#2)}\ \textit{#3}\  \ {#4}'))
        extra_arguments=NoEscape(r'\textbf{#1}\markboth{#1}{#1}\ {{\fontspec{Doulos SIL} #2}}\  {{\fontspec{Kalpurush} #3}}\ $\bullet$\ {#4}'))
    doc.append(new_comm)


    # print(type(fileData))
    entriesList = list(fileData.keys())
    entriesList.sort()

    doc.append(NoEscape(r'\begin{multicols}{2}'))

    for item in entriesList:
        entryList = fileData[item]
        for entry in entryList:
           word         = entry.get('word',"")
           bengali      = entry.get('bengali',"")
           prep         = entry.get('prep',"")
           ownExample   = entry.get('example',"")
           origin       = entry.get('origin',"")
           phonetic     = entry.get('phonetic',"")
           meaning      = entry.get('meaning',{})

           partsOfSpeech = list(meaning.keys())

           partStr = ""
           
           for part in partsOfSpeech:
               onepart     = meaning[part]
               deffCnt = 0
               strGen = "\\textsf{" + part + "}"
               for deff in onepart:
                   deffCnt = deffCnt + 1
                   definition  = deff.get('definition',"")
                   example     = deff.get('example',"")
                   synonyms    = deff.get('synonyms',"")
                   # print(word, part, definition)
                   # print(u', '.join((word, phonetic, part, definition)).encode('utf-8').strip())
                   # print("#############################")
                   # print(u''.join((lorem)).encode('utf-8').strip())
                   # doc.append(u', '.join((word, phonetic, part, definition)).encode('utf-8').strip())
                   # lorem.replace("&", "\&")
                   strGen = strGen + " \\textbf{" + str(deffCnt) + "} " + definition + " {\\fontspec{Times New Roman}◇} " + "\\textit{" + example + "}"

               partStr = partStr + " " + strGen

           lorem = "\entry{"+word+"}{"+phonetic+"}{"+bengali+"}{"+partStr+"}"
           doc.append(NoEscape(lorem))
           doc.append(NoEscape(r'\par'))
               


    print("******************************************************")
    # doc.append(NoEscape(r'\section*{A}'))
    # doc.append(NoEscape(r'test'))
    doc.append(NoEscape(r'\end{multicols}'))
    doc.generate_pdf(clean_tex=False, compiler='xelatex')
    doc.generate_tex()

    tex = doc.dumps()  # The from pylatex.utils import italic, NoEscapedocument as string in LaTeX syntax





def main():

    # with open('words.csv') as csvFile:
    #     csvReader = csv.reader(csvFile, delimiter=',')
    #     lineCount = 0
    #     unmanagedWord = 0
    #     for row in csvReader:
    #         if lineCount == 0:
    #             lineCount += 1
    #         else:
    #             lineCount += 1
    #             if len(row) < 1:
    #                 continue
    #             ret = processWord(row[0], row[1], row[2], row[3])
    #             if ret == 100:
    #                 print("Request timed out")
    #                 print("Check internet connection")
    #                 break
    #             elif ret == 4:
    #                 unmanagedWord = unmanagedWord + 1
    #         sys.stdout.write("\r%d lines processed so far..." % lineCount)
    #         sys.stdout.flush()
    #     print(f'\nProcessed {lineCount} lines total, %d word(s) not processed\n'
    #             % unmanagedWord)


    #     with io.open("dic.json", mode='w+', encoding='utf-8') as jsonFile:
    #         json.dump(fileData, jsonFile, ensure_ascii=False, indent=4, sort_keys=True)
    #     jsonFile.close()
    # csvFile.close()
    processLaTex()

    print("Process Completed\n")
    print("--- %s seconds ---" % (time.time() - startTime))

if __name__ == '__main__':
    main()


