import os
import json
import urllib2

url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&term=(%22Journal%20of%20natural%20products%22%5BJournal%5D)%20AND%20free%20full%20text%5BFilter%5D)"

response = urllib2.urlopen(url).read().decode('utf-8')
data = json.loads(response)

count = data['esearchresult']['count']
retmax = data['esearchresult']['retmax']
print 'Found', count, 'articles matching the query'
if count > retmax:
    print 'Warning: obtained only', retmax, 'IDs out of', count

ids = data['esearchresult']['idlist']
command = 'ruby pubmedid2pdf.rb ' + ','.join(ids)
print 'Attempting to download PDFs'

os.system(command)
if len(os.listdir('pdf')) == int(retmax):
    print 'Successfully downloaded everything'
else:
    print 'Some articles were not downloaded'


