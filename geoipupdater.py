#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
	Update GeoIP.dat if newer version exists on maxmind.com
	Intended to run as a cronjob
"""

__author__ = 'Morten Abildgaard <morten@abildgaard.org>'
__version__ = '1.1'

from cStringIO import StringIO
from datetime import datetime
from gzip import GzipFile
import logging as log
import os, sys
from requests import get, head

class GeoIP:
	def __init__(self):
		self.url = 'http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz'
		log.basicConfig(level=log.DEBUG,format='%(asctime)s %(levelname)s %(message)s',
			filename='%s.log'%os.path.abspath(__file__)[:-3])
		self.pwd = os.path.dirname(os.path.abspath(__file__))
		self.datfile = os.path.join(self.pwd,'GeoIP.dat')
		self.datfile = '/usr/share/GeoIP/GeoIP.dat'
		log.info('Checking for newer version of %s' % self.datfile)
		self.upd8()
		exit()

	def upd8(self):
		r = head(self.url)
		if r.headers and 'last-modified' in r.headers:
			remote_lm = datetime.strptime(r.headers['last-modified'], '%a, %d %b %Y %H:%M:%S GMT')
		local_lm = self.get_last_modified()
		if remote_lm > local_lm:
			log.info('Updating. remote_lm  (%s) seems newer than local_lm (%s)' % (remote_lm,local_lm))
			try:
				r = get(self.url)
				log.debug(r.headers)
				data = GzipFile('','r',0,StringIO(r.content)).read()
				with open(self.datfile, 'w') as f: f.write(data)
			except IOError:
				log.error('Unable to write to file %s' % self.datfile)
				exit(sys.exc_info())
			except Exception:
				log.error(sys.exc_info()[1])

	def get_last_modified(self):
		try:
			return datetime.fromtimestamp(os.path.getmtime(self.datfile))
		except Exception:
			return datetime.fromtimestamp(1)

if __name__ == '__main__':
	sys.exit(GeoIP())
