#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  testinglength.py
#  
#  Copyright 2024  <instrumentgroup@instrument>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import mido
from mido import MidiFile


def get_midi_length():
    """
    Calculate the length of the MIDI file in seconds.
    
    :param midi_file_path: Path to the MIDI file
    :return: Length of the MIDI file in seconds
    """
    midi_file = MidiFile('/home/instrumentgroup/Downloads/wii.mid')
    print(midi_file.length)
    print('slow')
    

get_midi_length()

