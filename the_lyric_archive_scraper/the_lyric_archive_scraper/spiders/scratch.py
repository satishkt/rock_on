from scrapy import Selector

__author__ = 'Satish'

import urlparse

from posixpath import basename, dirname

url = 'http://www.thelyricarchive.com/genres/Rock/British-Metal/'
parse_object = urlparse.urlparse(url)
print (parse_object.path[13:])[:-1]
# print basename(parse_object.path)

liststs = ['http://www.thelyricarchive.com/artists/0-9/1/', 'http://www.thelyricarchive.com/artists/H/1/',
           'http://www.thelyricarchive.com/artist/383107/Goanna']
exclude = ['artists']
x = (s for s in liststs if not any(e in s for e in exclude))
print list(x)

body = ""
with open('test.html', 'r') as myfile:
    body = myfile.read()

hxs = Selector(text=body)
# artist_title =hxs.xpath('/html/body/table[1]/tr[1]/td/h1/text()').extract()[0]
#
# topsongs = hxs.xpath('/html/body/table[1]/tr[2]/td[3]/div/a/text()')
# topsong_list =[]
# for topsong in topsongs:
#      topsong_list.append(topsong.extract().rstrip('lyrics').strip())
#
# grp_members = hxs.xpath('/html/body/table[1]/tr[2]/td[2]/table[2]/tr/td/a/text()')
# grpmember_list =[]
# for member  in grp_members:
#     grpmember_list.append(member.extract().strip())
#
# print ','.join(grpmember_list)
#
#
# print artist_title.rstrip(' lyrics')
# artist_tbl = hxs.xpath('/html/body/table[1]/tr[2]/td[2]/table[1]')
# artist_tbl_trs = artist_tbl.xpath('tr')
#
#
#
#
# for tr in artist_tbl_trs:
#     tds = tr.xpath('td')
#     label_td = tds[0]
#     val_td = tds[1]
#     label = label_td.xpath('b/text()').extract()
#
#     if len(label) > 0 and label[0] == 'Formed:':
#         value = val_td.xpath('./text()').extract()
#         print value[0]
#     if len(label) > 0 and label[0] == 'Disbanded:':
#         value = val_td.xpath('./text()').extract()
#         print value[0]
#     if len(label) > 0 and label[0] == 'Years active:':
#         value = val_td.xpath('./text()').extract()
#         print value[0]
#     if len(label) > 0 and label[0] == 'Genre:':
#         value = val_td.xpath('./text()').extract()
#         print value[0]
#     if len(label) > 0 and label[0] == 'Styles:':
#         style_val = []
#         lis = val_td.xpath('ul/li')
#         for li in lis:
#            li_val =li.xpath('./text()').extract()
#            if(len(li_val) >0 ):
#                 style_val.append(li_val[0])
#         print ','.join(style_val)
#
#
#
# album_links  = hxs.xpath("//div[@style = 'float: left; padding:5px']/table//tr/td/strong/a")
# for album in album_links:
#     print album.xpath('@href').extract()[0]
#     print album.xpath('text()').extract()[0]


album_title = hxs.xpath('/html/body/table[2]/tr/td[2]/table/tr[2]/td[2]/text()').extract()[0]
released_year = hxs.xpath('/html/body/table[2]/tr/td[2]/table/tr[3]/td[2]/text()').extract()[0]
genre  = hxs.xpath('/html/body/table[2]/tr/td[2]/table/tr[4]/td[2]/text()')
album_styles = hxs.xpath('/html/body/table[2]/tr/td[2]/table/tr[5]/td[2]/ul/li')
style_list= []
for album_style in album_styles:
    style  = album_style.xpath('./text()').extract()
    if(len(style) >0) :
        style_list.append(style[0])

print ','.join(style_list)


print album_title,released_year
