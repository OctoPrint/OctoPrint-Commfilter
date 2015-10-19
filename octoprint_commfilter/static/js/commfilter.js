/*
 * OctoPrint, the snappy web interface for your 3D printer
 * Copyright (C) 2015  The OctoPrint Developers
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

$(function() {
    function CommfilterViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];

        self.settings = undefined;

        self.onBeforeBinding = function () {
            self.settings = self.settingsViewModel.settings;

            var readSeparated = function(entry, phase) {
                var sep = ", ";
                if (entry == "regex") {
                    sep = "\n";
                }
                return self.settings.plugins.commfilter[entry][phase]().join(sep);
            };
            var writeSeparated = function(entry, phase, value) {
                var sep = ",";
                if (entry == "regex") {
                    sep = "\n";
                }
                return self.settings.plugins.commfilter[entry][phase](splitTextToArray(value, sep, true));
            };

            _.each(["gcode", "regex", "command_type"], function(entry) {
                _.each(["queuing", "sending"], function(phase) {
                    self[entry + "_" + phase] = ko.computed({
                        read: function() { return readSeparated(entry, phase); },
                        write: function(value) { writeSeparated(entry, phase, value); }
                    });
                });
            });

        };
    }

    // view model class, parameters for constructor, container to bind to
    ADDITIONAL_VIEWMODELS.push([
        CommfilterViewModel,
        ["settingsViewModel"],
        ["#settings_plugin_commfilter"]
    ]);
});
