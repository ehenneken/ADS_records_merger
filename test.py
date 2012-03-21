# coding=UTF-8
# Copyright (C) 2011, The SAO/NASA Astrophysics Data System
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
@author: Giovanni Di Milia and Benoit Thiell
File containing an example of the steps that should be taken (and better coded) before using the merger
'''

import libxslt
import libxml2

import sys
sys.path.append('/proj/ads/soft/python/lib/site-packages')
sys.path.append('/proj/adsx/invenio/lib/python')

from ads.ADSExports import ADSRecords

from merger import merge_records_xml

XSLT = 'misc/AdsXML2MarcXML_v2.xsl'


def merge_bibcodes(bibcodes, verbose=False):
    """
    Returns a merged version of the record identified by bibcode.
    """
    # Extract the record from ADS.
    records = ADSRecords()
    for bibcode in bibcodes:
        records.addCompleteRecord(bibcode)
    ads_xml_obj = records.export()
    
    # Convert to MarcXML.
    stylesheet = libxslt.parseStylesheetDoc(libxml2.parseFile(XSLT))
    xml_object = stylesheet.applyStylesheet(ads_xml_obj, None)
    # Convert to bibrecord.
    # TODO: We need to allow bibrecord to accept libxml2 objects.
    marcxml = xml_object.serialize(encoding='utf-8')
    
    return merge_records_xml(marcxml, verbose)



if __name__ == '__main__':
    merged_record = merge_bibcodes(['1999PASP..111..438F'], verbose=True)
    #print bibrecord.record_xml_output(merged_record)
