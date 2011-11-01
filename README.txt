00graber.py

When given an xml file of items in dublin core from 0ur0ntario.ca 
will download full size JPG of item and create DSpace ready input

-Caveats
	0ur0ntario item needs a link called 'Full Image'
	Will only ingest metadata with xmlns:dc="http://purl.org/dc/elements/1.1/" as name space (implicit in description)
	Formats DSpace info based on these details: http://www.dspace.org/1_7_0Documentation/System%20Administration.html#SystemAdministration-ImportingItems


-Upcoming
	Hopefully will support JPG items that do not have 'Full Image' link in display. ie some digitized documents
	Hopefully will support PDF items too