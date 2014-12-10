#!python2.6
# coding: utf-8
# This module provides a class that control General MIDI.
# This module has been tested on python ver.2.6.6.
# It need MIDIIO.dll(http://openmidiproject.sourceforge.jp/MIDIIOLibrary.html/)
# ver1.2006
# (C) 2014 Matsuda Hiroaki

import ctypes
import struct

class MIDIStructure(ctypes.Structure):
    _fields_ = [ ("m_pDeviceHandle", ctypes.c_void_p),
                 ("m_pDeviceName", ctypes.c_char_p),
                 ("m_lMode", ctypes.c_long),
                 ("m_pSysxHeader", ctypes.c_void_p),
                 ("m_bStarting", ctypes.c_long),
                 ("m_pBuf", ctypes.POINTER(ctypes.c_ubyte)),
                 ("m_lBufSize", ctypes.c_long),
                 ("m_lReadPosition", ctypes.c_long),
                 ("m_lWritePosition", ctypes.c_long),
                 ("m_bBufLocke", ctypes.c_long),
                 ("m_byRunningStatus", ctypes.c_ubyte)]
