import sys
import re
import pandas

df = pandas.read_csv("newbooks.txt", sep='^', na_filter=False)
df.columns = ['CALL','TITLE','EDITION','IMPRINT','SUBJECT','RECORD']
# add space between classification letters and numbers
df.CALL = df.CALL.str.replace('(?P<ClassLetters>\A[A-Z]*(?=[0-9]))', '\g<ClassLetters> ')
df.SUBJECT = df.SUBJECT.str.strip()
# remove oclc fast tags. example [;United States. fast (OCoLC)fst01204155]
df.SUBJECT = df.SUBJECT.str.replace("\;[^<;]*\.? fast \(OCoLC\)fst[0-9]*","")
# remove oclc fast date facets. example [;1900-1999 fast][; 1787 fast]
df.SUBJECT = df.SUBJECT.str.replace('\;*[0-9]{4} ?\- ?[0-9]{4} fast', '')
df.SUBJECT = df.SUBJECT.str.replace('\;*[0-9]{4} fast', '')
# remove local genre heading notations
df.SUBJECT = df.SUBJECT.str.replace('(\.* lcgft)|(\. local)', '.')
# add spaces between semicolons
df.SUBJECT = df.SUBJECT.str.replace('\;', '; ')
#escape ampersands
df.TITLE = df.TITLE.str.replace('&','&amp;')
df.EDITION = df.EDITION.str.replace('&','&amp;')
df.IMPRINT = df.IMPRINT.str.replace('&','&amp;')
df.SUBJECT = df.SUBJECT.str.replace('&','&amp;')

def func(row):
    xml = ['<BOOK>']
    for field in row.index:
        xml.append('  <{0}>{1}</{0}>'.format(field, row[field]))
    return '\n'.join(xml) + '\n</BOOK>'

content = '<?xml version="1.0" encoding="UTF-8"?>\n<dataroot>\n'
content = content + '\n'.join(df.apply(func, axis=1))
content = content + '\n</dataroot>'

with open('file.xml', 'w') as f:
    f.write(content)
