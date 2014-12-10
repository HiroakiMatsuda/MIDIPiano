#!python2.6
# coding: utf-8
# This module provides a class that control General MIDI.
# This module has been tested on python ver.2.6.6.
# It need MIDIIO.dll(http://openmidiproject.sourceforge.jp/MIDIIOLibrary.html/)
# ver1.2006
# (C) 2014 Matsuda Hiroaki

import ctypes
import midi_structure
import struct

from os import path
filepath = path.dirname(path.abspath( __file__ ))

midiio = ctypes.windll.LoadLibrary(filepath + "/MIDIIO.dll")

def get_device_num():

    return midiio.MIDIOut_GetDeviceNum()

def get_device_name(device_id, buffer_length = 64):

    device_name = ctypes.create_string_buffer(buffer_length)
    ret = midiio.MIDIOut_GetDeviceNameA(device_id,
                                        device_name,
                                        buffer_length)

    if ret > 0:
        index = device_name.raw.find("\0")

        if index >= 0:
            return device_name.raw[:index]

        elif index == -1:
            return device_name.raw
                
    else:
        return ""

def get_device_name_list(device_num):

    device_name_list = []
            
    for device_id in range(device_num):
                
        device_name = get_device_name(device_id)
        device_name_list.append(device_name)

    return device_name_list

class MIDIOut():

    def __init__(self, device_name):

        self.midi_device = self.open_midi_device(device_name)

    def open_midi_device(self, device_name):
        
        midiio.MIDIOut_OpenA.restype = ctypes.POINTER(midi_structure.MIDIStructure)
        midi_device = midiio.MIDIOut_OpenA(device_name)

        return midi_device

    def close_midi_device(self):

        midiio.MIDIOut_Close.argtypes = [ctypes.POINTER(midi_structure.MIDIStructure)]
        ret = midiio.MIDIOut_Close(self.midi_device)
    
        if ret < 0:
            raise IOError

    def press_key(self, channel, key, velocity):
        
        channel = struct.pack('>B', 0x90 | channel)
        key = struct.pack('>B', key)
        velocity = struct.pack('>B', velocity)

        message = '%s%s%s' %(channel, key, velocity)
        midiio.MIDIOut_PutMIDIMessage(self.midi_device, message, 3)

    def release_key(self, channel, key, velocity):
        
        channel = struct.pack('>B', 0x80 | channel)
        key = struct.pack('>B', key)
        velocity = struct.pack('>B', velocity)
        
        message = '%s%s%s' %(channel, key, velocity)
        midiio.MIDIOut_PutMIDIMessage(self.midi_device, message, 3)

    def program_change(self, channel, tone):
        
        program_change = struct.pack('>B', 0xC0 | channel) \
                       + struct.pack('>B', tone)

        midiio.MIDIOut_PutMIDIMessage(self.midi_device, program_change, 2)

if __name__ == '__main__':

    import midi_out

    device_num = midi_out.get_device_num()
    device_list = midi_out.get_device_name_list(device_num)

    for num, name in enumerate(device_list):
        print("Device %d: %s" %(num, name))

    midiout = midi_out.MIDIOut(device_list[0])

    import time

    midiout.program_change(0, 0)
    
    key = 0x60
    for i in range(8):
        midiout.press_key(0, 0x60 + i, 0x64)
        time.sleep(0.8)
        midiout.release_key(0, 0x60 + i, 0x00)

    midiout.close_midi_device()
