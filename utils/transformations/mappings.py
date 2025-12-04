import os
from datetime import date
from pathlib import Path

# Column Mappings for Source Datasets for use in transformations

def get_maritime_heritage_column_mappings():
	maritime_heritage_column_mapping = {
		'Vessel Name': 'vesselName',
		'Date of Wreck': 'dateOfWreck',
		'Event': 'event',
		'Location of wreck': 'locationOfwreck',
		'Tonnage': 'tonnage',
		'Length (FT)': 'lengthInFeet',
		'Breadth (FT)': 'breadthInFeet',
		'depth (ft)': 'depthInFeet',
		'Masts': 'masts',
		'Decks': 'decks',
		'Hull': 'hull',
		'Description': 'description',
		'Story': 'story',
		'Vessel Type': 'vesselType',
		'Type of event': 'typeOfEvent',
		'Nature of Event': 'natureOfEvent',
		'Cause of Event': 'causeOfEvent',
		'Cargo': 'cargo',
		'Lives Lost': 'livesLost',
		'Voyage from': 'voyageFrom',
		'Voyage To': 'voyageTo',
		'Remarks': 'remarks',
		'Built At': 'builtAt',
		'Date Built': 'dateBuilt',
		'Official Number': 'officialNumber',
		'Registered at': 'registeredat',
		'Date Registered': 'dateRegistered',
		'Propulsion': 'propulsion',
		'Rig': 'rig',
		'Details': 'details'
	}
	return maritime_heritage_column_mapping

def get_nj_maritime_shipwreck_database_mappings ():
	nj_maritime_shipwreck_database_mappings = {
		'SHIPS NAME': 'shipsName',
		'AKA': 'aka',
		'SHIPS OWNER': 'shipsOwner',
		'VESSEL TYPE': 'vesselType',
		'YEAR BUILT': 'yearBuilt',
		'WHERE BUILT': 'whereBuilt',
		'DATE LOST': 'dateLost',
		'YEAR': 'year',
		'MNTH': 'month',
		'DAY': 'day',
		'LOCATION LOST': 'locationLost',
		'LATITUDE': 'latitude',
		'LONGITUDE': 'longitude',
		'CAUSE OF LOSS': 'causeOfLoss',
		'CONSTRUCTION': 'construction',
		'FLAG': 'flag',
		'LENGTH': 'length',
		'BEAM': 'beam',
		'DRAFT': 'draft',
		'GROSS TONNAGE': 'grossTonnage',
		'NET TONNAGE': 'netTonnage',
		'HOME HAILING PORT': 'homeHailingPort',
		'DEPARTURE PORT': 'departurePort',
		'DESTINATION PORT': 'destinationPort',
		'MASTER': 'master',
		'NUM CREW': 'numberOfCrew',
		'NUM PASS': 'numPass',
		'LIVES LOST': 'livesLost',
		'SHIP VALUE': 'shipValue',
		'CARGO VALUE': 'cargoValue',
		'NATURE OF CARGO': 'natureOfCargo',
		'USLSS STATION NAME': 'uslssStationName',
		'MAP': 'map',
		'LOST': 'lost',
		'PHOTO ON FILE': 'photoOnFile',
		'MISC INFORMATION': 'miscInformation',
	}
	return nj_maritime_shipwreck_database_mappings

def get_nj_maritime_shipwreck_database_column_subset ():
	nj_shipwreck_database_subset = [
		'shipsName',
		'shipsOwner',
		'yearBuilt',
		'vesselType',
		'dateLost',
		'year',
		'month',
		'day',
		'latitude',
		'longitude',
		'locationLost',
		'causeOfLoss',
		'departurePort',
		'destinationPort'
	]
	return nj_shipwreck_database_subset

def get_emodnet_ha_heritage_shipwrecks_column_mappings():
	emodnet_ha_heritage_shipwrecks_mappings = {
		'OBJECTID': 'objectID',
		'SOURCE_ID': 'sourceID',
		'COUNTRY': 'country',
		'NAME': 'name',
		'LEAST_DEPTH': 'minDepth',
		'MAX_DEPTH': 'maxDepth',
		'DEPTH_INFO': 'depthInfo',
		'DEPTH_PREC': 'depthPrecision',
		'OBJECT_LENGTH': 'objectLength',
		'LOC_PREC': 'locationPrecision',
		'SITE_AREA': 'siteArea',
		'SINK_CONTEXT': 'sinkContext',
		'SINK_YR': 'sinkYear',
		'DATING': 'dating',
		'PERIOD': 'period',
		'STATUTORY_PROT': 'statutoryProt',
		'OBJ_DESC': 'objectDescription',
		'SHIP_CHAR': 'shipChar',
		'OBJ_TYPE': 'objectType',
		'EST_TONNAGE': 'estimatedTonnage',
		'PLACE_ORIG': 'originLocation',
		'PLACE_DEST': 'destination',
		'ARTEFACTS': 'artifacts',
		'COAST_DIST': 'coastDist',
		'SOURCE_INFO': 'sourceInfo',
		'REFERENCE': 'reference',
		'WEBSITE1': 'website',
		'WEBSITE2': 'websiteAlt'
	}
	return emodnet_ha_heritage_shipwrecks_mappings