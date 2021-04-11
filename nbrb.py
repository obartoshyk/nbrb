#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests

class Session(object):
	"""connector to nbrb site"""
	def __init__(self):
		super(Session, self).__init__()
		self.way = 'https://www.nbrb.by/api/exrates'
	
	def __enter__(self):
		self.session = requests.Session()
		return self
	
	def __exit__(self, type1, value, traceback):
		if hasattr(self, 'session'):
			self.session.close()

	def get(self, req):
		response = self.session.get('/'.join([self.way,req]))
		response.raise_for_status()
		return response.json()

class Currencies(object):
	"""list of currencies with amasing unique Currency ID(Cur_ID)
	developers in nbrb know nothing about ISO
	"""
	def __init__(self, session):
		super(Currencies, self).__init__()
		self.list = session.get("currencies")

	def __new__(self, session):
		if not hasattr(self, 'instance'):
			self.instance = super(Currencies, self).__new__(self)
		return self.instance

	def find_cur_id(self,curr):
		for inst in self.list:	
			if inst.get("Cur_Code") == curr: return inst.get("Cur_ID")
			if inst.get("Cur_Abbreviation") == curr: return inst.get("Cur_ID")
		return ""	

class Rates(object):
	"""get rates object
	modes (*optional): 
	cur_id* : currency code
	parammode : cur_id type
	  0: unique nbrb, 1: numeric code ISO 4217, 2: alphabetic code ISO 4217
	  (https://en.wikipedia.org/wiki/ISO_4217)
	periodicity* : period type( 0 : daily, 1 : monthly)
	ondate* : YYYY-MM-DD 
	"""
	def __init__(self, session):
		super(Rates, self).__init__()
		self.session = session

	def requests_str(self, **kwargs):
		cur_id = kwargs.get("cur_id") 
		return "rates{}?{}".format(
			"/{}".format(cur_id) if cur_id else "",
			"&".join(["{}={}".format(key,val) for key, val in kwargs.items() if key != "cur_id"]))

	def get(self, **kwargs):
		req = self.requests_str(**kwargs)
		print(req)
		return self.session.get(req)

class Dynamics(object):
	"""get rates in period object
	cur_id : unique nbrb currency code
	startdate : YYYY-MM-DD 
	enddate : YYYY-MM-DD 
	"""
	def __init__(self, session):
		super(Dynamics, self).__init__()
		self.session = session
	
	def get(self,cur_id,startdate,enddate):
		req = "rates/dynamics/{}?startdate={}&enddate={}".format( cur_id,startdate,enddate)
		return  (self.session.get(req))