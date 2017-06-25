#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

import os
import os, sys

sys.path.append(os.path.dirname(__file__))
import re

from microsofttranslator import Translator

from flask import Flask
from flask import request
from flask import render_template


APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

BING_CLIENT_ID = 'translate12341368'
BING_CLIENT_SECRET = 'ZcJOKvau7ZVM2C61DzwbeGUX03Zv+mPH/TCP2lL3vzg='

bingTranslator = Translator(BING_CLIENT_ID, BING_CLIENT_SECRET)




# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
def search1(word):
    import requests
    import re

    try:
        googleAnswer = requests.get(u'http://www.google.com/search?lr=lang_fa&q=%D9%81%D8%A7%D8%B1%D8%B3%DB%8C+' + word,
                                    timeout=2).text
        googleAnswer = googleAnswer.replace(u'%D9%81%D8%A7%D8%B1%D8%B3%DB%8C+', '')
        didYouMeanSign = 'Did you mean:.*href="[/a-z?&_;=%]*q=([a-z]*).*<i>.*q=http'
        showingResultsForSign = 'Showing results for.*href="[/a-z?&_;=%]*q=([a-z]*).*<i>.*Search instead for'
        didYouMean = re.search(didYouMeanSign, googleAnswer)
        showingResultsFor = re.search(showingResultsForSign, googleAnswer)
        if didYouMean is not None:
            for i in didYouMean.group(1):
                if i not in ['a', 'e', 'i', 'o'] and i not in word:
                    return word
            return didYouMean.group(1)
        elif showingResultsFor is not None:
            for i in showingResultsFor.group(1):
                if i not in ['a', 'e', 'i', 'o'] and i not in word:
                    return word
            return showingResultsFor.group(1)
        return word
    except:
        return word


def search2(word):
    import requests
    import re

    try:
        googleAnswer = requests.get(u'http://www.google.com/search?lr=lang_fa&q=' + word, timeout=2).text
        didYouMeanSign = 'Did you mean:.*href="[/a-z?&_;=%]*q=([a-z]*).*<i>.*q=http'
        showingResultsForSign = 'Showing results for.*href="[/a-z?&_;=%]*q=([a-z]*).*<i>.*Search instead for'
        didYouMean = re.search(didYouMeanSign, googleAnswer)
        showingResultsFor = re.search(showingResultsForSign, googleAnswer)
        if didYouMean is not None:
            for i in didYouMean.group(1):
                if i not in ['a', 'e', 'i', 'o'] and i not in word:
                    return word
            return didYouMean.group(1)
        elif showingResultsFor is not None:
            for i in showingResultsFor.group(1):
                if i not in ['a', 'e', 'i', 'o'] and i not in word:
                    return word
            return showingResultsFor.group(1)
        return word
    except:
        return word


def googleSuggest(word):
    searchResult1 = search1(word)
    if searchResult1 != word:
        return searchResult1
    else:
        return search2(word)



from cgi import parse_qs, escape


def worddb(s="", d=""):
    # xmlFile = os.path.dirname(__file__) + '/worddb.xml'
    xmlFile = os.path.join(APP_STATIC, 'worddb.xml')
    import xml.etree.ElementTree as ET

    if s != "":
        try:
            tree = None
            try:
                tree = ET.parse(xmlFile)
            except IOError:
                open("worddb.xml", "w").close()
                tree = ET.parse(xmlFile)
        except ET.ParseError:
            translate = ET.Element('translate')
            tree = ET.ElementTree(translate)
            tree.write(xmlFile)
        root = tree.getroot()
        if d == "":
            for word in root.findall("word"):
                fa = word.get("fa").encode("utf8")
                if s == fa:
                    return word.get("fe")
            return
        else:
            word = ET.SubElement(root, 'word')
            word.set("fa", s.decode("utf8"))
            word.set("fe", d.decode("utf8"))
            tree.write(xmlFile)
    return

@app.route('/translate', methods=['GET', 'POST'])
# def application(environ, start_response):
def application():
    import translator

    try:
        ctype = 'text/html; charset="utf8"'
        response_body = ""
        # word = parse_qs(environ['QUERY_STRING']).get('word', [''])[0]

        word_in_farsi = request.args.get('word')

        # word_in_farsi = "I want to go."
        word = bingTranslator.translate(word_in_farsi, "fa")
        # import ipdb;ipdb.set_trace()

        if word == "":
            word = u"vazhe".encode("utf8")
        text = worddb(word)
        if text != None:
            response_body = text
        else:
            # if environ['PATH_INFO'] == '/health':
            #     response_body = "1"
            # elif environ['PATH_INFO'] == '/env':
            #     response_body = ['%s: %s' % (key, value)
            #                      for key, value in sorted(environ.items())]
            #     response_body = '\n'.join(response_body)
            # else:
            # word = word.decode('u8')
            ctype = 'text/html; charset="utf8"'
            import requests

            xword = word.replace(u'+', u' ')
            for word in xword.split(u' '):
                reload(translator)
                tr = translator.translator()
                result = ''
                pron = word
                try:
                    text = requests.get(
                        'http://www.loghatnaameh.org/dehkhodasearchresult-fa.html?searchtype=2&word=' + word,
                        timeout=2).text
                    pText = text.find(u'href=\'dehkhodaworddetail')
                    foundPText = 1
                    p = ''
                    while (pText > 0):
                        p = text[pText + 85:pText + 228]
                        pText = text.find(u'href=\'dehkhodaworddetail', pText + 1)
                        foundPText = foundPText + 1
                        if foundPText < 5 and re.search(word + u'\s*\.\s*\[', p) is not None and re.search(
                                u'\[ *(.*) *\]', p) is not None:
                            pron = re.search(u'\[ *(.*) *\]', p).group(1).split(u' / ')
                            break
                    # make working for last t arabic
                    if word[-1] == u'\u0647' and pText < 0:
                        word = word.replace(u'\u0647', u'\u0629')
                        pText = text.find(u'href=\'dehkhodaworddetail')
                        foundPText = 1
                        p = ''
                        while (pText > 0):
                            p = text[pText + 85:pText + 228]
                            pText = text.find(u'href=\'dehkhodaworddetail', pText + 1)
                            foundPText = foundPText + 1
                            if foundPText < 5 and re.search(word + u'\s*\.\s*\[', p) is not None and re.search(
                                    u'\[ *(.*) *\]', p) is not None:
                                pron = re.search(u'\[ *(.*) *\]', p).group(1).split(u' / ')
                                break
                        word = word.replace(u'\u0629', u'\u0647')
                    preI = ''
                    if type(pron) is list:
                        for i in pron:
                            i = i.replace(u' ', '')
                            j = 0
                            k = 0
                            while j < len(i):
                                if j > 0 and j % 2 == 0:
                                    i = i[:k] + u' ' + i[k:]
                                    k = k + 1
                                j = j + 1
                                k = k + 1
                            pattern = i.replace(u'\u0650', u'.')
                            pattern = pattern.replace(u'\u064e', u'.')
                            pattern = pattern.replace(u'\u064f', u'.')
                            if re.search(pattern, preI) is not None:
                                i = re.sub(pattern, i, preI)
                            preI = i
                            i = re.sub(u'.ا', '', i)
                            i = re.sub(u'.و', '', i)
                            #	i = re.sub(u'.ی', '', i)
                            i = i.replace(u'  ', u' ')
                            resultTmp = googleSuggest(tr.trf2f(i.encode('u8'), word.encode('u8')))
                            worddb(word.encode('u8'), resultTmp.encode('u8'))
                            if False and ren(pron) > 1:
                                result = result + resultTmp + '/'
                            else:
                                result = resultTmp
                    else:
                        result = googleSuggest(tr.trf2f(pron.encode('u8'), word.encode('u8')))
                        worddb(word.encode('u8'), result.encode('u8'))
                except:
                    text = requests.get('http://fa.wiktionary.org/wiki/' + word, timeout=2).text
                    from bs4 import BeautifulSoup

                    soup = BeautifulSoup(text)
                    for p in soup.findAll("p"):
                        if p.parent.name == "div":
                            if re.search("\(.*\)", p.encode("utf8")) != None:
                                pron = str(p)
                                break
                    #if 'p' in locals() and re.search("\(.*\)",p.encode("utf8")) != None:
                    if pron != word:
                        result = googleSuggest(tr.trf2f(pron, word.encode('u8')))
                    else:
                        pron = u"<p>(" + word + u")</p>"
                        result = googleSuggest(tr.trf2f(pron.encode('u8'), word.encode('u8')))
                    worddb(word.encode('u8'), result.encode('u8'))

                response_body = response_body + ' ' + result

                # response_body = response_body

        # response_body = response_body.encode('u8')
        # status = '200 OK'
        # response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
        # start_response(status, response_headers)
        # return [response_body]
        return response_body
    except:
        status = '500 Internal Server Error'
        import traceback
        #
        # response_body = response_body + "<br/>\n" + traceback.format_exc()
        # response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
        # start_response(status, response_headers)
        # return [response_body]

        return traceback.format_exc()


@app.route("/")
def test():
    return render_template('main.html')



#
# Below for testing only
#
if __name__ == '__main__':
    # from wsgiref.simple_server import make_server
    #
    # httpd = make_server('localhost', 8051, application)
    # # Wait for a single request, serve it and quit.
    # httpd.handle_request()

    app.debug = True
    app.run()
