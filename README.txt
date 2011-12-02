00graber.py

When given an xml file of items in dublin core from 0ur0ntario.ca 
will download full size JPG or PDFS of item and create DSpace ready input

Give it an XML file with Dublin Core output (currently set to xml/parse_me.xml)
	Will try to download metadata of all items and dump into data/temp
	Will then go through each folder and:
		Try to Download JPG hiding under 'Full Image Link' -> data/done_easy
		Try to Download PDF if not jpg -> data/done_pdf
		Try to Download fullsized JPG that creates the Zoomify widget -> data/done_hard

	Anything left in data/temp it doesn't recognize.

In the complete done directories will be items formated in Dublin Core that can be ingested by DSpace
on the command line.  (Details: http://www.dspace.org/1_7_0Documentation/System%20Administration.html#SystemAdministration-AddingItemstoaCollection)

This does get hung a bit if there are none ascii characters in the data. The Description field has now been forced to utf8, before it writes out to disk.
&amp; show up in the XML data.  You might want to escape it before running this software, it will bork if it finds any.

This version now does description and creator tags, first few versions didn't for some reason.... I'm a busy buy I forget things.

