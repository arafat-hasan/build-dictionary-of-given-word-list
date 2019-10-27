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
from pylatex.utils import italic, NoEscape, bold, escape_latex
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

    titlePage = r'''
\renewcommand{\maketitle}{%

	\begin{titlepage} % Suppresses headers and footers on the title page

	\centering % Centre everything on the title page
	
	\scshape % Use small caps for all text on the title page
	
	\vspace*{\baselineskip} % White space at the top of the page
	
	%------------------------------------------------
	%	Title
	%------------------------------------------------
	
	\rule{\textwidth}{1.6pt}\vspace*{-\baselineskip}\vspace*{2pt} % Thick horizontal rule
	\rule{\textwidth}{0.4pt} % Thin horizontal rule
	
	\vspace{0.75\baselineskip} % Whitespace above the title
	
	{\LARGE THE DICTIONARY \\ OF COLLECTED WORDS\\} % Title
	
	\vspace{0.75\baselineskip} % Whitespace below the title
	
	\rule{\textwidth}{0.4pt}\vspace*{-\baselineskip}\vspace{3.2pt} % Thin horizontal rule
	\rule{\textwidth}{1.6pt} % Thick horizontal rule
	
	\vspace{2\baselineskip} % Whitespace after the title block
	
	%------------------------------------------------
	%	Subtitle
	%------------------------------------------------
	
	A Number of Fascinating and Fundamental Words Presented in a Dictionary Way % Subtitle or further description
	
	\vspace*{3\baselineskip} % Whitespace under the subtitle
    \vspace*{3\baselineskip} % Whitespace under the subtitle
    \vspace*{3\baselineskip} % Whitespace under the subtitle
	
	%------------------------------------------------
	%	Editor(s)
	%------------------------------------------------
	
	Edited By
	
	\vspace{0.5\baselineskip} % Whitespace before the editors
	
	{\scshape\Large Arafat Hasan \\} % Editor list
	
	\vspace{0.5\baselineskip} % Whitespace below the editor list
	
	\textit{Mawlana Bhashani Science and Technology University \\ Tangail, Bangladesh} % Editor affiliation
	
	\vfill % Whitespace between editor names and publisher logo
	
	%------------------------------------------------
	%	Publisher
	%------------------------------------------------
	
	%\plogo % Publisher logo
	
	%\vspace{0.3\baselineskip} % Whitespace under the publisher logo
	
	\the\year % Publication year
	
	%{\large publisher} % Publisher

	\end{titlepage}
}
'''


    pdfMeta = r'''
\usepackage[xetex,
            pdfauthor={Arafat Hasan},
            pdftitle={The Dictionary of Collected Words},
            pdfsubject={A Personal Dictionary},
            pdfkeywords={Personal Dictionary},
            pdfproducer={XeLaTeX on Ubuntu},
            pdfcreator={XeLaTeX}]{hyperref}
   '''


    geometry_options = {"top":"2.3cm","bottom":"2.0cm", "left":"2.5cm",\
            "right":"2.0cm", "columnsep":"27pt"}
    doc = Document('TheDictionaryOfCollectedWords', geometry_options=geometry_options)
    doc.documentclass = Command(
            'documentclass',
            options=['10pt', 'a4paper', 'twoside'],
            arguments=['book'],
            )

    doc.packages.append(Package('palatino'))
    doc.packages.append(Package('microtype'))
    doc.packages.append(Package('multicol'))
    doc.packages.append(Package('fontspec'))
    doc.packages.append(Package('enumitem'))
    doc.packages.append(Package('graphicx'))
    doc.packages.append(Package('PTSerif'))
    doc.packages.append(Package('titlesec', NoEscape('bf, sf, center')))
    doc.packages.append(Package('fancyhdr'))
    

    doc.preamble.append(Command('usepackage', \
            NoEscape(r'xcolor'), 'svgnames'))

    
    doc.preamble.append(NoEscape(pdfMeta))
    doc.preamble.append(NoEscape('%'))
    doc.preamble.append(NoEscape('%'))

    doc.preamble.append(Command('setmainfont', \
            'TeX Gyre Pagella', 'Numbers=OldStyle'))


    doc.preamble.append(Command('fancyhead', \
            NoEscape(r'\textsf{\rightmark}'), 'L'))
    doc.preamble.append(Command('fancyhead', \
            NoEscape(r'\textsf{\leftmark}'), 'R'))

    doc.preamble.append(NoEscape('%'))
    doc.preamble.append(NoEscape('%'))

    doc.preamble.append(Command('renewcommand', \
        arguments=Arguments(NoEscape(r'\headrulewidth'), '1.4pt')))

    doc.preamble.append(Command('fancyfoot', \
            NoEscape(r'\textbf{\textsf{\thepage}}'), 'C'))

    doc.preamble.append(Command('renewcommand', \
        arguments=Arguments(NoEscape(r'\footrulewidth'), '1.4pt')))

    doc.preamble.append(Command('pagestyle', 'fancy'))

    doc.append(NoEscape(r'\setlength{\parindent}{-0.7em}')) 

    new_comm = UnsafeCommand('newcommand', '\entry', options=7, \
    extra_arguments=NoEscape(r'\textbf{#1}\markboth{#1}{#1}\ {{\fontspec{Doulos SIL} #2}}\  {{\fontspec{Kalpurush} \small {#3}}}\ {#4}\ {#5}\ {\textit{#6}}\ {#7}'))
    doc.preamble.append(new_comm)

    color_bullet = UnsafeCommand('newcommand', '\colorBulletS', options=1, \
    extra_arguments=NoEscape(r'\colorbox[RGB]{171,171,171}{\makebox(11,2){\textcolor{white}{{\tiny \textbf{#1}}}}}'))
    doc.preamble.append(color_bullet)

    color_bullet = UnsafeCommand('newcommand', '\colorBullet', options=1, \
    extra_arguments=NoEscape(r'\colorbox[RGB]{171,171,171}{\makebox(22, 1){\textcolor{white}{{\tiny \textbf{#1}}}}}'))
    doc.preamble.append(color_bullet)

    doc.preamble.append(NoEscape(r'\newcommand{\plogo}{\fbox{$\mathcal{PL}$}} % Generic dummy publisher logo'))


    doc.preamble.append(NoEscape('%'))
    doc.preamble.append(NoEscape('%'))

    doc.preamble.append(NoEscape(titlePage))
    doc.append(NoEscape(r'\maketitle'))
    entriesList = list(fileData.keys())
    entriesList.sort()

    currentSection = "a"
    sectionStr = "\chapter*{" + currentSection.upper() + "}"
    doc.append(NoEscape(sectionStr))
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


           word         = escape_latex(word)
           bengali      = escape_latex(bengali)
           prep         = escape_latex(prep)   
           ownExample   = escape_latex(ownExample)
           origin       = escape_latex(origin)
           phonetic     = escape_latex(phonetic)
           
           if len(prep): prep = " \\colorBullet{OTHER} " + prep
           if len(origin): origin = " \\colorBullet{ORIGIN} " + origin

           partsOfSpeech = list(meaning.keys())

           if len(partsOfSpeech) == 1:
               partStr = ""
           else:
               partStr = "\\small{\\textsf{\\textit{" + escape_latex(", ".join(partsOfSpeech)) + "}}}"
           
           for part in partsOfSpeech:
               escapePart = escape_latex(str(part))
               onepart     = meaning[part]
               deffCnt = 0
               if len(partsOfSpeech) == 1:
                   strGen = "\\textsf{\\textit{" + escapePart + "}}\\"
               else:
                   strGen = "\\\\{\\fontspec{DejaVu Sans}▪ }\\textsf{\\textit{" + escapePart + "}}\\\\"

               for deff in onepart:
                   deffCnt = deffCnt + 1
                   definition  = deff.get('definition',"")
                   example     = deff.get('example',"")
                   synonyms    = deff.get('synonyms',{})

                   definition   = escape_latex(definition)
                   example      = escape_latex(example)
                   synonyms     = escape_latex(", ".join(synonyms))
                   if len(synonyms): synonyms     = " \\colorBulletS{SYN} " + synonyms

                   strGen = strGen + " \\textbf{" + str(deffCnt) + "} " + definition + " {\\fontspec{DejaVu Sans}◇} " + "\\textit{" + example + "}" + synonyms

               partStr = partStr + " " + strGen

           # lorem = "\entry{"+word+"}{"+phonetic+"}{"+bengali+"}{"+partStr+"}" + "{" + prep +"}" + "{" + ownExample + "}" + "{" + origin + "}" // With origin
           lorem = "\entry{"+word+"}{"+phonetic+"}{"+bengali+"}{"+partStr+"}" + "{" + prep +"}" + "{" + ownExample + "}"
           if item[0] is not currentSection[0]:
               currentSection = item[0]
               sectionStr = "\section*{" + currentSection.upper() + "}"
               doc.append(NoEscape(r'\end{multicols}'))
               doc.append(NoEscape(r'\pagebreak'))
               doc.append(NoEscape(sectionStr))
               doc.append(NoEscape(r'\begin{multicols}{2}'))
           doc.append(NoEscape(lorem))
           doc.append(NoEscape(r'\par'))
               


    doc.append(NoEscape(r'\end{multicols}'))
    doc.generate_pdf(clean_tex=False, compiler='xelatex')
    doc.generate_tex()

    tex = doc.dumps() 





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
    csvFile.close()
    processLaTex()

    print("Process Completed\n")
    print("--- %s seconds ---" % (time.time() - startTime))

if __name__ == '__main__':
    main()


