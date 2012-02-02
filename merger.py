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
@author: Giovanni Di Milia,
The ads merger is a tool that combines two elements and returns
the combined element.
'''

import merger_settings
from merger_settings import msg
from errors import ErrorsInBibrecord, OriginValueNotFound

def merge(create_records_output, verbose=False):
    """Main function: takes in input a whole record containing the
    different flavors of metadata

    @param create_records_output: the output of bibrecord.create_records()
    @return: a merged record
    """
    # The record is in "bibrecord" format (mix of tuples and dictionaries)
    # Check if there were errors in the conversion to bibrecord format and extract only the metadata from the tuples
    records = []
    for record, error_code, error in create_records_output:
        if error_code == 0:
            raise ErrorsInBibrecord(error)
        else:
            records.append(record)

    msg('Merging %d records.' % len(records), verbose)

    # If we have only one version, we don't need to merge.
    if len(records) == 1:
        return records[0]

    # Otherwise merge the single records
    # First of all group the data per field
    grouped_record = group_fields(records)

    # Pass each field to the function that takes care of merge all the versions together
    # and append the result to the main metadata container
    merged_record = {}
    for tag, field_versions in grouped_record.items():
        # TODO Why is this a list in a list?
        merged_record[tag] = merger_field_manager(tag, field_versions, verbose)[0]

    # Correct the field positions.
    record_reorder(merged_record)

    return merged_record

def merger_field_manager(tag, subfields, verbose):
    """function that manages the merging of multiple version of a field taking care of combining all the versions"""
    # Group the subfields per different indicators to merge the subfields inside the different groups
    grouped_subfields = group_subfields_per_indicator(subfields)
    # For each group merge the subfields in it
    merged_fields = []
    for subfield_group in grouped_subfields:
        cur_subfields = grouped_subfields[subfield_group]
        # If there is more than one version, merge the different versions
        if len(cur_subfields) > 1:
            # Current version of the field initially is the first version of the record
            current_version = cur_subfields[0]
            # Merge it with all the other versions
            for subfield in cur_subfields[1:]:
                current_version = merge_field(current_version, subfield, tag, verbose)
            merged_fields.append(current_version)
        # If there is only one version of the field, do nothing
        else:
            merged_fields.append(cur_subfields[0])
    return merged_fields

def merge_field(field1, field2, tag, verbose):
    """Function that merges two fields with a merging function"""
    # Retrieve the merging function (that is a representation of the merging
    # rule) for the specified field
    merging_func = eval(merger_settings.MERGING_RULES[merger_settings.MARC_TO_FIELD[tag]])
    msg('Merging tag %s with function %s.' % (tag, merging_func.func_name), verbose)
    try:
        return merging_func(field1, field2, tag)
    except OriginValueNotFound:
        raise

def group_fields(records):
    """Function that groups together the fields from different version of record
    i.e. if there are 2 version of field 100 there will be in the dictionary
    {'100':[[__version 1__], [__version 2__]]}"""
    grouped_record = {}
    for record in records:
        for tag, fields in record.items():
            grouped_record.setdefault(tag, []).append(fields)
    return grouped_record

def group_subfields_per_indicator(subfields):
    """Function that groups a bunch of subfield per indicator"""
    grouped_subfields = {}
    for subfield in subfields:
        # Extract the indicators
        indicator1 = subfield[0][1]
        if indicator1 == ' ':
            indicator1 = '_'
        indicator2 = subfield[0][2]
        if indicator2 == ' ':
            indicator2 = '_'
        grouped_subfields.setdefault(indicator1+indicator2, []).append(subfield)
    return grouped_subfields

def record_reorder(record):
    """
    Resets the field positions to default order of increasing tags. Note that
    the subfield order is kept untouched.
    """
    current_position = 1
    for tag in sorted(record.keys()):
        for index, field in enumerate(record[tag]):
            record[tag][index] = (field[0], field[1], field[2], field[3], current_position)
            current_position += 1
