from recon.core.module import BaseModule
from recon.mixins.threads import ThreadingMixin
import json
import os
import urllib
import re

class Module(BaseModule):

    meta = {
        'name': 'Instagram Image Downloader',
        'author':'James Fitts (@h1ghtopfade)',
        'description': 'Takes a username and downloads all of the images found on their instagram account.',
        'comments': (
            'Note: Will only work on open Instagram accounts',
        ),
        'options': (
            ('username', 'blah', True, 'Username of person'),
        ),
    }

    def module_run(self):
	uname = self.options['username']

	path = self.workspace

	if not os.path.exists("%s/instagram/%s" % (path, uname)):
		os.makedirs("%s/instagram/%s" % (path, uname))

	def isLegitAccount(uname):
		uri = "https://instagram.com/%s/" % (uname)
		res = self.request(uri)
		if res.status_code == 200:
			return 1
		elif res.status_code == 404:
			return -1

	def getImages(uname):
		img_array = []
		fnl_array = []

		uri = "https://instagram.com/%s/media/" % (uname)
		res = self.request(uri)
		max_id = re.findall('(?<="id":")[A-Za-z0-9]+_[A-Za-z0-9]+', res.raw)

		new_uri = "https://instagram.com/%s/media/?max_id=%s" % (uname, max_id[-1])
		res = self.request(new_uri)

		while 'more_available":true' in res.raw:
			img_array.append(re.findall('(?<=\"standard_resolution":{\"url\":\")https:\\\/\\\/[A-Za-z0-9\-.\\\/_]+', res.raw))
			max_id = re.findall('(?<="id":")[A-Za-z0-9]+_[A-Za-z0-9]+', res.raw)
			new_uri = "https://instagram.com/%s/media/?max_id=%s" % (uname, max_id[-1])
			res = self.request(new_uri)

		img_array = sum(img_array, [])
		for x in img_array:
			fnl_array.append(re.sub(r'\\\/', '/', x))
		
		self.alert('%i image(s) identified, downloading now...' % (len(fnl_array)))
		for img in fnl_array:
			img_name = img.split("/")[-1]
			new_path = "%s/instagram/%s/%s" % (path, uname, img_name)
			urllib.urlretrieve(img, new_path) 

	if isLegitAccount(uname) == 1:
		self.alert('Account is legit, lets start parsing Instagram')
		getImages(uname)
