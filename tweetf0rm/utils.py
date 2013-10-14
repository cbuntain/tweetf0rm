#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Singleton(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

import requests, json
def public_ip():
	r = requests.get('http://httpbin.org/ip')
	return r.json()['origin']

import hashlib
def md5(data):
	return hashlib.md5(data).hexdigest()

def node_id():
	ip = public_ip()
	return md5(ip)

def full_stack():
	import traceback, sys
	exc = sys.exc_info()[0]
	stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
	if not exc is None:  # i.e. if an exception is present
		del stack[-1]       # remove call of full_stack, the printed exception
							# will contain the caught exception caller instead
	trc = 'Traceback (most recent call last):\n'
	stackstr = trc + ''.join(traceback.format_list(stack))
	if not exc is None:
		 stackstr += '  ' + traceback.format_exc().lstrip(trc)
	return stackstr

def check_proxies(proxies, proxy_type="http"):
	url = "http://google.com"
	headers = {
		'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0',
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'en-US,en;q=0.5'
	}

	verified_proxies = []
	for proxy in proxies:
		try:			
			proxy_dict = {proxy_type : '%s://%s'%(proxy_type, proxy)}

			r = requests.get(url, headers=headers, proxies=proxy_dict)
			if (r.status_code == requests.codes.ok):
				verified_proxies.append(proxy)

				logger.info('GOOD: [%s] - %d'%(proxy, r.elapsed.seconds))
			else:
				logger.warn('BROKEN: [%s] - %d'%(proxy, r.elapsed.seconds))
		except:
			logger.warn('BROKEN: [%s] - %d'%(proxy, r.elapsed.seconds))
			pass

	return verified_proxies