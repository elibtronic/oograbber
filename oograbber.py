import xml.etree.ElementTree as etree
import re
import os
import shutil
import urllib
import urllib2


#attempt to d/l the media object, log if failed
def try_jpg():
    print("trying to download simple jpg and build metadata")
    listing = os.listdir("data/temp")
    for infile in listing:
        print "Working on: ",infile
        cf = open("data/temp/" + infile + "/contents", "r")
        data_url = cf.read()
        cf.close()
        req = urllib2.Request(data_url)
        req.add_header('User-Agent','Mozilla/5.0')
        page = urllib2.urlopen(req)
        textw = str(page.read())
        
        #easiest strategy
        try:
            matcher = re.search('(<a\shref=\"([^\"]*)\">Full Image<\/a>)',textw)
            req = urllib2.Request(str.lower(matcher.group(2)))
            req.add_header('User-Agent','Mozilla/5.0')
            page = urllib2.urlopen(req)
            textw = str(page.read())
            matcher = re.search('(http://images.ourontario.ca/Partners/\w{3}/\w{3}\d+\w.\w{3})',textw)
            filename = re.search('(\w{3}\d+\w.\w{3})',matcher.group(0))
            urllib.urlretrieve(matcher.group(0),"data/temp/"+infile+"/"+filename.group(0))
            filename_for_contents = filename.group(0)
            cf = open("data/temp/" + infile + "/contents", "w")
            cf.write(filename_for_contents)
            cf.close()
            os.rename("data/temp/" + infile, "data/done_easy/" + infile)
            print "Download Completed JPG: data/temp/" + infile
        except:
            print "No Easy JPEG: data/temp/" + infile
            
            
#Try PDF's second
def try_pdf():
    print("trying to download PDF and build metadata")

    listing = os.listdir("data/temp")
    for infile in listing:
        print "Working on: ",infile
        cf = open("data/temp/" + infile + "/contents", "r")
        data_url = cf.read()
        cf.close()
        req = urllib2.Request(data_url)
        req.add_header('User-Agent','Mozilla/5.0')
        page = urllib2.urlopen(req)
        textw = str(page.read())
        
        #PDF
        try:
            matcher = re.search('(http://images.ourontario.ca/Partners/\w{3}/[A-Za-z0-9]*.pdf)',textw)
            req = urllib2.Request(str.lower(matcher.group(0)))
            filename = matcher.group(0).rsplit('/')[5]
            req.add_header('User-Agent','Mozilla/5.0')
            urllib.urlretrieve(matcher.group(0),"data/temp/"+infile+"/"+filename)
            cf = open("data/temp/" + infile + "/contents", "w")
            cf.write(filename)
            cf.close()
            os.rename("data/temp/" + infile, "data/done_pdf/" + infile)
            print "Download Completed PDF: data/temp/" + infile
        except:
            print "No PDF: data/temp/" + infile
            
            

#Final go, the difficult JPGS
def try_hard_jpg():
    print("trying to download tricky jpgs and metadata")
    listing = os.listdir("data/temp")
    for infile in listing:
        print "Working on: ",infile
        cf = open("data/temp/" + infile + "/contents", "r")
        data_url = cf.read()
        cf.close()
        req = urllib2.Request(data_url)
        req.add_header('User-Agent','Mozilla/5.0')
        page = urllib2.urlopen(req)
        textw = str(page.read())
        
        #tough JPG
        try:
            matcher = re.search('(http://images.ourontario.ca/Partners/\w{3}/[A-Za-z0-9]*.jpg)',textw)
            filename = re.sub('.jpg','f.jpg', matcher.group(0).rsplit('/')[5])
            complete_url = re.sub('.jpg', 'f.jpg',matcher.group(0))
            req.add_header('User-Agent','Mozilla/5.0')
            urllib.urlretrieve(complete_url,"data/temp/"+infile+"/"+filename)
            filename_for_contents = filename
            cf = open("data/temp/" + infile + "/contents", "w")
            cf.write(filename)
            cf.close()
            os.rename("data/temp/" + infile, "data/done_hard/" + infile)
            print "Download Completed Tough JPG: data/temp/" + infile
        except:
            print "No Tough JPG: data/temp/" + infile
            
            

        
#create dirs and skeletons of the directories
def prep_data():
    tree = etree.parse('xml/parse_me.xml')
    root = tree.getroot()
    print ("Prepping Data...")

    for nodes in root:
        current_str = "<dublin_core>\n"
        
        for value in nodes:
            pair = value.tag.rsplit('}')
            if (pair[1] == 'identifier'):
                id = value.text.rsplit('/')
                print "creating ",id[4]
                if not os.path.exists("data/temp/"+id[4]):
                    os.mkdir("data/temp/"+id[4])
                payload = str.lower(value.text)
            if (pair[1] == 'title'):
                current_str += '<dcvalue element="title" qualifier="none">'+value.text.strip()+'</dcvalue>\n'
            if (pair[1] == 'subject'):
                current_str += '<dcvalue element="subject" qualifier="none">'+value.text.strip()+'</dcvalue>\n'
            if (pair[1] == 'issued'):
                pass
            if (pair[1] == 'modified'):
                pass
            if (pair[1] == 'type'):
                current_str += '<dcvalue element="type" qualifier="none">'+value.text.strip()+'</dcvalue>\n'
            if (pair[1] == 'langauge'):
                current_str += '<dcvalue element="language" qualifier="none">'+value.text.strip()+'</dcvalue>\n'

        current_str += "</dublin_core>\n"
        mf = open("data/temp/"+id[4]+"/dublin_core.xml","w")
        cf = open("data/temp/"+id[4]+"/contents","w")
        mf.write(current_str)
        cf.write(payload)
        mf.close()
        cf.close()
    print "done prep"

    

print('Starting oograber...')
#prep_data()
try_jpg()
try_pdf()
try_hard_jpg()
print('Completed oograber...')
