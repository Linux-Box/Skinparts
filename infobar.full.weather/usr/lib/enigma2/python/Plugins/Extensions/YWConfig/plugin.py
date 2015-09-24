# Yahoo weather config converter
# Copyright (c) 2boom 2013
# v.0.1-r0
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# mod by jpuigs (7-april-2015) to suit own needs
#
from Plugins.Plugin import PluginDescriptor
from Tools.Directories import fileExists
from Components.Console import Console
from Components.ActionMap import ActionMap
from Components.config import getConfigListEntry, ConfigText, ConfigSubsection, config, configfile
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
import os
import enigma
####################################################################
config.plugins.yweather = ConfigSubsection()
config.plugins.yweather.weather_city = ConfigText(default="753692", visible_width = 70, fixed_size = False)
####################################################################
class yweather_setup(ConfigListScreen, Screen):
	skin = """
<screen name="yweather_setup" position="center,center" size="650,190" backgroundColor="white">
  <widget position="15,10" size="620,75" name="config" scrollbarMode="no" font="Regular; 30" itemHeight="50" foregroundColor="white" backgroundColor="background" />
  <eLabel position="20,80" size="610,3" backgroundColor="grey" zPosition="5" />
 <eLabel position="16,94" size="610,30" backgroundColor="white" zPosition="5" text="Podras encontrar tu ID en http://metrixweather.open-store.net/" foregroundColor="black" halign="center" font="Regular; 20" />
  <widget source="key_red" render="Label" position="95,135" zPosition="2" size="168,50" font="Regular; 25" halign="center" valign="center" backgroundColor="red" foregroundColor="white" transparent="0" />
  <widget source="key_blue" render="Label" position="352,135" zPosition="2" size="168,50" font="Regular; 25" halign="center" valign="center" backgroundColor="blue" foregroundColor="white" transparent="0" />
</screen>"""
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.Console = Console()
		self.setTitle("Yahoo! Tiempo Configuracion")
                self.list = []
		self.list.append(getConfigListEntry("ID de tu Ciudad", config.plugins.yweather.weather_city))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = Label("Cerrar")
		self["key_blue"] = Label("Guardar")
		if not self.check():
			self.setTitle("YWeather.py no encontrado")
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"blue": self.save,
			"ok": self.save
		}, -2)
		
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)
		
	def check(self):
		if fileExists("/usr/lib/enigma2/python/Components/Converter/YWeather.py"):
			return True
		return False

	def save(self):
		wcity = ''
		if self.check():
			config.plugins.yweather.weather_city.save()
			configfile.save()
			if fileExists("/tmp/yweather.xml"):
                        	os.remove('/tmp/yweather.xml')
			self.mbox = self.session.open(MessageBox,("ID Ciudad Guardada!"), MessageBox.TYPE_INFO, timeout = 3 )
			self.cancel()
		else:
			self.setTitle("YWeather.py mp encontrado")
##############################################################################
def main(session, **kwargs):
	session.open(yweather_setup)
##############################################################################
def Plugins(**kwargs):
	return PluginDescriptor(name="Yahoo! Weather SkinPart", description="Configura ID de tu Ciudad en Yahoo! Weather", where = [PluginDescriptor.WHERE_PLUGINMENU], icon="icon.png", fnc=main)
	