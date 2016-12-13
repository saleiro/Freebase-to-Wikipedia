#!/usr/bin/env  python2
#  -*-  coding:  utf-8  -*-

"""
Author:  Pedro  Saleiro (pssc@fe.up.pt)

"""

import  sys,  re,  os,  gzip,  zlib

class  Parser():
    def  __init__(self,  basename, languages, auxfile):
        self.langs = languages
        self.basename = basename
        self.cache_size = 30000
        x  =  '(' + '|'.join([p for p in self.patterns.keys()]) + ')'
        self.pat = re.compile(self.base_pat % x)
        self.handler = gzip.open(auxfile, 'w')
        self.cached_lines  =  []

    def find_and_write(self,  lines):
        for  line  in  lines:
            pmatch  =  self.pat.match(line)
            if  pmatch:
                r  =  self.get_wiki(pmatch)
                if  r:
                    self.cached_lines.append('\t'.join(r))
                    if  len(self.cached_lines)  >  self.cache_size:
                        self.handler.write('\n'.join(self.cached_lines))
                        self.handler.write('\n')
                        self.cached_lines  =  []


class  WikipediaParser(Parser):
    def  __init__(self,  basename, languages, auxfile):
        self.base_pat  =  '<http://rdf.freebase.com/ns/(m\..*)>\t'  \
                                        '<http://rdf.freebase.com/ns/%s>\t(.*)\t.'
        self.patterns  =  {
            'type.object.name': 'name',
            'common.topic.topic_equivalent_webpage':  'wikipedia_link'
        }
        self.regex_com = re.compile('"(.*)"@(.*)')
        self.regex_wiki = re.compile('<http://(.*).wikipedia.org/wiki/(.*)>')
        Parser.__init__(self, basename, languages, auxfile)

    def get_wiki(self,  pmatch):
        _id = pmatch.group(1)
        key = self.patterns[pmatch.group(2)]
        if key == 'wikipedia_link':
            m = self.regex_wiki.match(pmatch.group(3))
            if m:
                lang = m.group(1)
                val = m.group(2)
                if lang in self.langs:
                    return _id, lang + '_' + key, val
        elif key == 'name':
            m = self.regex_com.match(pmatch.group(3))
            if m:
                lang = m.group(2)
                val = m.group(1)
                if lang in self.langs:
                    return _id, lang + '_' + key, val
        return None

