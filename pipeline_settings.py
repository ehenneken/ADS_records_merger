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
Settings file for pipeline
'''

from os.path import dirname, abspath
BASEDIR = dirname(abspath(__file__)) + '/'

VERBOSE = True

#base path for the output of the procedure
BASE_OUTPUT_PATH = BASEDIR + 'out'

#list of files that MUST be in each output directory
BASE_FILES = {'new':'bibcodes_to_extract_new_mod.dat', 'del':'bibcodes_to_extract_del.dat', 'done':'bibcodes_extracted.dat', 'prob':'bibcodes_with_problems.dat'}

#file where to store the extraction name log
EXTRACTION_FILENAME_LOG = 'extraction_name_log.txt'
EXTRACTION_BASE_NAME = 'extraction_'
EXTRACTION_READY_TO_UPLOAD_MESSAGE = 'ready_to_upload'
EXTRACTION_UPLOADED_MESSAGE = 'uploaded'

#files with list of bibcodes and timestamps
#AST
BIBCODES_AST = '/proj/ads/abstracts/ast/load/current/index.status'
#PHY
BIBCODES_PHY = '/proj/ads/abstracts/phy/load/current/index.status'
#GEN
BIBCODES_GEN = '/proj/ads/abstracts/gen/load/current/index.status'
#PRE
BIBCODES_PRE = '/proj/ads/abstracts/pre/load/current/index.status'
#The connection between published bibcodes and preprint
ARXIV2PUB = '/proj/ads/abstracts/config/links/preprint/arxiv2pub.list'

#style sheet path
STYLESHEET_PATH = BASEDIR + 'misc/AdsXML2MarcXML_v2.xsl'

#base name for the file of bibcodes to delete
BIBCODE_TO_DELETE_OUT_NAME = 'marcxml_to_delete'
#base name for the marcXML files
MARCXML_FILE_BASE_NAME = 'marcxml_to_add'
#extension for marcxml files
MARCXML_EXTENSION = '.xml'

#maximum number of bibcodes per group of extraction -> it means that this is also the maximum number of bibcodes per file of marcxml
NUMBER_OF_BIBCODES_PER_GROUP = 1000

#maximum amount of bibcodes that can be skipped for each group
MAX_SKIPPED_BIBCODES = NUMBER_OF_BIBCODES_PER_GROUP / 2

#maximum number of worker processes that have to run
NUMBER_WORKERS = 6

#maximum number of groups of bibcodes that each worker can process before dying
MAX_NUMBER_OF_GROUP_TO_PROCESS = 3

