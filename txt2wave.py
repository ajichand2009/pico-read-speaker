#!/usr/bin/python3

# -*- coding: utf-8 -*-
#Transform text in wav audio
#exec : text2wav.py

import os
import sys
import argparse

#limit char of pico2wave
limit_char = 30000

#choose default language between: 'en-US','en-GB','de-DE','es-ES','fr-FR','it-IT'
default_lang = 'en-GB'

#cut the text by sentence
def casier_txt(list_txt):
    current_letter=0
    list_sentence = []
    list_chapter = []

    for sentence in list_txt:
        current_letter += len(sentence)
        if limit_char < current_letter:
            if list_sentence:
                list_chapter.append(list_sentence)
                list_sentence = []
            else:
                list_sentence.append(u'%s.' % sentence)
                list_chapter.append(list_sentence)
                list_sentence = []
            current_letter = 0
        else:
            list_sentence.append(u'%s.' % sentence)

    if list_sentence:
        list_chapter.append(list_sentence)

    return list_chapter

# execute command line pico2wave
def text_to_speech(txt, lang):
    txt = txt.replace('"', '')
    total_letter = len(txt)
    if total_letter > 1:
        list_txt = txt.split('.')
        list_txt = filter(None, list_txt)
    else:
        list_txt = []
        list_txt.append("No text found.")

    if list_txt:
        position = casier_txt(list_txt)

    else:
        return "No sentence"

    os.system('ln -s /dev/stdout /tmp/out.wav')
    for index,value in enumerate(position):
        if value:
            value =' '.join(value)
            print("Vocalising in %s ..." % (lang))
            os.system('pico2wave -l={} -w=/tmp/out.wav "{}" | ffmpeg -i - -ar 48000 -ac 1 -ab 64k -f mp3 {}.mp3 -y'.format(lang, value, index + 1))
            os.system('cat {}.mp3 >> audio_book.mp3 && rm {}.mp3'.format(index + 1, index + 1))
    os.system('rm /tmp/out.wav')


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--infile',help='Input text file.',required=True)
	parser.add_argument('-l','--lang',help='Language',choices=['en-US','en-GB','de-DE','es-ES','fr-FR','it-IT'],default='en-GB')
	#parser.add_argument('-o','--outfile',help='Output file',required=True)
	args = parser.parse_args()

	with open(args.infile,'r') as rf:
		txt = rf.read()
	
	text_to_speech(txt,args.lang)

	input_text_file = os.path.splitext(args.infile)[0]
	os.system('mv audio_book.mp3 {}.mp3'.format(input_text_file))

	print('Output file = %s.mp3' % input_text_file)

if __name__ == "__main__":
    main()
