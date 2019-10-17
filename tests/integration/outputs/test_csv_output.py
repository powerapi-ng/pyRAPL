# MIT License
# Copyright (c) 2019, INRIA
# Copyright (c) 2019, University of Lille
# All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import pytest
import pyfakefs

import os

from pyRAPL import Result
from pyRAPL.outputs import CSVOutput

def test_add_2_result_in_empty_file(fs):
    """
    Use a CSVOutput instance to write 2 result in an empty csv file named 'toto.csv'
    Each result contains power consumption of two sockets

    Test if:
      - Before calling the save method, the csv file contains only the header
      - After calling the save method, the csv file contains 4 lines containing the result values
    """
    output = CSVOutput('toto.csv')
    result_list = [
        Result('toto', 0, 0.1, [0.1111, 0.2222], [0.3333, 0.4444]),
        Result('titi', 0, 0.2, [0.5555, 0.6666], [0.7777, 0.8888]),
    ]

    for result in result_list:
        output.add(result)

    assert os.path.exists('toto.csv')

    csv_file = open('toto.csv', 'r')
    assert csv_file.readline() == 'label,timestamp,duration,pkg,dram,socket\n'

    output.save()
    for result in result_list:
        line1 = f"""{result.label},{result.timestamp},{result.duration},{result.pkg[0]},{result.dram[0]},0\n"""
        line2 = f"""{result.label},{result.timestamp},{result.duration},{result.pkg[1]},{result.dram[1]},1\n"""

        assert line1 == csv_file.readline()
        assert line2 == csv_file.readline()
    assert csv_file.readline() == ''


def test_add_2_result_in_non_empty_file(fs):
    """
    Use a CSVOutput instance to write 2 result in an non empty csv file named 'toto.csv'
    Each result contains power consumption of two sockets

    before adding result, the csv file contains a header an a line of result containing only 0 values

    Test if:
      - Before calling the save method, the csv file contains only the header and one line
      - After calling the save method, the csv file contains 4 lines containing the result values
    """

    fs.create_file('toto.csv', contents='label,timestamp,duration,pkg,dram,socket\n0,0,0,0,0,0\n')
    output = CSVOutput('toto.csv')

    result_list = [
        Result('toto', 0, 0.1, [0.1111, 0.2222], [0.3333, 0.4444]),
        Result('titi', 0, 0.2, [0.5555, 0.6666], [0.7777, 0.8888]),
    ]

    for result in result_list:
        output.add(result)

    assert os.path.exists('toto.csv')

    csv_file = open('toto.csv', 'r')
    assert csv_file.readline() == 'label,timestamp,duration,pkg,dram,socket\n'
    assert csv_file.readline() == '0,0,0,0,0,0\n'
    assert csv_file.readline() == ''

    output.save()
    for result in result_list:
        line1 = f"""{result.label},{result.timestamp},{result.duration},{result.pkg[0]},{result.dram[0]},0\n"""
        line2 = f"""{result.label},{result.timestamp},{result.duration},{result.pkg[1]},{result.dram[1]},1\n"""

        assert line1 == csv_file.readline()
        assert line2 == csv_file.readline()
    assert csv_file.readline() == ''


def test_add_2_result_in_non_empty_file_non_append(fs):
    """
    Use a CSVOutput instance to overwrite 2 results on a non empty csv file named 'toto.csv'
    Each result contains power consumption of two sockets

    before adding result, the csv file contains a header an a line of result containing only 0 values

    Test if:
      - Before calling the save method, the csv file contains only the header and one line
      - After calling the save method, the csv file contains 2 lines containing the new results values
    """

    fs.create_file('toto.csv', contents='label,timestamp,duration,pkg,dram,socket\n0,0,0,0,0,0\n')
    output = CSVOutput('toto.csv', append='')

    result_list = [
        Result('toto', 0, 0.1, [0.1111, 0.2222], [0.3333, 0.4444]),
        Result('titi', 0, 0.2, [0.5555, 0.6666], [0.7777, 0.8888]),
    ]

    for result in result_list:
        output.add(result)

    assert os.path.exists('toto.csv')

    csv_file = open('toto.csv', 'r')
    assert csv_file.readline() == 'label,timestamp,duration,pkg,dram,socket\n'

    output.save()
    for result in result_list:
        line1 = f"""{result.label},{result.timestamp},{result.duration},{result.pkg[0]},{result.dram[0]},0\n"""
        line2 = f"""{result.label},{result.timestamp},{result.duration},{result.pkg[1]},{result.dram[1]},1\n"""

        assert line1 == csv_file.readline()
        assert line2 == csv_file.readline()
    assert csv_file.readline() == ''


def test_two_save_call(fs):
    """
    Use a CSVOutput instance to write 1 result in an empty csv file named 'toto.csv'

    After saving the first result, write another result in the csv file

    Each result contains power consumption of two sockets

    Test if:
      - Before calling the fisrt save method, the csv file contains only the header and one line
      - After calling the fisrt save method, the csv file contains 2 lines containing the result values
      - After calling the second save method, the csv file contains 4 lines containing the results values
    """

    result_list = [
        Result('toto', 0, 0.1, [0.1111, 0.2222], [0.3333, 0.4444]),
        Result('titi', 0, 0.2, [0.5555, 0.6666], [0.7777, 0.8888]),
    ]

    output = CSVOutput('toto.csv')
    assert os.path.exists('toto.csv')
    csv_file = open('toto.csv', 'r')
    assert csv_file.readline() == 'label,timestamp,duration,pkg,dram,socket\n'
    assert csv_file.readline() == ''  # end of file

    result = result_list[0]
    output.add(result)
    output.save()

    line1 = f"""{result.label},{result.timestamp},{result.duration},{result.pkg[0]},{result.dram[0]},0\n"""
    line2 = f"""{result.label},{result.timestamp},{result.duration},{result.pkg[1]},{result.dram[1]},1\n"""

    assert line1 == csv_file.readline()
    assert line2 == csv_file.readline()
    assert csv_file.readline() == ''
    csv_file.close()

    output.add(result_list[1])
    output.save()
    csv_file = open('toto.csv', 'r')

    assert csv_file.readline() == 'label,timestamp,duration,pkg,dram,socket\n'
    for result in result_list:
        line1 = f"""{result.label},{result.timestamp},{result.duration},{result.pkg[0]},{result.dram[0]},0\n"""
        line2 = f"""{result.label},{result.timestamp},{result.duration},{result.pkg[1]},{result.dram[1]},1\n"""

        assert line1 == csv_file.readline()
        assert line2 == csv_file.readline()
    assert csv_file.readline() == ''


def test_add_2_result_in_empty_file_semicolon_separator(fs):
    """
    Use a CSVOutput instance to write 2 result in an empty csv file named 'toto.csv'
    Each result contains power consumption of two sockets
    Each values must be separated with a semicolong

    Test if:
      - Before calling the save method, the csv file contains only the header
      - After calling the save method, the csv file contains 4 lines containing the result values separated with
        semicolon
    """
    output = CSVOutput('toto.csv', separator=';')
    result_list = [
        Result('toto', 0, 0.1, [0.1111, 0.2222], [0.3333, 0.4444]),
        Result('titi', 0, 0.2, [0.5555, 0.6666], [0.7777, 0.8888]),
    ]

    for result in result_list:
        output.add(result)

    assert os.path.exists('toto.csv')

    csv_file = open('toto.csv', 'r')
    assert csv_file.readline() == 'label;timestamp;duration;pkg;dram;socket\n'

    output.save()
    for result in result_list:
        line1 = f"""{result.label};{result.timestamp};{result.duration};{result.pkg[0]};{result.dram[0]};0\n"""
        line2 = f"""{result.label};{result.timestamp};{result.duration};{result.pkg[1]};{result.dram[1]};1\n"""

        assert line1 == csv_file.readline()
        assert line2 == csv_file.readline()
    assert csv_file.readline() == ''
