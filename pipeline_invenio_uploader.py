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
A custom version of the invenio bibupload module 
to upload directly in the Invenio DB the result of the merger
'''
import sys

from invenio import bibupload

def bibupload_merger(merged_bibrecords, logger, opt_mode="replace_or_insert", pretend=False):
    """Function to upload directly in the Invenio DB"""
    def write_message(msg, stream=sys.stdout, verbose=False):
        """Custom definition of write_message 
        to override the Invenio log"""
        #logger.info(msg)
        pass
    #I override the function inside Invenio
    bibupload.write_message = write_message
    
    for bibrecord in merged_bibrecords:
        bibupload.bibupload(bibrecord, opt_tag=None, opt_mode=opt_mode,
                  opt_stage_to_start_from=1, opt_notimechange=0, oai_rec_id = "", pretend=pretend)