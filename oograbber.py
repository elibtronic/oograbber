#Working with OO - Dublin Core Export.asp.xml

#Run through each <record> in the xml parse appropriately and download full-image
#in <dc:indentifer> load that and find link named 'Full Image'
#write out metadata in DSpace friendly format

import xml.etree.ElementTree as etree
import re
import os
import shutil
import urllib
import urllib2
tree = etree.parse('parse_me.xml')
fail_file = open('failed_item_dl.log','w')
jpg_fail_file = open('failed_jpg_items.log','w')
root = tree.getroot()

current_str = ""

print('Parsing...')

for nodes in root:
    killed = False
    current_str = "<dublin_core>"
    for value in nodes:
            
            pair = value.tag.rsplit('}')
            if (pair[1] == 'identifier'):
                id = value.text.rsplit('/')
                print id[4]
                if not os.path.exists("data/"+id[4]):
                    os.mkdir("data/"+id[4])
                #need to d/l jpg and save in that dir
                #for some reason domain name needs to be in lowercase ?!
                #Find the Full Image URL

                try:
                    req = urllib2.Request(str.lower(value.text))
                    req.add_header('User-Agent','Mozilla/5.0')
                    page = urllib2.urlopen(req)
                    textw = str(page.read())
                    matcher = re.search('(<a\shref=\"([^\"]*)\">Full Image<\/a>)',textw)
                except:
                    print "Could not d/l info page for item: ",id[4]
                    fail_file.write(value.text)
                    #shutil.rmtree("data/"+id[4])
                    killed = True
                    
                #D/L image from previously found URL
                
                try:
                    req = urllib2.Request(str.lower(matcher.group(2)))
                    req.add_header('User-Agent','Mozilla/5.0')
                    page = urllib2.urlopen(req)
                    textw = str(page.read())
                    matcher = re.search('(http://images.ourontario.ca/Partners/\w{3}/\w{3}\d+\w.\w{3})',textw)
                    filename = re.search('(\w{3}\d+\w.\w{3})',matcher.group(0))
                    urllib.urlretrieve(matcher.group(0),"data/"+id[4]+"/"+filename.group(0))
                    filename_for_contents = filename.group(0)
                except:
                    print "Could not d/l JPG for item: ",id[4]
                    jpg_fail_file.write(value.text+"\n")
                    try:
                        shutil.rmtree("data/"+id[4])
                    except:
                        print "could not delete: data/",id[4]
                    killed = True
                    

            if (pair[1] == 'title'):
                current_str += '<dcvalue element="title" qualifier="none">'+value.text.strip()+'</dcvalue>'
            if (pair[1] == 'subject'):
                current_str += '<dcvalue element="subject" qualifier="none">'+value.text.strip()+'</dcvalue>'
            if (pair[1] == 'issued'):
                pass
            if (pair[1] == 'modified'):
                pass
            if (pair[1] == 'type'):
                current_str += '<dcvalue element="type" qualifier="none">'+value.text.strip()+'</dcvalue>'
            if (pair[1] == 'langauge'):
                current_str += '<dcvalue element="language" qualifier="none">'+value.text.strip()+'</dcvalue>'

    current_str +="</dublin_core>"
    if(killed == False):
        mf = open("data/"+id[4]+"/dublin_core.xml","w")
        cf = open("data/"+id[4]+"/contents","w")
        mf.write(current_str)
        cf.write(filename_for_contents)
        mf.close()
        cf.close()
    print "...completed"

fail_file.close()
jpg_fail_file.close()
        
print "Now all done"
