# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

import re
import threading

class CommfilterPlugin(octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin):

	def __init__(self):
		self._regex_mutex = threading.RLock()
		self._regexes = dict(
			queuing=None,
			sending=None
		)

	def initialize(self):
		self._reset_regexes()

	def _reset_regexes(self):
		with self._regex_mutex:
			for phase in ("queuing", "sending"):
				patterns = self._settings.get(["regex", phase])
				if not patterns:
					continue

				valid = []
				for pattern in patterns:
					try:
						re.compile(pattern)
					except:
						self._logger.warn("Invalid pattern: {}".format(pattern))
					else:
						valid.append(pattern)

				if valid:
					full_pattern = "|".join(valid)
					self._logger.debug("Full regex pattern: {}".format(full_pattern))
					self._regexes[phase] = re.compile(full_pattern)
				else:
					self._regexes[phase] = None

	##~~ Settings Plugin

	def get_settings_defaults(self):
		return dict(
			gcode=dict(
				queuing=[],
				sending=[]
			),
			regex=dict(
				queuing=[],
				sending=[]
			),
			command_type=dict(
				queuing=[],
				sending=[]
			)
		)

	def on_settings_save(self, data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		self._reset_regexes()

	##~~ Asset Plugin

	def get_assets(self):
		return dict(
			js=["js/commfilter.js"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			commfilter=dict(
				displayName="Commfilter Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="OctoPrint",
				repo="OctoPrint-Commfilter",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/OctoPrint/OctoPrint-Commfilter/archive/{target_version}.zip"
			)
		)

	def handle_command(self, comm, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if phase not in ("queuing", "sending"):
			# unhandled phase, keep
			return

		with self._regex_mutex:
			regex = self._regexes.get(phase, None)
		gcodes = self._settings.get(["gcode", phase])
		command_types = self._settings.get(["command_type", phase])

		if gcode and gcode in gcodes or cmd_type and cmd_type in command_types or regex and regex.search(cmd):
			# strip
			self._logger.debug("Stripped: {} (Type: {}, GCODE: {})".format(cmd, cmd_type, gcode))
			return None,
		else:
			# keep
			return


__plugin_name__ = "Commfilter"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = CommfilterPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.handle_command,
		"octoprint.comm.protocol.gcode.sending": __plugin_implementation__.handle_command
	}

