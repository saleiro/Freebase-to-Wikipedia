#!/usr/bin/env  python2
#  -*-  coding:  utf-8  -*-

"""
Author:  Pedro  Saleiro (pssc@fe.up.pt)

"""
import  sys, os, gzip
from  datetime  import  datetime
from parser import WikipediaParser


def ReadFreebase(handler, filename, auxfile, block_len, languages): 
    parser  =  WikipediaParser(filename, languages, auxfile)
    line_num =  0
    m  =  0
    _buff  =  ''
    dd  =  datetime.today().strftime("%d/%m  -  %H:%M:%S")
    print("%s  :  Reader  is  starting"  %  dd)
    while  True:
        buff = handler.read(block_len)
        lines = (_buff + buff).split('\n')
        parser.find_and_write(lines[:-1])
        line_num +=  len(lines[:-1])
        if  line_num /  10000000  ==  m:
            dd  =  datetime.today().strftime("%d/%m  -  %H:%M:%S")
            print("%s  :  Line  %d"  %  (dd,  line_num))
            m  +=  1
        if  not  buff:  
            parser.handler.close()
            break
        _buff  =  lines[-1]
    dd  =  datetime.today().strftime("%d/%m  -  %H:%M:%S")
    print("%s  :  Reader  is  done  :  %d  lines"  %  (dd,  l))


def CreatingTSV(auxfile):
    print "freebase to wikipedia"
    maps = {}
    mid = ''
    dic = {}
    count = 1
    with gzip.open(dumpfile,  'rt') as dump:
        for line in dump:
            count += 1
            if count % 1000000 == 0:
                print count
            attr = line.strip('\n').split('\t')
            if attr[0] != mid:
                if len(dic) > 1:
                    mid = '/' + mid.replace('.','/')
                    maps[mid] = dic
                    #print mid, maps[mid]
                dic = {}
                mid = attr[0]
            if attr[1] == 'en_wikipedia_link':
                if attr[2].startswith('index.html'):
                    dic['curid'] = attr[2].replace('index.html?curid=','')
                else:
                    dic['en_wikipedia'] = attr[2]
            else:
                dic[attr[1]] = attr[2]
    Flush(auxfile,maps)
    return None


def Flush(auxfile, maps):
    print 'Flushing tsv file of length ', len(maps)
    with open('mid2wikipedia.tsv','w') as out:
        out.write('mid\ten_name\ten_wikipedia\tcurid\n')
        for key in maps:
            out.write(key+'\t')
            try:
                out.write(maps[key]['en_name']+'\t')
            except KeyError:
                out.write('-\t')
            try:
                out.write(maps[key]['en_wikipedia']+'\t')
            except KeyError:
                out.write('-\t')
            try:
                out.write(maps[key]['curid']+'\n')
            except KeyError:
                out.write('-\n')


if  __name__  ==  '__main__':
    freebase_path  =  sys.argv[1]
    basename  =  os.path.basename(freebase_path)
    aux_file = 'freebase_wikipedia_dump.gz'
    dump =  gzip.open(freebase_path, 'rt')
    languages = ['en']
    block_len = 1024 * 1024
    ReadFreebase(dump,  dump.name, aux_file, block_len, languages)
    dump.close()
    CreatingTSV(auxfile)


