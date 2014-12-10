#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file MIDIPiano.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

import MIDI

from pymidiio import midi_out

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
midipiano_spec = ["implementation_id", "MIDIPiano", 
		 "type_name",         "MIDIPiano", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "Hiroaki Matsuda", 
		 "category",          "MID", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.channel", "0",
		 "conf.default.tone", "0",
		 "conf.default.delay_time", "0.0",
		 "conf.default.device_name", "Microsoft GS Wavetable Synth",
		 "conf.__widget__.channel", "text",
		 "conf.__widget__.tone", "text",
		 "conf.__widget__.delay_time", "text",
		 "conf.__widget__.device_name", "text",
		 ""]
# </rtc-template>

##
# @class MIDIPiano
# @brief ModuleDescription
# 
#


def play_sound(midiout, channel, message, delay_time):

        if channel == -1 or channel == message.ch.channel:
                
                if message.event == 'Note On':
                        print("Event:%12s Ch:%2d Note:%2d Vel:%3d" %(message.event,
                                                                     message.ch.channel,
                                                                     message.ch.note_number,
                                                                     message.ch.velocity))
                        time.sleep(delay_time)
                        midiout.press_key(message.ch.channel,
                                          message.ch.note_number,
                                          message.ch.velocity)
                      
                elif message.event == 'Note Off':
                        print("Event:%12s Ch:%2d Note:%2d Vel:%3d" %(message.event,
                                                                     message.ch.channel,
                                                                     message.ch.note_number,
                                                                     message.ch.velocity))
                        time.sleep(delay_time)
                        midiout.release_key(message.ch.channel,
                                            message.ch.note_number,
                                            message.ch.velocity)
       
class DataListener(OpenRTM_aist.ConnectorDataListenerT):
        
        def __init__(self, name, midiout, channel, delay_time):
                self._name = name
                self.midiout = midiout
                self.channel = channel
                self.delay_time = delay_time

        def __del__(self):
                print("dtor of %s" %(self._name))

        def __call__(self, info, cdrdata):
                data = OpenRTM_aist.ConnectorDataListenerT.__call__(self,
                                                                    info,
                                                                    cdrdata,
                                                                    MIDI.MIDIMessage(RTC.Time(0, 0),
                                                                                     '',
                                                                                     MIDI.ChannelMessage(0, 0, 0, 0, 0, 0, 0, 0, 0),
                                                                                     MIDI.SystemMessage("", 0,"","","","","",
                                                                                                        "","","","", 0, 0, 0,
                                                                                                         0, 0, 0, 0, 0, 0, 0)))
                
                play_sound(self.midiout, self.channel, data, self.delay_time)

class MIDIPiano(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
          
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
		
		self._d_message = MIDI.MIDIMessage(RTC.Time(0,0),
                                                   '',
                                                   MIDI.ChannelMessage(0, 0, 0, 0, 0, 0, 0, 0, 0),
                                                   MIDI.SystemMessage("", 0,"","","","","",
                                                                      "","","","", 0, 0, 0,
                                                                       0, 0, 0, 0, 0, 0, 0))

                self._midi_inIn = OpenRTM_aist.InPort("midi_in", self._d_message)


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  channel
		 - DefaultValue: 0
		"""
		self._channel = [0]
		"""
		
		 - Name:  tone
		 - DefaultValue: 0
		"""
		self._tone = [0]
		"""
		
		 - Name:  delay_time
		 - DefaultValue: 0.0
		"""
		self._delay_time = [0.0]
		"""
		
		 - Name:  device_name
		 - DefaultValue: Microsoft GS Wavetable Synth
		"""
		self._device_name = ['Microsoft GS Wavetable Synth']
		
		# </rtc-template>

	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("channel", self._channel, "0")
		self.bindParameter("tone", self._tone, "0")
		self.bindParameter("delay_time", self._delay_time, "0.0")
		self.bindParameter("device_name", self._device_name, "Microsoft GS Wavetable Synth")
		
		# Set InPort buffers
		self.addInPort("midi_in",self._midi_inIn)
		
		# Set OutPort buffers
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports

		
		return RTC.RTC_OK

	def onStartup(self, ec_id):
                device_num = midi_out.get_device_num()
                device_list = midi_out.get_device_name_list(device_num)

                for num, name in enumerate(device_list):
                        print("Find Device %d: %s" %(num, name))

                print("MIDI Device: %s" %(self._device_name[0]))
                print("Ch: %s Tone: %s Delay: %s" %(self._channel[0],
                                                    self._tone[0],
                                                    self._delay_time[0]))

                
                self.midiout = midi_out.MIDIOut(self._device_name[0])
                self.midiout.program_change(0, self._tone[0])

		self._midi_inIn.addConnectorDataListener(OpenRTM_aist.ConnectorDataListenerType.ON_RECEIVED,
                                                         DataListener("ON_RECEIVED",
                                                                      self.midiout,
                                                                      self._channel[0],
                                                                      self._delay_time[0]))

		return RTC.RTC_OK
	
	def onShutdown(self, ec_id):
	
		return RTC.RTC_OK
	
	def onActivated(self, ec_id):

		return RTC.RTC_OK
	
	def onDeactivated(self, ec_id):
	
		return RTC.RTC_OK
	
	#def onExecute(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	def onAborting(self, ec_id):
	
		return RTC.RTC_OK
	
def MIDIPianoInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=midipiano_spec)
    manager.registerFactory(profile,
                            MIDIPiano,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    MIDIPianoInit(manager)

    # Create a component
    comp = manager.createComponent("MIDIPiano")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

