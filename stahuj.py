"""
Stahne aktualni seznam pobidek z webu Czech Investu
"""
import lxml.html
from urllib.parse import urljoin
from urllib.request import urlopen, urlretrieve

url = 'http://www.czechinvest.org/investicni-pobidky-nove'

ht = lxml.html.fromstring(urlopen(url).read())

tbl = ht.cssselect('div#content table')[0]

up = [j for j in tbl.cssselect('a') if j.text == 'Udělené investiční pobídky']
assert len(up) == 1

urlretrieve(urljoin(url, up[0].attrib['href']), 'cache/data.xls')
