#!/usr/bin/env python3
# -*- coding: utf-8 -*-
VER = '8.2.0.4 [00117]'

"""
    decode-config.py - Backup/Restore Tasmota configuration data

    Copyright (C) 2020 Norbert Richter <nr@prsolution.eu>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


Requirements:
    - Python 3.x and Pip:
        sudo apt-get install python3 python3-pip
        pip3 install requests configargparse

Instructions:
    Execute decode-config with option -d <ip> or <host> to retrieve config data
    from a Tasmota host or use -f <configfile.dmp> to read the configuration
    data from a file previously saved using Tasmota Web-UI

    For further information see 'README.md'

    For help execute command with argument -h (or -H for advanced help)


Usage: decode-config.py [-f <filename>] [-d <host>] [-P <port>]
                        [-u <username>] [-p <password>] [-i <filename>]
                        [-o <filename>] [-t json|bin|dmp] [-E] [-e] [-F]
                        [--json-indent <indent>] [--json-compact]
                        [--json-hide-pw] [--json-show-pw]
                        [--cmnd-indent <indent>] [--cmnd-groups]
                        [--cmnd-nogroups] [--cmnd-sort] [--cmnd-unsort]
                        [-c <filename>] [-S] [-T json|cmnd|command]
                        [-g {Control,Display,Domoticz,Internal,Knx,Light,Management,Mqtt,Power,Rf,Rules,Sensor,Serial,Setoption,Shutter,System,Timer,Wifi,Zigbee} [{Control,Display,Domoticz,Internal,Knx,Light,Management,Mqtt,Power,Rf,Rules,Sensor,Serial,Setoption,Shutter,System,Timer,Wifi,Zigbee} ...]]
                        [--ignore-warnings] [--dry-run] [-h] [-H] [-v] [-V]

    Backup/Restore Tasmota configuration data. Args that start with '--' (eg. -f)
    can also be set in a config file (specified via -c). Config file syntax
    allows: key=value, flag=true, stuff=[a,b,c] (for details, see syntax at
    https://goo.gl/R74nmi). If an arg is specified in more than one place, then
    commandline values override config file values which override defaults.

    Source:
      Read/Write Tasmota configuration from/to

      -f, --file <filename>
                            file to retrieve/write Tasmota configuration from/to
                            (default: None)'
      -d, --device <host>   hostname or IP address to retrieve/send Tasmota
                            configuration from/to (default: None)
      -P, --port <port>     TCP/IP port number to use for the host connection
                            (default: 80)
      -u, --username <username>
                            host HTTP access username (default: admin)
      -p, --password <password>
                            host HTTP access password (default: None)

    Backup/Restore:
      Backup & restore specification

      -i, --restore-file <filename>
                            file to restore configuration from (default: None).
                            Replacements: @v=firmware version from config,
                            @f=device friendly name from config, @h=device
                            hostname from config, @H=device hostname from device
                            (-d arg only)
      -o, --backup-file <filename>
                            file to backup configuration to (default: None).
                            Replacements: @v=firmware version from config,
                            @f=device friendly name from config, @h=device
                            hostname from config, @H=device hostname from device
                            (-d arg only)
      -t, --backup-type json|bin|dmp
                            backup filetype (default: 'json')
      -E, --extension       append filetype extension for -i and -o filename
                            (default)
      -e, --no-extension    do not append filetype extension, use -i and -o
                            filename as passed
      -F, --force-restore   force restore even configuration is identical

    JSON output:
      JSON format specification

      --json-indent <indent>
                            pretty-printed JSON output using indent level
                            (default: 'None'). -1 disables indent.
      --json-compact        compact JSON output by eliminate whitespace
      --json-hide-pw        hide passwords
      --json-show-pw        unhide passwords (default)

    Tasmota command output:
      Tasmota command output format specification

      --cmnd-indent <indent>
                            Tasmota command grouping indent level (default: '2').
                            0 disables indent
      --cmnd-groups         group Tasmota commands (default)
      --cmnd-nogroups       leave Tasmota commands ungrouped
      --cmnd-sort           sort Tasmota commands (default)
      --cmnd-unsort         leave Tasmota commands unsorted

    Common:
      Optional arguments

      -c, --config <filename>
                            program config file - can be used to set default
                            command parameters (default: None)
      -S, --output          display output regardsless of backup/restore usage
                            (default do not output on backup or restore usage)
      -T, --output-format json|cmnd|command
                            display output format (default: 'json')
      -g, --group {Control,Display,Domoticz,Internal,Knx,Light,Management,Mqtt,Power,Rf,Rules,Sensor,Serial,Setoption,Shutter,System,Timer,Wifi,Zigbee}
                            limit data processing to command groups (default no
                            filter)
      --ignore-warnings     do not exit on warnings. Not recommended, used by your
                            own responsibility!
      --dry-run             test program without changing configuration data on
                            device or file

    Info:
      Extra information

      -h, --help            show usage help message and exit
      -H, --full-help       show full help message and exit
      -v, --verbose         produce more output about what the program does
      -V, --version         show program's version number and exit

    Either argument -d <host> or -f <filename> must be given.


Returns:
    0: successful
    1: restore skipped
    2: program argument error
    3: file not found
    4: data size mismatch
    5: data CRC error
    6: unsupported configuration version
    7: configuration file read error
    8: JSON file decoding error
    9: Restore file data error
    10: Device data download error
    11: Device data upload error
    20: python module missing
    21: Internal error
    22: HTTP connection error
    >22: python library exit code
    4xx, 5xx: HTTP errors

"""

class ExitCode:
    """
    Program return codes
    """
    OK = 0
    RESTORE_SKIPPED = 1
    ARGUMENT_ERROR = 2
    FILE_NOT_FOUND = 3
    DATA_SIZE_MISMATCH = 4
    DATA_CRC_ERROR = 5
    UNSUPPORTED_VERSION = 6
    FILE_READ_ERROR = 7
    JSON_READ_ERROR = 8
    RESTORE_DATA_ERROR = 9
    DOWNLOAD_CONFIG_ERROR = 10
    UPLOAD_CONFIG_ERROR = 11
    INVALID_DATA = 12
    MODULE_NOT_FOUND = 20
    INTERNAL_ERROR = 21
    HTTP_CONNECTION_ERROR = 22
    STR = [
        'OK',
        'Restore skipped',
        'Parameter error',
        'File not found',
        'Data size mismatch',
        'Data CRC error',
        'Unsupported version',
        'File read error',
        'JSON read error',
        'Restore data error',
        'Download error',
        'Upload error',
        'Invaid data',
        '', '', '', '', '', '', '',
        'Module not found',
        'Internal error',
        'HTTP connection error'
        ]
    @staticmethod
    def str(code):
        """
        Program return string by code

        @param: code
            int number of code
        """
        if code >= 0 and code < len(ExitCode.STR):
            return ExitCode.STR[code]
        return ''

# ======================================================================
# imports
# ======================================================================
def module_import_error(module):
    """
    Module import error helper
    """
    errstr = str(module)
    print('{}, try "pip3 install {}"'.format(errstr, errstr.split(' ')[len(errstr.split(' '))-1]), file=sys.stderr)
    sys.exit(ExitCode.MODULE_NOT_FOUND)
# pylint: disable=wrong-import-position
import os.path
import sys
import platform
try:
    from datetime import datetime
    import time
    import copy
    import struct
    import socket       # pylint: disable=unused-import
    import re
    import inspect
    import itertools
    import json
    import configargparse
    import requests
    import urllib
    import codecs
except ImportError as err:
    module_import_error(err)
# pylint: enable=wrong-import-position

# ======================================================================
# globals
# ======================================================================
PROG = '{} v{} by Norbert Richter <nr@prsolution.eu>'.format(os.path.basename(sys.argv[0]), VER)

CONFIG_FILE_XOR = 0x5A
BINARYFILE_MAGIC = 0x63576223
STR_ENCODING = 'utf8'
HIDDEN_PASSWORD = '********'
INTERNAL = 'Internal'
VIRTUAL = '*'

DEFAULTS = {
    'source':
    {
        'device':       None,
        'port':         80,
        'username':     'admin',
        'password':     None,
        'tasmotafile':  None,
    },
    'backup':
    {
        'restorefile':  None,
        'backupfile':   None,
        'backupfileformat': 'json',
        'extension':    True,
        'forcerestore': False,
    },
    'jsonformat':
    {
        'jsonindent':   None,
        'jsoncompact':  False,
        'jsonsort':     True,
        'jsonhidepw':   False,
    },
    'cmndformat':
    {
        'cmndindent':   2,
        'cmndgroup':    True,
        'cmndsort':     True,
    },
    'common':
    {
        'output':       False,
        'outputformat': 'json',
        'configfile':   None,
        'dryrun':       False,
        'ignorewarning':False,
        'filter':       None,
    },
}

PARSER = None
ARGS = {}
EXIT_CODE = 0


# ======================================================================
# Settings mapping
# ======================================================================
"""
Settings dictionary

The Tasmota permanent setttings are stored in binary format using
'struct SYSCFG' defined in tasmota/settings.h.

decode-config handles the binary data described by this Settings
dictionary. The processing from/to Tasmota configuration data is
based on this dictionary.


    <setting> = { <name> : <def> }

    <name>: "string"
        key (string)
        for simply identifying value from Tasmota configuration this key has the same
        name as the structure element of tasmota/settings.h

    <def>:  ( <platform>, <format>, <addrdef>, <datadef> [,<converter>] )
        tuple with 4 or 5 objects which describes the format, address and structure
        of the binary source.
        For optional values there are two possibilities: If the definition object is
        mandatory it could be None, for none-mandatory optional objects it can be omit.

            <platform>: <int>
                platform bitmask validation
                determines whether the setting is valid for a platform (bit=1) or not (bit=0)
                bit0=ESP82xx, bit1=ESP32

            <format>:   <formatstring> | <setting>
                data type & format definition

                <formatstring>: <string>
                    defines the use of data at <addrdef>
                    format is defined in 'struct module format string'
                    see
                    https://docs.python.org/3.8/library/struct.html#format-strings
                <setting>:      <setting>
                    A dictionary describes a (sub)setting dictonary
                    and can recursively define another <setting>


            <addrdef>:  <baseaddr> | (<baseaddr>, <bits>, <bitshift>) | (<baseaddr>, <strindex>)
                address definition

                <baseaddr>: <uint>
                    The address (starting from 0) within binary config data.

                <bits>:     <uint>
                    number of bits used (positive integer)

                <bitshift>: <int>
                    bit shift <bitshift>:
                    <bitshift> >= 0: shift the result right
                    <bitshift> <  0: shift the result left

                <strindex>: <int>
                    index into a set of strings delimited by \0


            <datadef>:  <arraydef> | (<arraydef>, <validate> [,cmd])
                data definition

                <arraydef>: None | <dim> | [<dim>] | [<dim> ,<dim>...]
                    None:
                        single value
                    <dim>:  <uint>

                    [<dim>]
                        a one-dimensional array of size <n>

                    [<dim> ,<dim>...]
                        a one- or multi-dimensional array

                <validate>: None | <function>
                    value validation function

                <cmd>:  (<group>, <tasmotacmnd>) - optional
                    Tasmota command definition

                    <group>:        <string>
                        command group
                        There exists two special group names
                        INTERNAL - processed but invisible in group output
                        VIRTUAL  - must be used as group name for nested
                                   dict definition - invisible in group output

                    <tasmotacmnd>:   <function> | (<function>,...)
                        convert function into Tasmota cmnd function


            <converter>:    <readconverter> | (<readconverter>, <writeconverter>) -
                read/write converter

                <readconverter>:    None | <function>
                    Will be used in bin2mapping to convert values read
                    from the binary data object into mapping dictionary
                    None
                        indicates no read conversion
                    <function>
                        to convert value from binary object to JSON.

                <writeconverter>:   None | False | <function>
                    Will be used in mapping2bin to convert values read
                    from mapping dictionary before write to binary
                    data object
                    None
                        indicates no write conversion
                    False
                        False indicates the value is readonly and is not
                        written back into the binary Tasmota data.
                    <function>
                        to convert value from JSON back to binary object


        Common definitions

        <function>: <functionname> | <string> | None
            the name of an object to be called or a string to be evaluated

            <functionname>:
                name will be called with one or two parameter:
                    - The value to be processed
                    - (optional) the current array index (1,n)
                      if an array is defined

            <string>
                A string will be evaluate as is. The following placeholder
                can be used for runtime replacements:
                '$':
                    will be replaced by the object mapping value
                '#':
                    will be replace by array index (if defined)
                '@':
                    can be used to reference another mapping value


        <string>:   'string' | "string"
            characters enclosed by ' or "

        <int>:      integer
             integer number in the range -2147483648 through 2147483647

        <uint>:     unsigned integer
             integer number in the range 0 through 4294967295

"""
# ----------------------------------------------------------------------
# Settings helper
# ----------------------------------------------------------------------
def passwordread(value):
    """
    Password read helper
    """
    return HIDDEN_PASSWORD if ARGS.jsonhidepw else value

def passwordwrite(value):
    """
    Password write helper
    """
    return None if value == HIDDEN_PASSWORD else value

def bitsread(value, pos=0, bits=1):
    """
    Reads bit(s) of a number

    @param value:
        the number from which to read

    @param pos:
        which bit position to read

    @param bits:
        how many bits to read (1 if omitted)

    @return:
        the bit value(s)
    """
    if isinstance(value, str):
        value = int(value, 0)
    if isinstance(pos, str):
        pos = int(pos, 0)

    if pos >= 0:
        value >>= pos
    else:
        value <<= abs(pos)
    if bits > 0:
        value &= (1<<bits)-1
    return value

def cmnd_websensor(value, idx):
    """
    Tasmota WebSensor cmnd helper
    """
    cmd = []
    for i in range(0, 32):
        cmd.append("WebSensor{} {}".format(i+(idx-1)*32, "1" if (int(value, 16) & (1<<i)) != 0 else "0"))
    return cmd

# ----------------------------------------------------------------------
# Tasmota configuration data definition
# ----------------------------------------------------------------------

# Tasmota setings platforms
PLATFORMS = ["ESP82xx", "ESP32"]

class Platform:
    """
    Platform bitmask
    """
    ESP82 = 0x1
    ESP32 = 0x2
    ALL = 0xf

# pylint: disable=bad-continuation,bad-whitespace
SETTING_5_10_0 = {
                              # <platform>, <format>, <addrdef>, <datadef> [,<converter>]
    'cfg_holder':                   (Platform.ALL,   '<L',  0x000,       (None, None,                           (INTERNAL,      None)), '"0x{:08x}".format($)' ),
    'save_flag':                    (Platform.ALL,   '<L',  0x004,       (None, None,                           (INTERNAL,      None)), (None,      False) ),
    'version':                      (Platform.ALL,   '<L',  0x008,       (None, None,                           ('System',      None)), ('hex($)',  False) ),
    'bootcount':                    (Platform.ALL,   '<L',  0x00C,       (None, None,                           ('System',      None)), (None,      False) ),
    'flag':                         (Platform.ALL, {
        'save_state':               (Platform.ALL,   '<L', (0x010,1, 0), (None, None,                           ('SetOption',   '"SetOption0 {}".format($)')) ),
        'button_restrict':          (Platform.ALL,   '<L', (0x010,1, 1), (None, None,                           ('SetOption',   '"SetOption1 {}".format($)')) ),
        'value_units':              (Platform.ALL,   '<L', (0x010,1, 2), (None, None,                           ('SetOption',   '"SetOption2 {}".format($)')) ),
        'mqtt_enabled':             (Platform.ALL,   '<L', (0x010,1, 3), (None, None,                           ('SetOption',   '"SetOption3 {}".format($)')) ),
        'mqtt_response':            (Platform.ALL,   '<L', (0x010,1, 4), (None, None,                           ('SetOption',   '"SetOption4 {}".format($)')) ),
        'mqtt_power_retain':        (Platform.ALL,   '<L', (0x010,1, 5), (None, None,                           ('MQTT',        '"PowerRetain {}".format($)')) ),
        'mqtt_button_retain':       (Platform.ALL,   '<L', (0x010,1, 6), (None, None,                           ('MQTT',        '"ButtonRetain {}".format($)')) ),
        'mqtt_switch_retain':       (Platform.ALL,   '<L', (0x010,1, 7), (None, None,                           ('MQTT',        '"SwitchRetain {}".format($)')) ),
        'temperature_conversion':   (Platform.ALL,   '<L', (0x010,1, 8), (None, None,                           ('SetOption',   '"SetOption8 {}".format($)')) ),
        'mqtt_sensor_retain':       (Platform.ALL,   '<L', (0x010,1, 9), (None, None,                           ('MQTT',        '"SensorRetain {}".format($)')) ),
        'mqtt_offline':             (Platform.ALL,   '<L', (0x010,1,10), (None, None,                           ('SetOption',   '"SetOption10 {}".format($)')) ),
        'button_swap':              (Platform.ALL,   '<L', (0x010,1,11), (None, None,                           ('SetOption',   '"SetOption11 {}".format($)')) ),
        'stop_flash_rotate':        (Platform.ALL,   '<L', (0x010,1,12), (None, None,                           ('Management',  '"SetOption12 {}".format($)')) ),
        'button_single':            (Platform.ALL,   '<L', (0x010,1,13), (None, None,                           ('SetOption',   '"SetOption13 {}".format($)')) ),
        'interlock':                (Platform.ALL,   '<L', (0x010,1,14), (None, None,                           ('SetOption',   '"SetOption14 {}".format($)')) ),
        'pwm_control':              (Platform.ALL,   '<L', (0x010,1,15), (None, None,                           ('SetOption',   '"SetOption15 {}".format($)')) ),
        'ws_clock_reverse':         (Platform.ALL,   '<L', (0x010,1,16), (None, None,                           ('SetOption',   '"SetOption16 {}".format($)')) ),
        'decimal_text':             (Platform.ALL,   '<L', (0x010,1,17), (None, None,                           ('SetOption',   '"SetOption17 {}".format($)')) ),
                                    },                      0x010,       (None, None,                           (VIRTUAL,       None)), (None,      None) ),
    'save_data':                    (Platform.ALL,   '<h',  0x014,       (None, '0 <= $ <= 3600',               ('Management',  '"SaveData {}".format($)')) ),
    'timezone':                     (Platform.ALL,   'b',   0x016,       (None, '-13 <= $ <= 13 or $==99',      ('Management',  '"Timezone {}".format($)')) ),
    'ota_url':                      (Platform.ALL,   '101s',0x017,       (None, None,                           ('Management',  '"OtaUrl {}".format($)')) ),
    'mqtt_prefix':                  (Platform.ALL,   '11s', 0x07C,       ([3],  None,                           ('MQTT',        '"Prefix{} {}".format(#,$)')) ),
    'seriallog_level':              (Platform.ALL,   'B',   0x09E,       (None, '0 <= $ <= 5',                  ('Management',  '"SerialLog {}".format($)')) ),
    'sta_config':                   (Platform.ALL,   'B',   0x09F,       (None, '0 <= $ <= 5',                  ('Wifi',        '"WifiConfig {}".format($)')) ),
    'sta_active':                   (Platform.ALL,   'B',   0x0A0,       (None, '0 <= $ <= 1',                  ('Wifi',        '"AP {}".format($)')) ),
    'sta_ssid':                     (Platform.ALL,   '33s', 0x0A1,       ([2],  None,                           ('Wifi',        '"SSId{} {}".format(#,$)')) ),
    'sta_pwd':                      (Platform.ALL,   '65s', 0x0E3,       ([2],  None,                           ('Wifi',        '"Password{} {}".format(#,$)')), (passwordread,passwordwrite) ),
    'hostname':                     (Platform.ALL,   '33s', 0x165,       (None, None,                           ('Wifi',        '"Hostname {}".format($)')) ),
    'syslog_host':                  (Platform.ALL,   '33s', 0x186,       (None, None,                           ('Management',  '"LogHost {}".format($)')) ),
    'syslog_port':                  (Platform.ALL,   '<H',  0x1A8,       (None, '1 <= $ <= 32766',              ('Management',  '"LogPort {}".format($)')) ),
    'syslog_level':                 (Platform.ALL,   'B',   0x1AA,       (None, '0 <= $ <= 4',                  ('Management',  '"SysLog {}".format($)')) ),
    'webserver':                    (Platform.ALL,   'B',   0x1AB,       (None, '0 <= $ <= 2',                  ('Wifi',        '"WebServer {}".format($)')) ),
    'weblog_level':                 (Platform.ALL,   'B',   0x1AC,       (None, '0 <= $ <= 4',                  ('Management',  '"WebLog {}".format($)')) ),
    'mqtt_fingerprint':             (Platform.ALL,   'B',   0x1AD,       ([60], None,                           ('MQTT',        '"MqttFingerprint {}".format(" ".join("{:02X}".format((int(c,0))) for c in @["mqtt_fingerprint"])) if 1==# else None')), '"0x{:02x}".format($)' ),
    'mqtt_host':                    (Platform.ALL,   '33s', 0x1E9,       (None, None,                           ('MQTT',        '"MqttHost {}".format($)')) ),
    'mqtt_port':                    (Platform.ALL,   '<H',  0x20A,       (None, None,                           ('MQTT',        '"MqttPort {}".format($)')) ),
    'mqtt_client':                  (Platform.ALL,   '33s', 0x20C,       (None, None,                           ('MQTT',        '"MqttClient {}".format($)')) ),
    'mqtt_user':                    (Platform.ALL,   '33s', 0x22D,       (None, None,                           ('MQTT',        '"MqttUser {}".format($)')) ),
    'mqtt_pwd':                     (Platform.ALL,   '33s', 0x24E,       (None, None,                           ('MQTT',        '"MqttPassword {}".format($)')), (passwordread,passwordwrite) ),
    'mqtt_topic':                   (Platform.ALL,   '33s', 0x26F,       (None, None,                           ('MQTT',        '"FullTopic {}".format($)')) ),
    'button_topic':                 (Platform.ALL,   '33s', 0x290,       (None, None,                           ('MQTT',        '"ButtonTopic {}".format($)')) ),
    'mqtt_grptopic':                (Platform.ALL,   '33s', 0x2B1,       (None, None,                           ('MQTT',        '"GroupTopic {}".format($)')) ),
    'mqtt_fingerprinth':            (Platform.ALL,   'B',   0x2D2,       ([20], None,                           ('MQTT',        None)) ),
    'pwm_frequency':                (Platform.ALL,   '<H',  0x2E6,       (None, '$==1 or 100 <= $ <= 4000',     ('Management',  '"PwmFrequency {}".format($)')) ),
    'power':                        (Platform.ALL, {
        'power1':                   (Platform.ALL,   '<L', (0x2E8,1,0),  (None, None,                           ('Control',     '"Power1 {}".format($)')) ),
        'power2':                   (Platform.ALL,   '<L', (0x2E8,1,1),  (None, None,                           ('Control',     '"Power2 {}".format($)')) ),
        'power3':                   (Platform.ALL,   '<L', (0x2E8,1,2),  (None, None,                           ('Control',     '"Power3 {}".format($)')) ),
        'power4':                   (Platform.ALL,   '<L', (0x2E8,1,3),  (None, None,                           ('Control',     '"Power4 {}".format($)')) ),
        'power5':                   (Platform.ALL,   '<L', (0x2E8,1,4),  (None, None,                           ('Control',     '"Power5 {}".format($)')) ),
        'power6':                   (Platform.ALL,   '<L', (0x2E8,1,5),  (None, None,                           ('Control',     '"Power6 {}".format($)')) ),
        'power7':                   (Platform.ALL,   '<L', (0x2E8,1,6),  (None, None,                           ('Control',     '"Power7 {}".format($)')) ),
        'power8':                   (Platform.ALL,   '<L', (0x2E8,1,7),  (None, None,                           ('Control',     '"Power8 {}".format($)')) ),
                                    },                      0x2E8,       (None, None,                           ('Control',     None)), (None,      None) ),
    'pwm_value':                    (Platform.ALL,   '<H',  0x2EC,       ([5],  '0 <= $ <= 1023',               ('Management',  '"Pwm{} {}".format(#,$)')) ),
    'altitude':                     (Platform.ALL,   '<h',  0x2F6,       (None, '-30000 <= $ <= 30000',         ('Sensor',      '"Altitude {}".format($)')) ),
    'tele_period':                  (Platform.ALL,   '<H',  0x2F8,       (None, '0 <= $ <= 1 or 10 <= $ <= 3600',('MQTT',       '"TelePeriod {}".format($)')) ),
    'ledstate':                     (Platform.ALL,   'B',   0x2FB,       (None, '0 <= ($ & 0x7) <= 7',          ('Control',     '"LedState {}".format(($ & 0x7))')) ),
    'param':                        (Platform.ALL,   'B',   0x2FC,       ([23], None,                           ('SetOption',   '"SetOption{} {}".format(#+31,$)')) ),
    'state_text':                   (Platform.ALL,   '11s', 0x313,       ([4],  None,                           ('MQTT',        '"StateText{} {}".format(#,$)')) ),
    'domoticz_update_timer':        (Platform.ALL,   '<H',  0x340,       (None, '0 <= $ <= 3600',               ('Domoticz',    '"DomoticzUpdateTimer {}".format($)')) ),
    'pwm_range':                    (Platform.ALL,   '<H',  0x342,       (None, '$==1 or 255 <= $ <= 1023',     ('Management',  '"PwmRange {}".format($)')) ),
    'domoticz_relay_idx':           (Platform.ALL,   '<L',  0x344,       ([4],  None,                           ('Domoticz',    '"DomoticzIdx{} {}".format(#,$)')) ),
    'domoticz_key_idx':             (Platform.ALL,   '<L',  0x354,       ([4],  None,                           ('Domoticz',    '"DomoticzKeyIdx{} {}".format(#,$)')) ),
    'energy_power_calibration':     (Platform.ALL,   '<L',  0x364,       (None, None,                           ('Power',       '"PowerSet {}".format($)')) ),
    'energy_voltage_calibration':   (Platform.ALL,   '<L',  0x368,       (None, None,                           ('Power',       '"VoltageSet {}".format($)')) ),
    'energy_current_calibration':   (Platform.ALL,   '<L',  0x36C,       (None, None,                           ('Power',       '"CurrentSet {}".format($)')) ),
    'energy_kWhtoday':              (Platform.ALL,   '<L',  0x370,       (None, '0 <= $ <= 4250000',            ('Power',       '"EnergyReset1 {}".format(int(round(float($)//100)))')) ),
    'energy_kWhyesterday':          (Platform.ALL,   '<L',  0x374,       (None, '0 <= $ <= 4250000',            ('Power',       '"EnergyReset2 {}".format(int(round(float($)//100)))')) ),
    'energy_kWhdoy':                (Platform.ALL,   '<H',  0x378,       (None, None,                           ('Power',       None)) ),
    'energy_min_power':             (Platform.ALL,   '<H',  0x37A,       (None, None,                           ('Power',       '"PowerLow {}".format($)')) ),
    'energy_max_power':             (Platform.ALL,   '<H',  0x37C,       (None, None,                           ('Power',       '"PowerHigh {}".format($)')) ),
    'energy_min_voltage':           (Platform.ALL,   '<H',  0x37E,       (None, None,                           ('Power',       '"VoltageLow {}".format($)')) ),
    'energy_max_voltage':           (Platform.ALL,   '<H',  0x380,       (None, None,                           ('Power',       '"VoltageHigh {}".format($)')) ),
    'energy_min_current':           (Platform.ALL,   '<H',  0x382,       (None, None,                           ('Power',       '"CurrentLow {}".format($)')) ),
    'energy_max_current':           (Platform.ALL,   '<H',  0x384,       (None, None,                           ('Power',       '"CurrentHigh {}".format($)')) ),
    'energy_max_power_limit':       (Platform.ALL,   '<H',  0x386,       (None, None,                           ('Power',       '"MaxPower {}".format($)')) ),
    'energy_max_power_limit_hold':  (Platform.ALL,   '<H',  0x388,       (None, None,                           ('Power',       '"MaxPowerHold {}".format($)')) ),
    'energy_max_power_limit_window':(Platform.ALL,   '<H',  0x38A,       (None, None,                           ('Power',       '"MaxPowerWindow {}".format($)')) ),
    'energy_max_power_safe_limit':  (Platform.ALL,   '<H',  0x38C,       (None, None,                           ('Power',       '"SavePower {}".format($)')) ),
    'energy_max_power_safe_limit_hold':
                                    (Platform.ALL,   '<H',  0x38E,       (None, None,                           ('Power',       '"SavePowerHold {}".format($)')) ),
    'energy_max_power_safe_limit_window':
                                    (Platform.ALL,   '<H',  0x390,       (None, None,                           ('Power',       '"SavePowerWindow {}".format($)')) ),
    'energy_max_energy':            (Platform.ALL,   '<H',  0x392,       (None, None,                           ('Power',       '"MaxEnergy {}".format($)')) ),
    'energy_max_energy_start':      (Platform.ALL,   '<H',  0x394,       (None, None,                           ('Power',       '"MaxEnergyStart {}".format($)')) ),
    'mqtt_retry':                   (Platform.ALL,   '<H',  0x396,       (None, '10 <= $ <= 32000',             ('MQTT',        '"MqttRetry {}".format($)')) ),
    'poweronstate':                 (Platform.ALL,   'B',   0x398,       (None, '0 <= $ <= 5',                  ('Control',     '"PowerOnState {}".format($)')) ),
    'last_module':                  (Platform.ALL,   'B',   0x399,       (None, None,                           (INTERNAL,      None)) ),
    'blinktime':                    (Platform.ALL,   '<H',  0x39A,       (None, '2 <= $ <= 3600',               ('Control',     '"BlinkTime {}".format($)')) ),
    'blinkcount':                   (Platform.ALL,   '<H',  0x39C,       (None, '0 <= $ <= 32000',              ('Control',     '"BlinkCount {}".format($)')) ),
    'friendlyname':                 (Platform.ALL,   '33s', 0x3AC,       ([4],  None,                           ('Management',  '"FriendlyName{} {}".format(#,"\\"" if len($) == 0 else $)')) ),
    'switch_topic':                 (Platform.ALL,   '33s', 0x430,       (None, None,                           ('MQTT',        '"SwitchTopic {}".format($)')) ),
    'sleep':                        (Platform.ALL,   'B',   0x453,       (None, '0 <= $ <= 250',                ('Management',  '"Sleep {}".format($)')) ),
    'domoticz_switch_idx':          (Platform.ALL,   '<H',  0x454,       ([4],  None,                           ('Domoticz',    '"DomoticzSwitchIdx{} {}".format(#,$)')) ),
    'domoticz_sensor_idx':          (Platform.ALL,   '<H',  0x45C,       ([12], None,                           ('Domoticz',    '"DomoticzSensorIdx{} {}".format(#,$)')) ),
    'module':                       (Platform.ALL,   'B',   0x474,       (None, None,                           ('Management',  '"Module {}".format($)')) ),
    'ws_color':                     (Platform.ALL,   'B',   0x475,       ([4,3],None,                           ('Light',       None)) ),
    'ws_width':                     (Platform.ALL,   'B',   0x481,       ([3],  None,                           ('Light',       None)) ),
    'my_gp':                        (Platform.ALL,   'B',   0x484,       ([18], None,                           ('Management',  '"Gpio{} {}".format(#-1,$)')) ),
    'light_pixels':                 (Platform.ALL,   '<H',  0x496,       (None, '1 <= $ <= 512',                ('Light',       '"Pxels {}".format($)')) ),
    'light_color':                  (Platform.ALL,   'B',   0x498,       ([5],  None,                           ('Light',       None)) ),
    'light_correction':             (Platform.ALL,   'B',   0x49D     ,  (None, '0 <= $ <= 1',                  ('Light',       '"LedTable {}".format($)')) ),
    'light_dimmer':                 (Platform.ALL,   'B',   0x49E,       (None, '0 <= $ <= 100',                ('Light',       '"Wakeup {}".format($)')) ),
    'light_fade':                   (Platform.ALL,   'B',   0x4A1,       (None, '0 <= $ <= 1',                  ('Light',       '"Fade {}".format($)')) ),
    'light_speed':                  (Platform.ALL,   'B',   0x4A2,       (None, '1 <= $ <= 20',                 ('Light',       '"Speed {}".format($)')) ),
    'light_scheme':                 (Platform.ALL,   'B',   0x4A3,       (None, None,                           ('Light',       '"Scheme {}".format($)')) ),
    'light_width':                  (Platform.ALL,   'B',   0x4A4,       (None, '0 <= $ <= 4',                  ('Light',       '"Width {}".format($)')) ),
    'light_wakeup':                 (Platform.ALL,   '<H',  0x4A6,       (None, '0 <= $ <= 3100',               ('Light',       '"WakeUpDuration {}".format($)')) ),
    'web_password':                 (Platform.ALL,   '33s', 0x4A9,       (None, None,                           ('Wifi',        '"WebPassword {}".format($)')), (passwordread,passwordwrite) ),
    'switchmode':                   (Platform.ALL,   'B',   0x4CA,       ([4],  '0 <= $ <= 7',                  ('Control',     '"SwitchMode{} {}".format(#,$)')) ),
    'ntp_server':                   (Platform.ALL,   '33s', 0x4CE,       ([3],  None,                           ('Wifi',        '"NtpServer{} {}".format(#,$)')) ),
    'ina219_mode':                  (Platform.ALL,   'B',   0x531,       (None, '0 <= $ <= 7',                  ('Sensor',      '"Sensor13 {}".format($)')) ),
    'pulse_timer':                  (Platform.ALL,   '<H',  0x532,       ([8],  '0 <= $ <= 64900',              ('Control',     '"PulseTime{} {}".format(#,$)')) ),
    'ip_address':                   (Platform.ALL,   '<L',  0x544,       ([4],  None,                           ('Wifi',        '"IPAddress{} {}".format(#,$)')), ("socket.inet_ntoa(struct.pack('<L', $))", "struct.unpack('<L', socket.inet_aton($))[0]")),
    'energy_kWhtotal':              (Platform.ALL,   '<L',  0x554,       (None, '0 <= $ <= 4250000000',         ('Power',       '"EnergyReset3 {}".format(int(round(float($)//100)))')) ),
    'mqtt_fulltopic':               (Platform.ALL,   '100s',0x558,       (None, None,                           ('MQTT',        '"FullTopic {}".format($)')) ),
    'flag2':                        (Platform.ALL, {
        'current_resolution':       (Platform.ALL,   '<L', (0x5BC,2,15), (None, '0 <= $ <= 3',                  ('Sensor',      '"AmpRes {}".format($)')) ),
        'voltage_resolution':       (Platform.ALL,   '<L', (0x5BC,2,17), (None, '0 <= $ <= 3',                  ('Sensor',      '"VoltRes {}".format($)')) ),
        'wattage_resolution':       (Platform.ALL,   '<L', (0x5BC,2,19), (None, '0 <= $ <= 3',                  ('Sensor',      '"WattRes {}".format($)')) ),
        'emulation':                (Platform.ALL,   '<L', (0x5BC,2,21), (None, '0 <= $ <= 2',                  ('Management',  '"Emulation {}".format($)')) ),
        'energy_resolution':        (Platform.ALL,   '<L', (0x5BC,3,23), (None, '0 <= $ <= 5',                  ('Sensor',      '"EnergyRes {}".format($)')) ),
        'pressure_resolution':      (Platform.ALL,   '<L', (0x5BC,2,26), (None, '0 <= $ <= 3',                  ('Sensor',      '"PressRes {}".format($)')) ),
        'humidity_resolution':      (Platform.ALL,   '<L', (0x5BC,2,28), (None, '0 <= $ <= 3',                  ('Sensor',      '"HumRes {}".format($)')) ),
        'temperature_resolution':   (Platform.ALL,   '<L', (0x5BC,2,30), (None, '0 <= $ <= 3',                  ('Sensor',      '"TempRes {}".format($)')) ),
                                    },                      0x5BC,       (None, None,                           (VIRTUAL,       None)), (None,      None) ),
    'pulse_counter':                (Platform.ALL,   '<L',  0x5C0,       ([4],  None,                           ('Sensor',      '"Counter{} {}".format(#,$)')) ),
    'pulse_counter_type':           (Platform.ALL, {
        'pulse_counter_type1':      (Platform.ALL,   '<H', (0x5D0,1,0),  (None, None,                           ('Sensor',      '"CounterType1 {}".format($)')) ),
        'pulse_counter_type2':      (Platform.ALL,   '<H', (0x5D0,1,1),  (None, None,                           ('Sensor',      '"CounterType2 {}".format($)')) ),
        'pulse_counter_type3':      (Platform.ALL,   '<H', (0x5D0,1,2),  (None, None,                           ('Sensor',      '"CounterType3 {}".format($)')) ),
        'pulse_counter_type4':      (Platform.ALL,   '<H', (0x5D0,1,3),  (None, None,                           ('Sensor',      '"CounterType4 {}".format($)')) ),
                                    },                      0x5D0,       (None, None,                           ('Sensor',      None)), (None,      None) ),
    'pulse_counter_debounce':       (Platform.ALL,   '<H',  0x5D2,       (None, '0 <= $ <= 32000',              ('Sensor',      '"CounterDebounce {}".format($)')) ),
    'rf_code':                      (Platform.ALL,   'B',   0x5D4,       ([17,9],None,                          ('Rf',          None)), '"0x{:02x}".format($)'),
}
# ======================================================================
SETTING_5_11_0 = copy.deepcopy(SETTING_5_10_0)
SETTING_5_11_0.update               ({
    'display_model':                (Platform.ALL,   'B',   0x2D2,       (None, '0 <= $ <= 16',                 ('Display',     '"Model {}".format($)')) ),
    'display_mode':                 (Platform.ALL,   'B',   0x2D3,       (None, '0 <= $ <= 5',                  ('Display',     '"Mode {}".format($)')) ),
    'display_refresh':              (Platform.ALL,   'B',   0x2D4,       (None, '1 <= $ <= 7',                  ('Display',     '"Refresh {}".format($)')) ),
    'display_rows':                 (Platform.ALL,   'B',   0x2D5,       (None, '1 <= $ <= 32',                 ('Display',     '"Rows {}".format($)')) ),
    'display_cols':                 (Platform.ALL,   'B',   0x2D6,       ([2],  '1 <= $ <= 40',                 ('Display',     '"Cols{} {}".format(#,$)')) ),
    'display_address':              (Platform.ALL,   'B',   0x2D8,       ([8],  None,                           ('Display',     '"Address{} {}".format(#,$)')) ),
    'display_dimmer':               (Platform.ALL,   'B',   0x2E0,       (None, '0 <= $ <= 100',                ('Display',     '"Dimmer {}".format($)')) ),
    'display_size':                 (Platform.ALL,   'B',   0x2E1,       (None, '1 <= $ <= 4',                  ('Display',     '"Size {}".format($)')) ),
                                    })
SETTING_5_11_0['flag'][1].update    ({
        'light_signal':             (Platform.ALL,   '<L', (0x010,1,18), (None, None,                           ('SetOption',   '"SetOption18 {}".format($)')) ),
                                    })
SETTING_5_11_0.pop('mqtt_fingerprinth',None)
# ======================================================================
SETTING_5_12_0 = copy.deepcopy(SETTING_5_11_0)
SETTING_5_12_0['flag'][1].update    ({
        'hass_discovery':           (Platform.ALL,   '<L', (0x010,1,19), (None, None,                           ('SetOption',   '"SetOption19 {}".format($)')) ),
        'not_power_linked':         (Platform.ALL,   '<L', (0x010,1,20), (None, None,                           ('SetOption',   '"SetOption20 {}".format($)')) ),
        'no_power_on_check':        (Platform.ALL,   '<L', (0x010,1,21), (None, None,                           ('SetOption',   '"SetOption21 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_5_13_1 = copy.deepcopy(SETTING_5_12_0)
SETTING_5_13_1.pop('mqtt_fingerprint',None)
SETTING_5_13_1['flag'][1].update    ({
        'mqtt_serial':              (Platform.ALL,   '<L', (0x010,1,22), (None, None,                           ('SetOption',   '"SetOption22 {}".format($)')) ),
        'rules_enabled':            (Platform.ALL,   '<L', (0x010,1,23), (None, None,                           ('SetOption',   '"SetOption23 {}".format($)')) ),
        'rules_once':               (Platform.ALL,   '<L', (0x010,1,24), (None, None,                           ('SetOption',   '"SetOption24 {}".format($)')) ),
        'knx_enabled':              (Platform.ALL,   '<L', (0x010,1,25), (None, None,                           ('KNX',         '"KNX_ENABLED {}".format($)')) ),
                                    })
SETTING_5_13_1.update               ({
    'baudrate':                     (Platform.ALL,   'B',   0x09D,       (None, None,                           ('Serial',      '"Baudrate {}".format($)')), ('$ * 1200','$ // 1200') ),
    'mqtt_fingerprint1':            (Platform.ALL,   'B',   0x1AD,       ([20], None,                           ('MQTT',        '"MqttFingerprint1 {}".format(" ".join("{:02X}".format((int(c,0))) for c in @["mqtt_fingerprint1"])) if 1==# else None')), '"0x{:02x}".format($)' ),
    'mqtt_fingerprint2':            (Platform.ALL,   'B',   0x1AD+20,    ([20], None,                           ('MQTT',        '"MqttFingerprint2 {}".format(" ".join("{:02X}".format((int(c,0))) for c in @["mqtt_fingerprint2"])) if 1==# else None')), '"0x{:02x}".format($)' ),
    'energy_power_delta':           (Platform.ALL,   'B',   0x33F,       (None, None,                           ('Power',       '"PowerDelta {}".format($)')) ),
    'light_rotation':               (Platform.ALL,   '<H',  0x39E,       (None, None,                           ('Light',       '"Rotation {}".format($)')) ),
    'serial_delimiter':             (Platform.ALL,   'B',   0x451,       (None, None,                           ('Serial',      '"SerialDelimiter {}".format($)')) ),
    'sbaudrate':                    (Platform.ALL,   'B',   0x452,       (None, None,                           ('Serial',      '"SBaudrate {}".format($)')), ('$ * 1200','$ // 1200') ),
    'knx_GA_registered':            (Platform.ALL,   'B',   0x4A5,       (None, None,                           ('KNX',         None)) ),
    'knx_CB_registered':            (Platform.ALL,   'B',   0x4A8,       (None, None,                           ('KNX',         None)) ),
    'timer':                        (Platform.ALL, {
        'time':                     (Platform.ALL,   '<L', (0x670,11, 0),(None, '0 <= $ < 1440',                ('Timer',       '"Timer{} {{\\\"Arm\\\":{arm},\\\"Mode\\\":{mode},\\\"Time\\\":\\\"{tsign}{time}\\\",\\\"Window\\\":{window},\\\"Days\\\":\\\"{days}\\\",\\\"Repeat\\\":{repeat},\\\"Output\\\":{device},\\\"Action\\\":{power}}}".format(#, arm=bitsread($,31),mode=bitsread($,29,2),tsign="-" if bitsread($,29,2)>0 and bitsread($,0,11)>(12*60) else "",time=time.strftime("%H:%M",time.gmtime((bitsread($,0,11) if bitsread($,29,2)==0 else bitsread($,0,11) if bitsread($,0,11)<=(12*60) else bitsread($,0,11)-(12*60))*60)),window=bitsread($,11,4),repeat=bitsread($,15),days="{:07b}".format(bitsread($,16,7))[::-1],device=bitsread($,23,4)+1,power=bitsread($,27,2) )')), ('"0x{:08x}".format($)', False) ),
        'window':                   (Platform.ALL,   '<L', (0x670, 4,11),(None, None,                           ('Timer',       None)) ),
        'repeat':                   (Platform.ALL,   '<L', (0x670, 1,15),(None, None,                           ('Timer',       None)) ),
        'days':                     (Platform.ALL,   '<L', (0x670, 7,16),(None, None,                           ('Timer',       None)), '"0b{:07b}".format($)' ),
        'device':                   (Platform.ALL,   '<L', (0x670, 4,23),(None, None,                           ('Timer',       None)) ),
        'power':                    (Platform.ALL,   '<L', (0x670, 2,27),(None, None,                           ('Timer',       None)) ),
        'mode':                     (Platform.ALL,   '<L', (0x670, 2,29),(None, '0 <= $ <= 3',                  ('Timer',       None)) ),
        'arm':                      (Platform.ALL,   '<L', (0x670, 1,31),(None, None,                           ('Timer',       None)) ),
                                    },                      0x670,       ([16], None,                           ('Timer',       None)) ),
    'latitude':                     (Platform.ALL,   'i',   0x6B0,       (None, None,                           ('Timer',       '"Latitude {}".format($)')),  ('float($) / 1000000', 'int($ * 1000000)')),
    'longitude':                    (Platform.ALL,   'i',   0x6B4,       (None, None,                           ('Timer',       '"Longitude {}".format($)')), ('float($) / 1000000', 'int($ * 1000000)')),
    'knx_physsical_addr':           (Platform.ALL,   '<H',  0x6B8,       (None, None,                           ('KNX',         None)) ),
    'knx_GA_addr':                  (Platform.ALL,   '<H',  0x6BA,       ([10], None,                           ('KNX',         None)) ),
    'knx_CB_addr':                  (Platform.ALL,   '<H',  0x6CE,       ([10], None,                           ('KNX',         None)) ),
    'knx_GA_param':                 (Platform.ALL,   'B',   0x6E2,       ([10], None,                           ('KNX',         None)) ),
    'knx_CB_param':                 (Platform.ALL,   'B',   0x6EC,       ([10], None,                           ('KNX',         None)) ),
    'rules':                        (Platform.ALL,   '512s',0x800,       (None, None,                           ('Rules',       '"Rule {}".format("\\"" if len($) == 0 else $)')) ),
                                    })
# ======================================================================
SETTING_5_14_0 = copy.deepcopy(SETTING_5_13_1)
SETTING_5_14_0['flag'][1].update    ({
        'device_index_enable':      (Platform.ALL,   '<L', (0x010,1,26), (None, None,                           ('SetOption',   '"SetOption26 {}".format($)')) ),
                                    })
SETTING_5_14_0['flag'][1].pop('rules_once',None)
SETTING_5_14_0.update               ({
    'tflag':                        (Platform.ALL, {
        'hemis':                    (Platform.ALL,   '<H', (0x2E2,1, 0), (None, None,                           ('Management',  None)) ),
        'week':                     (Platform.ALL,   '<H', (0x2E2,3, 1), (None, '0 <= $ <= 4',                  ('Management',  None)) ),
        'month':                    (Platform.ALL,   '<H', (0x2E2,4, 4), (None, '1 <= $ <= 12',                 ('Management',  None)) ),
        'dow':                      (Platform.ALL,   '<H', (0x2E2,3, 8), (None, '1 <= $ <= 7',                  ('Management',  None)) ),
        'hour':                     (Platform.ALL,   '<H', (0x2E2,5,11), (None, '0 <= $ <= 23',                 ('Management',  None)) ),
                                    },                      0x2E2,       ([2],  None,                           ('Management',  None)), (None,      None) ),
    'param':                        (Platform.ALL,   'B',   0x2FC,       ([18], None,                           ('SetOption',   '"SetOption{} {}".format(#+31,$)')) ),
    'toffset':                      (Platform.ALL,   '<h',  0x30E,       ([2],  None,                           ('Management',  '"{cmnd} {hemis},{week},{month},{dow},{hour},{toffset}".format(cmnd="TimeSTD" if idx==1 else "TimeDST", hemis=@["tflag"][#-1]["hemis"], week=@["tflag"][#-1]["week"], month=@["tflag"][#-1]["month"], dow=@["tflag"][#-1]["dow"], hour=@["tflag"][#-1]["hour"], toffset=value)')) ),
                                    })
# ======================================================================
SETTING_6_0_0 = copy.deepcopy(SETTING_5_14_0)
SETTING_6_0_0.update({
    'cfg_holder':                   (Platform.ALL,   '<H',  0x000,       (None, None,                           ('System',      None)), ),
    'cfg_size':                     (Platform.ALL,   '<H',  0x002,       (None, None,                           ('System',      None)), (None, False)),
    'bootcount':                    (Platform.ALL,   '<H',  0x00C,       (None, None,                           ('System',      None)), (None, False)),
    'cfg_crc':                      (Platform.ALL,   '<H',  0x00E,       (None, None,                           ('System',      None)), '"0x{:04x}".format($)'),
    'rule_enabled':                 (Platform.ALL, {
        'rule1':                    (Platform.ALL,   'B',  (0x49F,1,0),  (None, None,                           ('Rules',       '"Rule1 {}".format($)')) ),
        'rule2':                    (Platform.ALL,   'B',  (0x49F,1,1),  (None, None,                           ('Rules',       '"Rule2 {}".format($)')) ),
        'rule3':                    (Platform.ALL,   'B',  (0x49F,1,2),  (None, None,                           ('Rules',       '"Rule3 {}".format($)')) ),
                                    },                      0x49F,       (None, None,                           ('Rules',       None)), (None,      None) ),
    'rule_once':                    (Platform.ALL, {
        'rule1':                    (Platform.ALL,   'B',  (0x4A0,1,0),  (None, None,                           ('Rules',       '"Rule1 {}".format($+4)')) ),
        'rule2':                    (Platform.ALL,   'B',  (0x4A0,1,1),  (None, None,                           ('Rules',       '"Rule2 {}".format($+4)')) ),
        'rule3':                    (Platform.ALL,   'B',  (0x4A0,1,2),  (None, None,                           ('Rules',       '"Rule3 {}".format($+4)')) ),
                                    },                      0x4A0,       (None, None,                           ('Rules',       None)), (None,      None) ),
    'mems':                         (Platform.ALL,   '10s', 0x7CE,       ([5],  None,                           ('Rules',       '"Mem{} {}".format(#,"\\"" if len($) == 0 else $)')) ),
    'rules':                        (Platform.ALL,   '512s',0x800,       ([3],  None,                           ('Rules',       '"Rule{} {}".format(#,"\\"" if len($) == 0 else $)')) ),
})
SETTING_6_0_0['flag'][1].update     ({
        'knx_enable_enhancement':   (Platform.ALL,   '<L', (0x010,1,27), (None, None,                           ('KNX',         '"KNX_ENHANCED {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_1_1 = copy.deepcopy(SETTING_6_0_0)
SETTING_6_1_1.update                ({
    'flag3':                        (Platform.ALL,   '<L',  0x3A0,       (None, None,                           (INTERNAL,      None)), '"0x{:08x}".format($)' ),
    'switchmode':                   (Platform.ALL,   'B',   0x3A4,       ([8],  '0 <= $ <= 7',                  ('Control',     '"SwitchMode{} {}".format(#,$)')) ),
    'mcp230xx_config':              (Platform.ALL, {
        'pinmode':                  (Platform.ALL,   '<L', (0x6F6,3, 0), (None, None,                           ('Sensor',      '"Sensor29 {pin},{pinmode},{pullup},{intmode}".format(pin=#-1, pinmode=@["mcp230xx_config"][#-1]["pinmode"], pullup=@["mcp230xx_config"][#-1]["pullup"], intmode=@["mcp230xx_config"][#-1]["int_report_mode"])')), '"0x{:08x}".format($)' ),
        'pullup':                   (Platform.ALL,   '<L', (0x6F6,1, 3), (None, None,                           ('Sensor',      None)) ),
        'saved_state':              (Platform.ALL,   '<L', (0x6F6,1, 4), (None, None,                           ('Sensor',      None)) ),
        'int_report_mode':          (Platform.ALL,   '<L', (0x6F6,2, 5), (None, None,                           ('Sensor',      None)) ),
        'int_report_defer':         (Platform.ALL,   '<L', (0x6F6,4, 7), (None, None,                           ('Sensor',      None)) ),
        'int_count_en':             (Platform.ALL,   '<L', (0x6F6,1,11), (None, None,                           ('Sensor',      None)) ),
                                     },     0x6F6,       ([16], None,                                           ('Sensor',      None)), (None,      None) ),
                                    })
SETTING_6_1_1['flag'][1].update     ({
        'rf_receive_decimal':       (Platform.ALL,   '<L', (0x010,1,28), (None, None,                           ('SetOption' ,  '"SetOption28 {}".format($)')) ),
        'ir_receive_decimal':       (Platform.ALL,   '<L', (0x010,1,29), (None, None,                           ('SetOption',   '"SetOption29 {}".format($)')) ),
        'hass_light':               (Platform.ALL,   '<L', (0x010,1,30), (None, None,                           ('SetOption',   '"SetOption30 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_2_1 = copy.deepcopy(SETTING_6_1_1)
SETTING_6_2_1.update                ({
    'rule_stop':                    (Platform.ALL, {
        'rule1':                    (Platform.ALL,   'B',  (0x1A7,1,0),  (None, None,                           ('Rules',       '"Rule1 {}".format($+8)')) ),
        'rule2':                    (Platform.ALL,   'B',  (0x1A7,1,1),  (None, None,                           ('Rules',       '"Rule2 {}".format($+8)')) ),
        'rule3':                    (Platform.ALL,   'B',  (0x1A7,1,2),  (None, None,                           ('Rules',       '"Rule3 {}".format($+8)')) ),
                                     },     0x1A7,        None),
    'display_rotate':               (Platform.ALL,   'B',   0x2FA,       (None, '0 <= $ <= 3',                  ('Display',     '"Rotate {}".format($)')) ),
    'display_font':                 (Platform.ALL,   'B',   0x312,       (None, '1 <= $ <= 4',                  ('Display',     '"Font {}".format($)')) ),
    'flag3':                        (Platform.ALL, {
         'timers_enable':           (Platform.ALL,   '<L', (0x3A0,1, 0), (None, None,                           ('Timer',       '"Timers {}".format($)')) ),
         'user_esp8285_enable':     (Platform.ALL,   '<L', (0x3A0,1,31), (None, None,                           (INTERNAL,      None)) ),
                                    },                      0x3A0,       (None, None,                           (VIRTUAL,       None)), (None,      None) ),
    'button_debounce':              (Platform.ALL,   '<H',  0x542,       (None, '40 <= $ <= 1000',              ('Control',     '"ButtonDebounce {}".format($)')) ),
    'switch_debounce':              (Platform.ALL,   '<H',  0x66E,       (None, '40 <= $ <= 1000',              ('Control',     '"SwitchDebounce {}".format($)')) ),
    'mcp230xx_int_prio':            (Platform.ALL,   'B',   0x716,       (None, None,                           ('Sensor',      None)) ),
    'mcp230xx_int_timer':           (Platform.ALL,   '<H',  0x718,       (None, None,                           ('Sensor',      None)) ),
                                    })
SETTING_6_2_1['flag'][1].pop('rules_enabled',None)
SETTING_6_2_1['flag'][1].update     ({
        'mqtt_serial_raw':          (Platform.ALL,   '<L', (0x010,1,23), (None, None,                           ('SetOption',   '"SetOption23 {}".format($)')) ),
        'global_state':             (Platform.ALL,   '<L', (0x010,1,31), (None, None,                           ('SetOption',   '"SetOption31 {}".format($)')) ),
                                    })
SETTING_6_2_1['flag2'][1].update    ({
    # currently unsupported Tasmota command, should be Sensor32, still needs to implement
    'axis_resolution':              (Platform.ALL,   '<L', (0x5BC,2,13), (None, None,                           (INTERNAL,      None)) ),
                                    })
# ======================================================================
SETTING_6_2_1_2 = copy.deepcopy(SETTING_6_2_1)
SETTING_6_2_1_2['flag3'][1].update  ({
         'user_esp8285_enable':     (Platform.ALL,   '<L', (0x3A0,1, 1), (None, None,                           ('SetOption',   '"SetOption51 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_2_1_3 = copy.deepcopy(SETTING_6_2_1_2)
SETTING_6_2_1_3['flag2'][1].update  ({
        'frequency_resolution':     (Platform.ALL,   '<L', (0x5BC,2,11), (None, '0 <= $ <= 3',                  ('Power',       '"FreqRes {}".format($)')) ),
                                    })
SETTING_6_2_1_3['flag3'][1].update  ({
        'time_append_timezone':     (Platform.ALL,   '<L', (0x3A0,1, 2), (None, None,                           ('SetOption',   '"SetOption52 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_2_1_6 = copy.deepcopy(SETTING_6_2_1_3)
SETTING_6_2_1_6.update({
    'energy_power_calibration':     (Platform.ALL,   '<L',  0x364,       (None, None,                           ('Power',       None)) ),
    'energy_voltage_calibration':   (Platform.ALL,   '<L',  0x368,       (None, None,                           ('Power',       None)) ),
    'energy_current_calibration':   (Platform.ALL,   '<L',  0x36C,       (None, None,                           ('Power',       None)) ),
    'energy_frequency_calibration': (Platform.ALL,   '<L',  0x7C8,       (None, '45000 < $ < 65000',            ('Power',       '"FrequencySet {}".format($)')) ),
})
# ======================================================================
SETTING_6_2_1_10 = copy.deepcopy(SETTING_6_2_1_6)
SETTING_6_2_1_10.update({
    'rgbwwTable':                   (Platform.ALL,   'B',   0x71A,       ([5],  None,                           (INTERNAL,      None)) ), # RGBWWTable 255,135,70,255,255
})
# ======================================================================
SETTING_6_2_1_14 = copy.deepcopy(SETTING_6_2_1_10)
SETTING_6_2_1_14.update({
    'weight_reference':             (Platform.ALL,   '<L',  0x7C0,       (None, None,                           ('Management',  '"Sensor34 3 {}".format($)')) ),
    'weight_calibration':           (Platform.ALL,   '<L',  0x7C4,       (None, None,                           ('Management',  '"Sensor34 4 {}".format($)')) ),
    'weight_max':                   (Platform.ALL,   '<H',  0x7BE,       (None, None,                           ('Management',  '"Sensor34 5 {}".format($)')), ('float($) // 1000', 'int($ * 1000)') ),
    'weight_item':                  (Platform.ALL,   '<H',  0x7BC,       (None, None,                           ('Management',  '"Sensor34 6 {}".format($)')), ('int($ * 10)', 'float($) // 10') ),
    'web_refresh':                  (Platform.ALL,   '<H',  0x7CC,       (None, '1000 <= $ <= 10000',           ('Wifi',        '"WebRefresh {}".format($)')) ),
})
SETTING_6_2_1_14['flag2'][1].update ({
        'weight_resolution':        (Platform.ALL,   '<L', (0x5BC,2, 9), (None, '0 <= $ <= 3',                  ('Sensor',      '"WeightRes {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_2_1_19 = copy.deepcopy(SETTING_6_2_1_14)
SETTING_6_2_1_19.update({
    'weight_item':                  (Platform.ALL,   '<L',  0x7B8,       (None, None,                           ('Sensor',      '"Sensor34 6 {}".format($)')), ('int($ * 10)', 'float($) // 10') ),
})
SETTING_6_2_1_20 = SETTING_6_2_1_19
SETTING_6_2_1_20['flag3'][1].update ({
        'gui_hostname_ip':          (Platform.ALL,   '<L', (0x3A0,1,3),  (None, None,                           ('SetOption',   '"SetOption53 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_3_0 = copy.deepcopy(SETTING_6_2_1_20)
SETTING_6_3_0.update({
    'energy_kWhtotal_time':         (Platform.ALL,   '<L',  0x7B4,       (None, None,                           (INTERNAL,      None)) ),
})
# ======================================================================
SETTING_6_3_0_2 = copy.deepcopy(SETTING_6_3_0)
SETTING_6_3_0_2.update({
    'timezone_minutes':             (Platform.ALL,   'B',   0x66D,       (None, None,                           (INTERNAL,      None)) ),
})
SETTING_6_3_0_2['flag'][1].pop('rules_once',None)
SETTING_6_3_0_2['flag'][1].update   ({
        'pressure_conversion':      (Platform.ALL,   '<L', (0x010,1,24), (None, None,                           ('SetOption',   '"SetOption24 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_3_0_4 = copy.deepcopy(SETTING_6_3_0_2)
SETTING_6_3_0_4.update({
    'drivers':                      (Platform.ALL,   '<L',  0x794,       ([3],  None,                           (INTERNAL,      None)), '"0x{:08x}".format($)' ),
    'monitors':                     (Platform.ALL,   '<L',  0x7A0,       (None, None,                           (INTERNAL,      None)), '"0x{:08x}".format($)' ),
    'sensors':                      (Platform.ALL,   '<L',  0x7A4,       ([3],  None,                           (INTERNAL,      None)), '"0x{:08x}".format($)' ),
    'displays':                     (Platform.ALL,   '<L',  0x7B0,       (None, None,                           (INTERNAL,      None)), '"0x{:08x}".format($)' ),
})
SETTING_6_3_0_4['flag3'][1].update ({
        'tuya_apply_o20':           (Platform.ALL,   '<L', (0x3A0,1, 4), (None, None,                           ('SetOption',   '"SetOption54 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_3_0_8 = copy.deepcopy(SETTING_6_3_0_4)
SETTING_6_3_0_8['flag3'][1].update ({
        'hass_short_discovery_msg': (Platform.ALL,   '<L', (0x3A0,1, 5), (None, None,                           ('SetOption',   '"SetOption55 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_3_0_10 = copy.deepcopy(SETTING_6_3_0_8)
SETTING_6_3_0_10['flag3'][1].update ({
        'use_wifi_scan':            (Platform.ALL,   '<L', (0x3A0,1, 6), (None, None,                           ('SetOption',   '"SetOption56 {}".format($)')) ),
        'use_wifi_rescan':          (Platform.ALL,   '<L', (0x3A0,1, 7), (None, None,                           ('SetOption',   '"SetOption57 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_3_0_11 = copy.deepcopy(SETTING_6_3_0_10)
SETTING_6_3_0_11['flag3'][1].update ({
        'receive_raw':          	(Platform.ALL,   '<L', (0x3A0,1, 8), (None, None,                           ('SetOption',   '"SetOption58 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_3_0_13 = copy.deepcopy(SETTING_6_3_0_11)
SETTING_6_3_0_13['flag3'][1].update ({
        'hass_tele_on_power':       (Platform.ALL,   '<L', (0x3A0,1, 9), (None, None,                           ('SetOption',   '"SetOption59 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_3_0_14 = copy.deepcopy(SETTING_6_3_0_13)
SETTING_6_3_0_14['flag2'][1].update ({
        'calc_resolution':          (Platform.ALL,   '<L', (0x5BC,3, 6), (None, '0 <= $ <= 7',                  ('Rules',       '"CalcRes {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_3_0_15 = copy.deepcopy(SETTING_6_3_0_14)
SETTING_6_3_0_15['flag3'][1].update ({
        'sleep_normal':             (Platform.ALL,   '<L', (0x3A0,1,10), (None, None,                           ('SetOption',   '"SetOption60 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_3_0_16 = copy.deepcopy(SETTING_6_3_0_15)
SETTING_6_3_0_16['mcp230xx_config'][1].update ({
        'int_retain_flag':          (Platform.ALL,   '<L', (0x6F6,1,12), (None, None,                           ('Sensor',      None)) ),
                                    })
SETTING_6_3_0_16['flag3'][1].update ({
        'button_switch_force_local':(Platform.ALL,   '<L', (0x3A0,1,11), (None, None,                           ('SetOption',   '"SetOption61 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_4_0_2 = copy.deepcopy(SETTING_6_3_0_16)
SETTING_6_4_0_2['flag3'][1].pop('hass_short_discovery_msg',None)
# ======================================================================
SETTING_6_4_1_4 = copy.deepcopy(SETTING_6_4_0_2)
SETTING_6_4_1_4['flag3'][1].update ({
        'mdns_enabled':             (Platform.ALL,   '<L', (0x3A0,1, 5), (None, None,                           ('SetOption',   '"SetOption55 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_4_1_7 = copy.deepcopy(SETTING_6_4_1_4)
SETTING_6_4_1_7['flag3'][1].update ({
        'no_pullup':                (Platform.ALL,   '<L', (0x3A0,1,12), (None, None,                           ('SetOption',   '"SetOption62 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_4_1_8 = copy.deepcopy(SETTING_6_4_1_7)
SETTING_6_4_1_8.update              ({
    'my_gp':                        (Platform.ALL,   'B',   0x484,       ([17], None,                           ('Management',  '"Gpio{} {}".format(#-1,$)')) ),
                                    })
SETTING_6_4_1_8['flag3'][1].update ({
        'split_interlock':          (Platform.ALL,   '<L', (0x3A0,1,13), (None, None,                           ('SetOption',   '"SetOption63 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_4_1_11 = copy.deepcopy(SETTING_6_4_1_8)
SETTING_6_4_1_11['flag3'][1].pop('split_interlock',None)
SETTING_6_4_1_11.update            ({
    'interlock':                    (Platform.ALL,   'B',   0x4CA,       ([4],  None,                           ('Control',     None)), '"0x{:02x}".format($)' ),
                                    })
SETTING_6_4_1_11['flag'][1].update ({
        'interlock':                (Platform.ALL,   '<L', (0x010,1,14), (None, None,                           ('Control',     '"Interlock {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_4_1_13 = copy.deepcopy(SETTING_6_4_1_11)
SETTING_6_4_1_13.update            ({
    'SensorBits1':                 (Platform.ALL, {
        'mhz19b_abc_disable':       (Platform.ALL,   'B',  (0x717,1, 7), (None, None,                           ('Sensor',      '"Sensor15 {}".format($)')) ),
                                    },                      0x717,       (None, None,                           (VIRTUAL,       None)), (None,      None) ),
                                    })
# ======================================================================
SETTING_6_4_1_16 = copy.deepcopy(SETTING_6_4_1_13)
SETTING_6_4_1_16.update            ({
    'user_template':               (Platform.ALL, {
        'base':                     (Platform.ALL,   'B',   0x71F,       (None, None,                           ('Management',  '"Template {{\\\"BASE\\\":{}}}".format($)')), ('$+1','$-1') ),
        'name':                     (Platform.ALL,   '15s', 0x720,       (None, None,                           ('Management',  '"Template {{\\\"NAME\\\":\\\"{}\\\"}}".format($)' )) ),
        'gpio':                     (Platform.ALL,   'B',   0x72F,       ([13], None,                           ('Management',  '"Template {{\\\"GPIO\\\":{}}}".format(@["user_template"]["gpio"]) if 1==# else None')) ),
        'flag':                     (Platform.ALL, {
            'adc0':                 (Platform.ALL,   'B',  (0x73C,4,0),  (None, None,                           ('Management',  '"Template {{\\\"FLAG\\\":{}}}".format($)')) ),
                                    },                      0x73C,       (None, None,                           ('Management',  None))
                                    ),
                                    },                      0x71F,       (None, None,                           ('Management',  None))
                                    ),
                                   })
# ======================================================================
SETTING_6_4_1_17 = copy.deepcopy(SETTING_6_4_1_16)
SETTING_6_4_1_17['flag3'][1].pop('no_pullup',None)
# ======================================================================
SETTING_6_4_1_18 = copy.deepcopy(SETTING_6_4_1_17)
SETTING_6_4_1_18['flag3'][1].update ({
        'no_hold_retain':           (Platform.ALL,   '<L', (0x3A0,1,12), (None, None,                           ('SetOption',   '"SetOption62 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_5_0_3 = copy.deepcopy(SETTING_6_4_1_18)
SETTING_6_5_0_3.update              ({
    'novasds_period':               (Platform.ALL,   'B',   0x73D,       (None, '1 <= $ <= 255',                ('Sensor',      '"Sensor20 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_5_0_6 = copy.deepcopy(SETTING_6_5_0_3)
SETTING_6_5_0_6.update              ({
    'web_color':                    (Platform.ALL,   '3B',  0x73E,       ([18], None,                           ('Wifi',        '"WebColor{} {}{:06x}".format(#,chr(35),int($,0))')), '"0x{:06x}".format($)' ),
                                    })
# ======================================================================
SETTING_6_5_0_7 = copy.deepcopy(SETTING_6_5_0_6)
SETTING_6_5_0_7.update              ({
    'ledmask':                      (Platform.ALL,   '<H',  0x7BC,       (None, None,                           ('Control',     '"LedMask {}".format($)')), '"0x{:04x}".format($)' ),
                                    })
# ======================================================================
SETTING_6_5_0_9 = copy.deepcopy(SETTING_6_5_0_7)
SETTING_6_5_0_9['flag3'][1].update ({
        'no_power_feedback':        (Platform.ALL,   '<L', (0x3A0,1,13), (None, None,                           ('SetOption',   '"SetOption63 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_5_0_10 = copy.deepcopy(SETTING_6_5_0_9)
SETTING_6_5_0_10.update             ({
    'my_adc0':                      (Platform.ALL,   'B',   0x495,       (None, None,                           ('Sensor',      '"Adc {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_5_0_11 = copy.deepcopy(SETTING_6_5_0_10)
SETTING_6_5_0_11['flag3'][1].update ({
        'use_underscore':           (Platform.ALL,   '<L', (0x3A0,1,14), (None, None,                           ('SetOption',   '"SetOption64 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_5_0_12 = copy.deepcopy(SETTING_6_5_0_11)
SETTING_6_5_0_12.pop('drivers',None)
SETTING_6_5_0_12.update             ({
    'adc_param_type':               (Platform.ALL,   'B',   0x1D5,       (None, '2 <= $ <= 3',                  ('Sensor',      '"AdcParam {type},{param1},{param2},{param3}".format(type=@["my_adc0"],param1=@["adc_param1"],param2=@["adc_param2"],param3=@["adc_param3"]/10000)')) ),
    'adc_param1':                   (Platform.ALL,   '<L',  0x794,       (None, None,                           ('Sensor',      None)) ),
    'adc_param2':                   (Platform.ALL,   '<L',  0x798,       (None, None,                           ('Sensor',      None)) ),
    'adc_param3':                   (Platform.ALL,   '<l',  0x79C,       (None, None,                           ('Sensor',      None)) ),
    'sps30_inuse_hours':            (Platform.ALL,   'B',   0x1E8,       (None, None,                           (INTERNAL,      None)) ),
                                    })
# ======================================================================
SETTING_6_5_0_15 = copy.deepcopy(SETTING_6_5_0_12)
SETTING_6_5_0_15['flag3'][1].update ({
        'tuya_show_dimmer':         (Platform.ALL,   '<L', (0x3A0,1,15), (None, None,                           ('SetOption',   '"SetOption65 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_6_0_1 = copy.deepcopy(SETTING_6_5_0_15)
SETTING_6_6_0_1['flag3'][1].update ({
        'tuya_dimmer_range_255':    (Platform.ALL,   '<L', (0x3A0,1,16), (None, None,                           ('SetOption',   '"SetOption66 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_6_0_2 = copy.deepcopy(SETTING_6_6_0_1)
SETTING_6_6_0_2['flag3'][1].update ({
        'buzzer_enable':            (Platform.ALL,   '<L', (0x3A0,1,17), (None, None,                           ('SetOption',   '"SetOption67 {}".format($)')) ),
                                    })
SETTING_6_6_0_2.update              ({
    'display_width':                (Platform.ALL,   '<H',  0x774,       (None, None,                           ('Display',     '"DisplayWidth {}".format($)')) ),
    'display_height':               (Platform.ALL,   '<H',  0x776,       (None, None,                           ('Display',     '"DisplayHeight {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_6_0_3 = copy.deepcopy(SETTING_6_6_0_2)
SETTING_6_6_0_3['flag3'][1].update ({
        'pwm_multi_channels':       (Platform.ALL,   '<L', (0x3A0,1,18), (None, None,                           ('SetOption',   '"SetOption68 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_6_0_5 = copy.deepcopy(SETTING_6_6_0_3)
SETTING_6_6_0_5.update              ({
    'sensors':                      (Platform.ALL,   '<L',  0x7A4,       ([3],  None,                           ('Wifi',        cmnd_websensor)), '"0x{:08x}".format($)' ),
                                    })
SETTING_6_6_0_5['flag3'][1].update ({
        'tuya_dimmer_min_limit':    (Platform.ALL,   '<L', (0x3A0,1,19), (None, None,                           ('SetOption',   '"SetOption69 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_6_0_6 = copy.deepcopy(SETTING_6_6_0_5)
SETTING_6_6_0_6['flag3'][1].pop('tuya_show_dimmer',None)
SETTING_6_6_0_6['flag3'][1].update ({
        'tuya_disable_dimmer':      (Platform.ALL,   '<L', (0x3A0,1,15), (None, None,                           ('SetOption',   '"SetOption65 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_6_0_7 = copy.deepcopy(SETTING_6_6_0_6)
SETTING_6_6_0_7.update              ({
    'energy_usage':                 (Platform.ALL, {
        'usage1_kWhtotal':          (Platform.ALL,   '<L',  0x77C,       (None, None,                           ('Power',       None)) ),
        'usage1_kWhtoday':          (Platform.ALL,   '<L',  0x780,       (None, None,                           ('Power',       None)) ),
        'return1_kWhtotal':         (Platform.ALL,   '<L',  0x784,       (None, None,                           ('Power',       None)) ),
        'return2_kWhtotal':         (Platform.ALL,   '<L',  0x788,       (None, None,                           ('Power',       None)) ),
        'last_usage_kWhtotal':      (Platform.ALL,   '<L',  0x78C,       (None, None,                           ('Power',       None)) ),
        'last_return_kWhtotal':     (Platform.ALL,   '<L',  0x790,       (None, None,                           ('Power',       None)) ),
                                    },                      0x77C,       (None, None,                           ('Power',       None)) ),
                                    })
# ======================================================================
SETTING_6_6_0_8 = copy.deepcopy(SETTING_6_6_0_7)
SETTING_6_6_0_8['flag3'][1].update ({
        'energy_weekend':           (Platform.ALL,   '<L', (0x3A0,1,20), (None, None,                           ('Power',       '"Tariff3 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_6_0_9 = copy.deepcopy(SETTING_6_6_0_8)
SETTING_6_6_0_9.update              ({
    'baudrate':                     (Platform.ALL,   '<H',  0x778,       (None, None,                           ('Serial',      '"Baudrate {}".format($)')), ('$ * 1200','$ // 1200') ),
    'sbaudrate':                    (Platform.ALL,   '<H',  0x77A,       (None, None,                           ('Serial',      '"SBaudrate {}".format($)')), ('$ * 1200','$ // 1200') ),
                                    })
# ======================================================================
SETTING_6_6_0_10 = copy.deepcopy(SETTING_6_6_0_9)
SETTING_6_6_0_10['flag3'][1].pop('tuya_disable_dimmer',None)
SETTING_6_6_0_10.update             ({
    'cfg_timestamp':                (Platform.ALL,   '<L',  0xFF8,       (None, None,                           ('System',      None)) ),
    'cfg_crc32':                    (Platform.ALL,   '<L',  0xFFC,       (None, None,                           ('System',      None)), '"0x{:08x}".format($)' ),
    'tuya_fnid_map':                (Platform.ALL, {
        'fnid':                     (Platform.ALL,   'B',   0xE00,       (None, None,                           ('Management',  '"TuyaMCU {},{}".format($,@["tuya_fnid_map"][#-1]["dpid"]) if ($!=0 or @["tuya_fnid_map"][#-1]["dpid"]!=0) else None')) ),
        'dpid':                     (Platform.ALL,   'B',   0xE01,       (None, None,                           ('Management',  None)) ),
                                    },                      0xE00,       ([16], None,                           ('Management',  None)), (None,      None) ),
                                    })
SETTING_6_6_0_10['flag2'][1].update ({
        'time_format':              (Platform.ALL,   '<L', (0x5BC,2, 4), (None, None,                           ('Management', '"Time {}".format($+1)')) ),
                                    })
SETTING_6_6_0_10['flag3'][1].pop('tuya_show_dimmer',None)
# ======================================================================
SETTING_6_6_0_11 = copy.deepcopy(SETTING_6_6_0_10)
SETTING_6_6_0_11.update             ({
    'ina226_r_shunt':               (Platform.ALL,   '<H',  0xE20,       ([4], None,                            ('Power',       '"Sensor54 {}1 {}".format(#,$)')) ),
    'ina226_i_fs':                  (Platform.ALL,   '<H',  0xE28,       ([4], None,                            ('Power',       '"Sensor54 {}2 {}".format(#,$)')) ),
                                    })
# ======================================================================
SETTING_6_6_0_12 = copy.deepcopy(SETTING_6_6_0_11)
SETTING_6_6_0_12.update             ({
    'register8_ENERGY_TARIFF1_ST':  (Platform.ALL,   'B',   0x1D6,       (None, None,                           ('Power',       '"Tariff1 {},{}".format($,@["register8_ENERGY_TARIFF1_DS"])')) ),
    'register8_ENERGY_TARIFF2_ST':  (Platform.ALL,   'B',   0x1D7,       (None, None,                           ('Power',       '"Tariff2 {},{}".format($,@["register8_ENERGY_TARIFF2_DS"])')) ),
    'register8_ENERGY_TARIFF1_DS':  (Platform.ALL,   'B',   0x1D8,       (None, None,                           ('Power',       None)) ),
    'register8_ENERGY_TARIFF2_DS':  (Platform.ALL,   'B',   0x1D9,       (None, None,                           ('Power',       None)) ),
                                    })
SETTING_6_6_0_12['flag3'][1].update ({
        'energy_weekend':           (Platform.ALL,   '<L', (0x3A0,1,20), (None, None,                           ('Power',       '"Tariff9 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_6_0_13 = copy.deepcopy(SETTING_6_6_0_12)
SETTING_6_6_0_13['SensorBits1'][1].update ({
        'hx711_json_weight_change': (Platform.ALL,   'B',  (0x717,1, 6), (None, None,                           ('Sensor',      '"Sensor34 8 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_6_0_14 = copy.deepcopy(SETTING_6_6_0_13)
SETTING_6_6_0_14.pop('register8_ENERGY_TARIFF1_ST',None)
SETTING_6_6_0_14.pop('register8_ENERGY_TARIFF2_ST',None)
SETTING_6_6_0_14.pop('register8_ENERGY_TARIFF1_DS',None)
SETTING_6_6_0_14.pop('register8_ENERGY_TARIFF2_DS',None)
SETTING_6_6_0_14.update             ({
    'register8':                    (Platform.ALL,   'B',   0x1D6,       ([16], None,                           ('Power',       None)) ),
    'tariff1_0':                    (Platform.ALL,   '<H',  0xE30,       (None, None,                           ('Power',       '"Tariff1 {:02d}:{:02d},{:02d}:{:02d}".format(@["tariff1_0"]//60,@["tariff1_0"]%60,@["tariff1_1"]//60,@["tariff1_1"]%60)')) ),
    'tariff1_1':                    (Platform.ALL,   '<H',  0xE32,       (None, None,                           ('Power',       None)) ),
    'tariff2_0':                    (Platform.ALL,   '<H',  0xE34,       (None, None,                           ('Power',       '"Tariff2 {:02d}:{:02d},{:02d}:{:02d}".format(@["tariff2_0"]//60,@["tariff2_0"]%60,@["tariff2_1"]//60,@["tariff2_1"]%60)')) ),
    'tariff2_1':                    (Platform.ALL,   '<H',  0xE36,       (None, None,                           ('Power',       None)) ),
    'mqttlog_level':                (Platform.ALL,   'B',   0x1E7,       (None, None,                           ('Management', '"MqttLog {}".format($)')) ),
    'pcf8574_config':               (Platform.ALL,   'B',   0xE88,       ([8],  None,                           ('Sensor',      None)) ),
    'shutter_accuracy':             (Platform.ALL,   'B',   0x1E6,       (None, None,                           ('Shutter',     None)) ),
    'shutter_opentime':             (Platform.ALL,   '<H',  0xE40,       ([4],  None,                           ('Shutter',     '"ShutterOpenDuration{} {:.1f}".format(#,float($)/10.0)')) ),
    'shutter_closetime':            (Platform.ALL,   '<H',  0xE48,       ([4],  None,                           ('Shutter',     '"ShutterCloseDuration{} {:.1f}".format(#,float($)/10.0)')) ),
    'shuttercoeff':                 (Platform.ALL,   '<H',  0xE50,       ([5,4],None,                           ('Shutter',     None)) ),
    'shutter_invert':               (Platform.ALL,   'B',   0xE78,       ([4],  None,                           ('Shutter',     '"ShutterInvert{} {}".format(#,$)')) ),
    'shutter_set50percent':         (Platform.ALL,   'B',   0xE7C,       ([4],  None,                           ('Shutter',     '"ShutterSetHalfway{} {}".format(#,$)')) ),
    'shutter_position':             (Platform.ALL,   'B',   0xE80,       ([4],  None,                           ('Shutter',     '"ShutterPosition{} {}".format(#,$)')) ),
    'shutter_startrelay':           (Platform.ALL,   'B',   0xE84,       ([4],  None,                           ('Shutter',     '"ShutterRelay{} {}".format(#,$)')) ),
                                    })
SETTING_6_6_0_14['flag3'][1].update ({
        'dds2382_model':            (Platform.ALL,   '<L', (0x3A0,1,21), (None, None,                           ('SetOption',   '"SetOption71 {}".format($)')) ),
        'shutter_mode':             (Platform.ALL,   '<L', (0x3A0,1,30), (None, None,                           ('SetOption',   '"SetOption80 {}".format($)')) ),
        'pcf8574_ports_inverted':   (Platform.ALL,   '<L', (0x3A0,1,31), (None, None,                           ('SetOption',   '"SetOption81 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_6_0_15 = copy.deepcopy(SETTING_6_6_0_14)
SETTING_6_6_0_15['flag3'][1].update ({
        'hardware_energy_total':    (Platform.ALL,   '<L', (0x3A0,1,22), (None, None,                           ('SetOption',   '"SetOption72 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_6_0_18 = copy.deepcopy(SETTING_6_6_0_15)
SETTING_6_6_0_18['flag3'][1].pop('tuya_dimmer_range_255',None)
SETTING_6_6_0_18['flag3'][1].pop('tuya_dimmer_min_limit',None)
SETTING_6_6_0_18.pop('novasds_period',None)
SETTING_6_6_0_18.update             ({
    'dimmer_hw_min':                (Platform.ALL,   '<H',  0xE90,       (None, None,                           ('Light',       '"DimmerRange {},{}".format($,@["dimmer_hw_max"])')) ),
    'dimmer_hw_max':                (Platform.ALL,   '<H',  0xE92,       (None, None,                           ('Light',       None)) ),
    'deepsleep':                    (Platform.ALL,   '<H',  0xE94,       (None, '0 or 10 <= $ <= 86400',        ('Management',  '"DeepSleepTime {}".format($)')) ),
    'novasds_startingoffset':       (Platform.ALL,   'B',   0x73D,       (None, '1 <= $ <= 255',                ('Sensor',      '"Sensor20 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_6_0_20 = copy.deepcopy(SETTING_6_6_0_18)
SETTING_6_6_0_20['flag3'][1].update ({
        'fast_power_cycle_disable': (Platform.ALL,   '<L', (0x3A0,1,15), (None, None,                           ('SetOption',   '"SetOption65 {}".format($)')) ),
                                    })
SETTING_6_6_0_20.update             ({
    'energy_power_delta':           (Platform.ALL,   '<H',  0xE98,       (None, '0 <= $ < 32000',               ('Power',       '"PowerDelta {}".format($)')) ),
                                    })
# ======================================================================
SETTING_6_6_0_21 = copy.deepcopy(SETTING_6_6_0_20)
SETTING_6_6_0_21['flag'][1].pop('value_units',None)
SETTING_6_6_0_21['flag3'][1].pop('tuya_dimmer_range_255',None)
SETTING_6_6_0_21['flag3'][1].update ({
        'tuya_serial_mqtt_publish': (Platform.ALL,   '<L', (0x3A0,1,16), (None, None,                           ('SetOption',   '"SetOption66 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_7_0_0_1 = copy.deepcopy(SETTING_6_6_0_21)
SETTING_7_0_0_1.pop('register8',None)
SETTING_7_0_0_1.update             ({
    'shutter_motordelay':           (Platform.ALL,   'B',   0xE9A,       ([4],  None,                           ('Shutter',     '"ShutterMotorDelay{} {:.1f}".format(#,float($)/20.0)')) ),
    'flag4':                        (Platform.ALL,   '<L',  0x1E0,       (None, None,                           (INTERNAL,      None)), '"0x{:08x}".format($)' ),
                                    })
SETTING_7_0_0_1['flag3'][1].update ({
        'cors_enabled':             (Platform.ALL,   '<L', (0x3A0,1,23), (None, None,                           ('SetOption',   '"SetOption73 {}".format($)')) ),
        'ds18x20_internal_pullup':  (Platform.ALL,   '<L', (0x3A0,1,24), (None, None,                           ('SetOption',   '"SetOption74 {}".format($)')) ),
        'grouptopic_mode':          (Platform.ALL,   '<L', (0x3A0,1,25), (None, None,                           ('SetOption',   '"SetOption75 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_7_0_0_2 = copy.deepcopy(SETTING_7_0_0_1)
SETTING_7_0_0_2.update             ({
    'web_color2':                   (Platform.ALL,   '3B',  0xEA0,       ([1],  None,                           ('Wifi',        '"WebColor{} {}{:06x}".format(#+18,chr(35),int($,0))')), '"0x{:06x}".format($)' ),
                                    })
# ======================================================================
SETTING_7_0_0_3 = copy.deepcopy(SETTING_7_0_0_2)
SETTING_7_0_0_3.update             ({
    'i2c_drivers':                  (Platform.ALL,   '<L',  0xFEC,       ([3],  None,                           ('Management',  None)),'"0x{:08x}".format($)' ),
                                    })
# ======================================================================
SETTING_7_0_0_4 = copy.deepcopy(SETTING_7_0_0_3)
SETTING_7_0_0_4.update             ({
    'wifi_output_power':            (Platform.ALL,   'B',   0x1E5,       (None, None,                           ('Wifi',        '"WifiPower {:.1f}".format(float($)/10.0)')) ),
                                    })
SETTING_7_0_0_4['flag3'][1].update ({
        'bootcount_update':         (Platform.ALL,   '<L', (0x3A0,1,26), (None, None,                           ('SetOption',   '"SetOption76 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_7_0_0_5 = copy.deepcopy(SETTING_7_0_0_4)
SETTING_7_0_0_5.update             ({
    'temp_comp':                    (Platform.ALL,   'b',   0xE9E,       (None, '-127 < $ < 127',               ('Sensor',      '"TempOffset {:.1f}".format(float($)/10.0)')) ),
                                    })
# ======================================================================
SETTING_7_0_0_6 = copy.deepcopy(SETTING_7_0_0_5)
SETTING_7_0_0_6['flag3'][1].update ({
        'slider_dimmer_stay_on':    (Platform.ALL,   '<L', (0x3A0,1,27), (None, None,                           ('SetOption',   '"SetOption77 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_7_1_2_2 = copy.deepcopy(SETTING_7_0_0_6)
SETTING_7_1_2_2.update             ({
    'serial_config':                (Platform.ALL,   'b',   0x14E,       (None, '0 <= $ <= 23',                 ('Serial',      '"SerialConfig {}".format(("5N1","6N1","7N1","8N1","5N2","6N2","7N2","8N2","5E1","6E1","7E1","8E1","5E2","6E2","7E2","8E2","5O1","6O1","7O1","8O1","5O2","6O2","7O2","8O2")[$ % 24])')) ),
                                    })
# ======================================================================
SETTING_7_1_2_3 = copy.deepcopy(SETTING_7_1_2_2)
SETTING_7_1_2_3['flag3'][1].pop('cors_enabled',None)
SETTING_7_1_2_3.update             ({
    'cors_domain':                  (Platform.ALL,   '33s', 0xEA6,       (None, None,                           ('Wifi',        '"CORS {}".format($ if len($) else \'"\')')) ),
    'weight_change':                (Platform.ALL,   'B',   0xE9F,       (None, None,                           ('Management',  '"Sensor34 9 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_7_1_2_5 = copy.deepcopy(SETTING_7_1_2_3)
SETTING_7_1_2_5.update             ({
    'seriallog_level':              (Platform.ALL,   'B',   0x452,       (None, '0 <= $ <= 5',                  ('Management',  '"SerialLog {}".format($)')) ),
    'sta_config':                   (Platform.ALL,   'B',   0xEC7,       (None, '0 <= $ <= 5',                  ('Wifi',        '"WifiConfig {}".format($)')) ),
    'sta_active':                   (Platform.ALL,   'B',   0xEC8,       (None, '0 <= $ <= 1',                  ('Wifi',        '"AP {}".format($)')) ),
    'rule_stop':                    (Platform.ALL, {
        'rule1':                    (Platform.ALL,   'B',  (0xEC9,1,0),  (None, None,                           ('Rules',       '"Rule1 {}".format($+8)')) ),
        'rule2':                    (Platform.ALL,   'B',  (0xEC9,1,1),  (None, None,                           ('Rules',       '"Rule2 {}".format($+8)')) ),
        'rule3':                    (Platform.ALL,   'B',  (0xEC9,1,2),  (None, None,                           ('Rules',       '"Rule3 {}".format($+8)')) ),
                                     },     0xEC9,        None),
    'syslog_port':                  (Platform.ALL,   '<H',  0xECA,       (None, '1 <= $ <= 32766',              ('Management',  '"LogPort {}".format($)')) ),
    'syslog_level':                 (Platform.ALL,   'B',   0xECC,       (None, '0 <= $ <= 4',                  ('Management',  '"SysLog {}".format($)')) ),
    'webserver':                    (Platform.ALL,   'B',   0xECD,       (None, '0 <= $ <= 2',                  ('Wifi',        '"WebServer {}".format($)')) ),
    'weblog_level':                 (Platform.ALL,   'B',   0xECE,       (None, '0 <= $ <= 4',                  ('Management',  '"WebLog {}".format($)')) ),
    'mqtt_fingerprint1':            (Platform.ALL,   'B',   0xECF,       ([20], None,                           ('MQTT',        '"MqttFingerprint1 {}".format(" ".join("{:02X}".format((int(c,0))) for c in @["mqtt_fingerprint1"])) if 1==# else None')), '"0x{:02x}".format($)' ),
    'mqtt_fingerprint2':            (Platform.ALL,   'B',   0xECF+20,    ([20], None,                           ('MQTT',        '"MqttFingerprint2 {}".format(" ".join("{:02X}".format((int(c,0))) for c in @["mqtt_fingerprint2"])) if 1==# else None')), '"0x{:02x}".format($)' ),
    'adc_param_type':               (Platform.ALL,   'B',   0xEF7,       (None, '2 <= $ <= 3',                  ('Sensor',       '"AdcParam {type},{param1},{param2},{param3}".format(type=$,param1=@["adc_param1"],param2=@["adc_param2"],param3=@["adc_param3"]//10000)')) ),
                                    })
# ======================================================================
SETTING_7_1_2_6 = copy.deepcopy(SETTING_7_1_2_5)
SETTING_7_1_2_6.update             ({
    'flag4':                        (Platform.ALL,   '<L',  0xEF8,       (None, None,                           (INTERNAL,      None)), '"0x{:08x}".format($)' ),
    'serial_config':                (Platform.ALL,   'b',   0xEFE,       (None, '0 <= $ <= 23',                 ('Serial',      '"SerialConfig {}".format(("5N1","6N1","7N1","8N1","5N2","6N2","7N2","8N2","5E1","6E1","7E1","8E1","5E2","6E2","7E2","8E2","5O1","6O1","7O1","8O1","5O2","6O2","7O2","8O2")[$ % 24])')) ),
    'wifi_output_power':            (Platform.ALL,   'B',   0xEFF,       (None, None,                           ('Wifi',        '"WifiPower {:.1f}".format(float($)/10.0)')) ),
    'mqtt_port':                    (Platform.ALL,   '<H',  0xEFC,       (None, None,                           ('MQTT',        '"MqttPort {}".format($)')) ),
    'shutter_accuracy':             (Platform.ALL,   'B',   0xF00,       (None, None,                           ('Shutter',     None)) ),
    'mqttlog_level':                (Platform.ALL,   'B',   0xF01,       (None, None,                           ('Management',  '"MqttLog {}".format($)')) ),
    'sps30_inuse_hours':            (Platform.ALL,   'B',   0xF02,       (None, None,                           (INTERNAL,      None)) ),
                                    })
SETTING_7_1_2_6['flag3'][1].update ({
        'compatibility_check':      (Platform.ALL,   '<L', (0x3A0,1,28), (None, None,                           ('SetOption',   '"SetOption78 {}".format($)')) ),
                                    })
# ======================================================================
# v8.x.x.x: Index numbers for indexed strings
SETTINGSTEXTINDEX =['SET_OTAURL',
                    'SET_MQTTPREFIX1', 'SET_MQTTPREFIX2', 'SET_MQTTPREFIX3',
                    'SET_STASSID1', 'SET_STASSID2',
                    'SET_STAPWD1', 'SET_STAPWD2',
                    'SET_HOSTNAME', 'SET_SYSLOG_HOST',
                    'SET_WEBPWD', 'SET_CORS',
                    'SET_MQTT_HOST', 'SET_MQTT_CLIENT',
                    'SET_MQTT_USER', 'SET_MQTT_PWD',
                    'SET_MQTT_FULLTOPIC', 'SET_MQTT_TOPIC',
                    'SET_MQTT_BUTTON_TOPIC', 'SET_MQTT_SWITCH_TOPIC', 'SET_MQTT_GRP_TOPIC',
                    'SET_STATE_TXT1', 'SET_STATE_TXT2', 'SET_STATE_TXT3', 'SET_STATE_TXT4',
                    'SET_NTPSERVER1', 'SET_NTPSERVER2', 'SET_NTPSERVER3',
                    'SET_MEM1', 'SET_MEM2', 'SET_MEM3', 'SET_MEM4', 'SET_MEM5', 'SET_MEM6', 'SET_MEM7', 'SET_MEM8',
                    'SET_MEM9', 'SET_MEM10', 'SET_MEM11', 'SET_MEM12', 'SET_MEM13', 'SET_MEM14', 'SET_MEM15', 'SET_MEM16',
                    'SET_FRIENDLYNAME1', 'SET_FRIENDLYNAME2', 'SET_FRIENDLYNAME3', 'SET_FRIENDLYNAME4',
                    'SET_FRIENDLYNAME5', 'SET_FRIENDLYNAME6', 'SET_FRIENDLYNAME7', 'SET_FRIENDLYNAME8',
                    'SET_BUTTON1', 'SET_BUTTON2', 'SET_BUTTON3', 'SET_BUTTON4', 'SET_BUTTON5', 'SET_BUTTON6', 'SET_BUTTON7', 'SET_BUTTON8',
                    'SET_BUTTON9', 'SET_BUTTON10', 'SET_BUTTON11', 'SET_BUTTON12', 'SET_BUTTON13', 'SET_BUTTON14', 'SET_BUTTON15', 'SET_BUTTON16',
                    'SET_MQTT_GRP_TOPIC2', 'SET_MQTT_GRP_TOPIC3', 'SET_MQTT_GRP_TOPIC4',
                    'SET_TEMPLATE_NAME',
                    'SET_DEV_GROUP_NAME1', 'SET_DEV_GROUP_NAME2', 'SET_DEV_GROUP_NAME3', 'SET_DEV_GROUP_NAME4',
                    'SET_MAX']
# ----------------------------------------------------------------------
SETTING_8_0_0_1 = copy.deepcopy(SETTING_7_1_2_6)
SETTING_8_0_0_1.update             ({
    'ota_url':                      (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_OTAURL')),
                                                                         (None, None,                           ('Management',  '"OtaUrl {}".format($)')) ),
    'mqtt_prefix':                  (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_MQTTPREFIX1')),
                                                                         ([3],  None,                           ('MQTT',        '"Prefix{} {}".format(#,$)')) ),
    'sta_ssid':                     (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_STASSID1')),
                                                                         ([2],  None,                           ('Wifi',        '"SSId{} {}".format(#,$)')) ),
    'sta_pwd':                      (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_STAPWD1')),
                                                                         ([2],  None,                           ('Wifi',        '"Password{} {}".format(#,$)')), (passwordread,passwordwrite) ),
    'hostname':                     (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_HOSTNAME')),
                                                                         (None, None,                           ('Wifi',        '"Hostname {}".format($)')) ),
    'syslog_host':                  (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_SYSLOG_HOST')),
                                                                         (None, None,                           ('Management',  '"LogHost {}".format($)')) ),
    'web_password':                 (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_WEBPWD')),
                                                                         (None, None,                           ('Wifi',        '"WebPassword {}".format($)')), (passwordread,passwordwrite) ),
    'cors_domain':                  (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_CORS')),
                                                                         (None, None,                           ('Wifi',        '"CORS {}".format($ if len($) else \'"\')')) ),
    'mqtt_host':                    (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_MQTT_HOST')),
                                                                         (None, None,                           ('MQTT',        '"MqttHost {}".format($)')) ),
    'mqtt_client':                  (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_MQTT_CLIENT')),
                                                                         (None, None,                           ('MQTT',        '"MqttClient {}".format($)')) ),
    'mqtt_user':                    (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_MQTT_USER')),
                                                                         (None, None,                           ('MQTT',        '"MqttUser {}".format($)')) ),
    'mqtt_pwd':                     (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_MQTT_PWD')),
                                                                        (None, None,                           ('MQTT',        '"MqttPassword {}".format($)')), (passwordread,passwordwrite) ),
    'mqtt_fulltopic':               (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_MQTT_FULLTOPIC')),
                                                                         (None, None,                           ('MQTT',        '"FullTopic {}".format($)')) ),
    'mqtt_topic':                   (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_MQTT_TOPIC')),
                                                                         (None, None,                           ('MQTT',        '"FullTopic {}".format($)')) ),
    'button_topic':                 (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_MQTT_BUTTON_TOPIC')),
                                                                         (None, None,                           ('MQTT',        '"ButtonTopic {}".format($)')) ),
    'switch_topic':                 (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_MQTT_SWITCH_TOPIC')),
                                                                         (None, None,                           ('MQTT',        '"SwitchTopic {}".format($)')) ),
    'mqtt_grptopic':                (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_MQTT_GRP_TOPIC')),
                                                                         (None, None,                           ('MQTT',        '"GroupTopic {}".format($)')) ),
    'state_text':                   (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_STATE_TXT1')),
                                                                         ([4],  None,                           ('MQTT',        '"StateText{} {}".format(#,$)')) ),
    'ntp_server':                   (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_NTPSERVER1')),
                                                                         ([3],  None,                           ('Wifi',        '"NtpServer{} {}".format(#,$)')) ),
    'mems':                         (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_MEM1')),
                                                                         ([16], None,                           ('Rules',       '"Mem{} {}".format(#,"\\"" if len($) == 0 else $)')) ),
    'friendlyname':                 (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_FRIENDLYNAME1')),
                                                                         ([4],  None,                           ('Management',  '"FriendlyName{} {}".format(#,"\\"" if len($) == 0 else $)')) ),
                                    })
# ======================================================================
SETTING_8_1_0_0 = copy.deepcopy(SETTING_8_0_0_1)
SETTING_8_1_0_0.update             ({
    'friendlyname':                 (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_FRIENDLYNAME1')),
                                                                         ([8],  None,                           ('Management',  '"FriendlyName{} {}".format(#,"\\"" if len($) == 0 else $)')) ),
    'button_text':                  (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_BUTTON1')),
                                                                         ([16], None,                           ('Wifi',        '"WebButton{} {}".format(#,"\\"" if len($) == 0 else $)')) ),
                                    })
# ======================================================================
SETTING_8_1_0_1 = copy.deepcopy(SETTING_8_1_0_0)
SETTING_8_1_0_1['flag3'][1].update ({
        'counter_reset_on_tele':    (Platform.ALL,   '<L', (0x3A0,1,29), (None, None,                           ('SetOption',   '"SetOption79 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_8_1_0_2 = copy.deepcopy(SETTING_8_1_0_1)
SETTING_8_1_0_2.update             ({
    'hotplug_scan':                 (Platform.ALL,   'B',   0xF03,       (None, None,                           ('Sensor',      '"HotPlug {}".format($)')) ),
    'shutter_button':               (Platform.ALL,   '<L',  0xFDC,       ([4],  None,                           ('Shutter',     '"ShutterButton{} {a} {b} {c} {d} {e} {f} {g} {h} {i} {j}".format(#, a=(($>> 0)&(0x03))+1, b=((($>> 2)&(0x3f))-1)<<1, c=((($>> 8)&(0x3f))-1)<<1, d=((($>>14)&(0x3f))-1)<<1, e=((($>>20)&(0x3f))-1)<<1, f=($>>26)&(0x01), g=($>>27)&(0x01),  h=($>>28)&(0x01), i=($>>29)&(0x01), j=($>>30)&(0x01) ) if $!=0 else "ShutterButton{} {}".format(#,0)')),'"0x{:08x}".format($)' ),
                                    })
# ======================================================================
SETTING_8_1_0_3 = copy.deepcopy(SETTING_8_1_0_2)
SETTING_8_1_0_3.pop('shutter_invert',None)
SETTING_8_1_0_3.update             ({
    'shutter_options':              (Platform.ALL,   'B',   0xE78,       ([4],  None,                           ('Shutter',     ('"ShutterInvert{} {}".format(#,1 if $ & 1 else 0)',\
                                                                                                                 '"ShutterLock{} {}".format(#,1 if $ & 2 else 0)',\
                                                                                                                 '"ShutterEnableEndStopTime{} {}".format(#,1 if $ & 4 else 0)'))) ),
    'shutter_button':               (Platform.ALL, {
        '_':                        (Platform.ALL,   '<L',  0xFDC,       (None, None,                           ('Shutter',     '"ShutterButton{x} {a} {b} {c} {d} {e} {f} {g} {h} {i} {j}".format( \
                                                                                                                                x=@["shutter_button"][#-1]["shutter"], \
                                                                                                                                a=#, \
                                                                                                                                b=@["shutter_button"][#-1]["press_single"], \
                                                                                                                                c=@["shutter_button"][#-1]["press_double"], \
                                                                                                                                d=@["shutter_button"][#-1]["press_triple"], \
                                                                                                                                e=@["shutter_button"][#-1]["press_hold"], \
                                                                                                                                f=@["shutter_button"][#-1]["mqtt_broadcast_single"], \
                                                                                                                                g=@["shutter_button"][#-1]["mqtt_broadcast_double"], \
                                                                                                                                h=@["shutter_button"][#-1]["mqtt_broadcast_triple"], \
                                                                                                                                i=@["shutter_button"][#-1]["mqtt_broadcast_hold"], \
                                                                                                                                j=@["shutter_button"][#-1]["mqtt_broadcast_all"] \
                                                                                                                                )')), \
                                                                                                                                ('"0x{:08x}".format($)', False) ),
        'shutter':                  (Platform.ALL,   '<L', (0xFDC,2, 0), (None, None,                           ('Shutter',     None)), ('$+1','$-1') ),
        'press_single':             (Platform.ALL,   '<L', (0xFDC,6, 2), (None, None,                           ('Shutter',     None)), ('"-" if $==0 else ($-1)<<1','0 if $=="-" else (int(str($),0)>>1)+1') ),
        'press_double':             (Platform.ALL,   '<L', (0xFDC,6, 8), (None, None,                           ('Shutter',     None)), ('"-" if $==0 else ($-1)<<1','0 if $=="-" else (int(str($),0)>>1)+1') ),
        'press_triple':             (Platform.ALL,   '<L', (0xFDC,6,14), (None, None,                           ('Shutter',     None)), ('"-" if $==0 else ($-1)<<1','0 if $=="-" else (int(str($),0)>>1)+1') ),
        'press_hold':               (Platform.ALL,   '<L', (0xFDC,6,20), (None, None,                           ('Shutter',     None)), ('"-" if $==0 else ($-1)<<1','0 if $=="-" else (int(str($),0)>>1)+1') ),
        'mqtt_broadcast_single':    (Platform.ALL,   '<L', (0xFDC,1,26), (None, None,                           ('Shutter',     None)) ),
        'mqtt_broadcast_double':    (Platform.ALL,   '<L', (0xFDC,1,27), (None, None,                           ('Shutter',     None)) ),
        'mqtt_broadcast_triple':    (Platform.ALL,   '<L', (0xFDC,1,28), (None, None,                           ('Shutter',     None)) ),
        'mqtt_broadcast_hold':      (Platform.ALL,   '<L', (0xFDC,1,29), (None, None,                           ('Shutter',     None)) ),
        'mqtt_broadcast_all':       (Platform.ALL,   '<L', (0xFDC,1,30), (None, None,                           ('Shutter',     None)) ),
        'enabled':                  (Platform.ALL,   '<L', (0xFDC,1,31), (None, None,                           ('Shutter',     None)) ),
                                    },                      0xFDC,       ([4], None,                            ('Shutter',     None)), (None,      None) ),
    'flag4':                        (Platform.ALL, {
         'alexa_ct_range':          (Platform.ALL,   '<L', (0xEF8,1, 0), (None, None,                           ('SetOption',   '"SetOption82 {}".format($)')) ),
                                    },                      0xEF8,       (None, None,                           (VIRTUAL,       None)), (None,      None) ),
                                    })
# ======================================================================
SETTING_8_1_0_4 = copy.deepcopy(SETTING_8_1_0_3)
SETTING_8_1_0_4.update             ({
    'switchmode':                   (Platform.ALL,   'B',   0x3A4,       ([8],  '0 <= $ <= 10',                 ('Control',     '"SwitchMode{} {}".format(#,$)')) ),
    'adc_param_type':               (Platform.ALL,   'B',   0xEF7,       (None, '2 <= $ <= 7',                  ('Sensor',      '"AdcParam {type},{param1},{param2},{param3},{param4}".format(type=@["my_adc0"],param1=@["adc_param1"],param2=@["adc_param2"],param3=@["adc_param3"],param4=@["adc_param4"]) \
                                                                                                                  if 6==@["my_adc0"] \
                                                                                                                  else \
                                                                                                                  "AdcParam {type},{param1},{param2},{param3}".format(type=@["my_adc0"],param1=@["adc_param1"],param2=@["adc_param2"],param3=@["adc_param3"]/10000)')) ),
    'adc_param4':                   (Platform.ALL,   '<l',  0xFD8,       (None, None,                           ('Sensor',      None)) ),
                                    })
SETTING_8_1_0_4['flag4'][1].update ({
        'zigbee_use_names':         (Platform.ALL,   '<L', (0xEF8,1, 1), (None, None,                           ('SetOption',   '"SetOption83 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_8_1_0_5 = copy.deepcopy(SETTING_8_1_0_4)
SETTING_8_1_0_5['flag4'][1].update ({
        'awsiot_shadow':            (Platform.ALL,   '<L', (0xEF8,1, 2), (None, None,                           ('SetOption',   '"SetOption84 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_8_1_0_6 = copy.deepcopy(SETTING_8_1_0_5)
SETTING_8_1_0_6.update             ({
    'bootcount_reset_time':         (Platform.ALL,   '<L',  0xFD4,       (None, None,                           ('System',      None)) ),
                                    })
# ======================================================================
SETTING_8_1_0_9 = copy.deepcopy(SETTING_8_1_0_6)
SETTING_8_1_0_9.update             ({
    'device_group_share_in':        (Platform.ALL,   '<L',  0xFCC,       (None, None,                           ('MQTT',        '"DevGroupShare 0x{:08x},0x{:08x}".format(@["device_group_share_in"],@["device_group_share_out"])')) ),
    'device_group_share_out':       (Platform.ALL,   '<L',  0xFD0,       (None, None,                           ('MQTT',        None)) ),
    'bri_power_on':                 (Platform.ALL,   'B',   0xF04,       (None, None,                           ('Light',       None)) ),
    'bri_min':                      (Platform.ALL,   'B',   0xF05,       (None, None,                           ('Light',       '"BriMin {}".format($)')) ),
    'bri_preset_low':               (Platform.ALL,   'B',   0xF06,       (None, None,                           ('Light',       '"BriPreset {},{}".format(@["bri_preset_low"],@["bri_preset_high"])')) ),
    'bri_preset_high':              (Platform.ALL,   'B',   0xF07,       (None, None,                           ('Light',       None)) ),
    'mqtt_grptopicdev':             (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_MQTT_GRP_TOPIC2')),
                                                                         ([3],  None,                           ('MQTT',        '"GroupTopic{} {}".format(#+1,$)')) ),
                                    })
SETTING_8_1_0_9['flag4'][1].update ({
        'device_groups_enabled':    (Platform.ALL,   '<L', (0xEF8,1, 3), (None, None,                           ('SetOption',   '"SetOption85 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_8_1_0_10 = copy.deepcopy(SETTING_8_1_0_9)
SETTING_8_1_0_10['flag2'][1].update ({
        'speed_conversion':         (Platform.ALL,   '<L', (0x5BC,3, 1), (None, '0 <= $ <= 5',                  ('Sensor',      '"SpeedUnit {}".format($)')) ),
                                    })
SETTING_8_1_0_10['flag4'][1].update ({
        'led_timeout':              (Platform.ALL,   '<L', (0xEF8,1, 4), (None, None,                           ('SetOption',   '"SetOption86 {}".format($)')) ),
        'powered_off_led':          (Platform.ALL,   '<L', (0xEF8,1, 5), (None, None,                           ('SetOption',   '"SetOption87 {}".format($)')) ),
        'remote_device_mode':       (Platform.ALL,   '<L', (0xEF8,1, 6), (None, None,                           ('SetOption',   '"SetOption88 {}".format($)')) ),
        'zigbee_distinct_topics':   (Platform.ALL,   '<L', (0xEF8,1, 7), (None, None,                           ('SetOption',   '"SetOption89 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_8_1_0_11 = copy.deepcopy(SETTING_8_1_0_10)
SETTING_8_1_0_11.update             ({
    'hum_comp':                     (Platform.ALL,   'b',   0xF08,       (None, '-101 < $ < 101',               ('Sensor',      '"HumOffset {:.1f}".format(float($)/10.0)')) ),
                                    })
# ======================================================================
SETTING_8_2_0_0 = copy.deepcopy(SETTING_8_1_0_11)
SETTING_8_2_0_0.update             ({
    'switchmode':                   (Platform.ALL,   'B',   0x3A4,       ([8],  '0 <= $ <= 14',                 ('Control',     '"SwitchMode{} {}".format(#,$)')) ),
                                    })
# ======================================================================
SETTING_8_2_0_3 = copy.deepcopy(SETTING_8_2_0_0)
SETTING_8_2_0_3.pop('mqtt_grptopicdev',None)
SETTING_8_2_0_3.update             ({
    'templatename':                 (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_TEMPLATE_NAME')),
                                                                         (None, None,                           ('Management',  '"Template {{\\\"NAME\\\":\\\"{}\\\"}}".format($)')) ),
    'pulse_counter_debounce_low':   (Platform.ALL,   '<H',  0xFB8,       (None, '0 <= $ <= 32000',              ('Sensor',      '"CounterDebounceLow {}".format($)')) ),
    'pulse_counter_debounce_high':  (Platform.ALL,   '<H',  0xFBA,       (None, '0 <= $ <= 32000',              ('Sensor',      '"CounterDebounceHigh {}".format($)')) ),
    'channel':                      (Platform.ALL,   'B',   0xF09,       (None, None,                           ('Wifi',        None)) ),
    'bssid':                        (Platform.ALL,   'B',   0xF0A,       ([6],  None,                           ('Wifi',        None)) ),
    'as3935_sensor_cfg':            (Platform.ALL,   'B',   0xF10,       ([5],  None,                           ('Sensor',      None)) ),
    'as3935_functions':             (Platform.ALL, {
         'nf_autotune':             (Platform.ALL,   'B',  (0xF15,1, 0), (None, None,                           ('Sensor',      '"AS3935AutoNF {}".format($)')) ),
         'dist_autotune':           (Platform.ALL,   'B',  (0xF15,1, 1), (None, None,                           ('Sensor',      '"AS3935AutoDisturber {}".format($)')) ),
         'nf_autotune_both':        (Platform.ALL,   'B',  (0xF15,1, 2), (None, None,                           ('Sensor',      '"AS3935AutoNFMax {}".format($)')) ),
         'mqtt_only_Light_Event':   (Platform.ALL,   'B',  (0xF15,1, 3), (None, None,                           ('Sensor',      '"AS3935MQTTEvent {}".format($)')) ),
                                    },                      0xF15,       (None, None,                           (VIRTUAL,       None)), (None,      None) ),
    'as3935_parameter':             (Platform.ALL, {
         'nf_autotune_time':        (Platform.ALL,   '<H', (0xF16,4, 0), (None, '0 <= $ <= 15',                 ('Sensor',      '"AS3935NFTime {}".format($)')) ),
         'dist_autotune_time':      (Platform.ALL,   '<H', (0xF16,1, 4), (None, '0 <= $ <= 15',                 ('Sensor',      '"AS3935DistTime {}".format($)')) ),
         'nf_autotune_min':         (Platform.ALL,   '<H', (0xF16,1, 8), (None, '0 <= $ <= 15',                 ('Sensor',      '"AS3935SetMinStage {}".format($)')) ),
                                    },                      0xF16,       (None, None,                           (VIRTUAL,       None)), (None,      None) ),
    'zb_ext_panid':                 (Platform.ALL,   '<Q',  0xF18,       (None, None,                           ('Zigbee',      None)), '"0x{:016x}".format($)' ),
    'zb_precfgkey_l':               (Platform.ALL,   '<Q',  0xF20,       (None, None,                           ('Zigbee',      None)), '"0x{:016x}".format($)' ),
    'zb_precfgkey_h':               (Platform.ALL,   '<Q',  0xF28,       (None, None,                           ('Zigbee',      None)), '"0x{:016x}".format($)' ),
    'zb_pan_id':                    (Platform.ALL,   '<H',  0xF30,       (None, None,                           ('Zigbee',      None)), '"0x{:016x}".format($)' ),
    'zb_channel':                   (Platform.ALL,   'B',   0xF32,       (None, '11 <= $ <= 26',                ('Zigbee',      '"ZbConfig {{\\\"Channel\\\":{},\\\"PanID\\\":\\\"0x{:04X}\\\",\\\"ExtPanID\\\":\\\"0x{:016X}\\\",\\\"KeyL\\\":\\\"0x{:016X}\\\",\\\"KeyH\\\":\\\"0x{:016X}\\\"}}".format(@["zb_channel"], int(@["zb_pan_id"],0), int(@["zb_ext_panid"],0), int(@["zb_precfgkey_l"],0), int(@["zb_precfgkey_h"],0))')) ),
    'pms_wake_interval':            (Platform.ALL,   '<H',  0xF34,       (None, None,                           ('Sensor',      '"Sensor18 {}".format($)')) ),
    'device_group_share_in':        (Platform.ALL,   '<L',  0xFCC,       (None, None,                           ('Control',     '"DevGroupShare 0x{:08x},0x{:08x}".format(@["device_group_share_in"],@["device_group_share_out"])')) ),
    'device_group_share_out':       (Platform.ALL,   '<L',  0xFD0,       (None, None,                           ('Control',      None)) ),
    'device_group_topic':           (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_DEV_GROUP_NAME1')),
                                                                         ([4],  None,                           ('Control',     '"DevGroupName{} {}".format(#,$ if len($) else "\\"")')) ),
    'mqtt_grptopic':                (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_MQTT_GRP_TOPIC')),
                                                                         (None, None,                           ('MQTT',        '"GroupTopic1 {}".format("\\"" if len($) == 0 else $)')) ),
    'mqtt_grptopic2':               (Platform.ALL,   '699s',(0x017,SETTINGSTEXTINDEX.index('SET_MQTT_GRP_TOPIC2')),
                                                                         ([3],  None,                           ('MQTT',        '"GroupTopic{} {}".format(#+1, "\\"" if len($) == 0 else $)')) ),
    'my_gp':                        (Platform.ESP82, 'B',   0x484,       ([17], None,                           ('Management',  '"Gpio{} {}".format(#-1,$)')) ),
    'my_gp_esp32':                  (Platform.ESP32, 'B',   0x558,       ([40], None,                           ('Management',  '"Gpio{} {}".format(#-1,$)')) ),
    'user_template_esp32':          (Platform.ESP32,{
        'base':                     (Platform.ESP32, 'B',   0x71F,       (None, None,                           ('Management',  '"Template {{\\\"BASE\\\":{}}}".format($)')), ('$+1','$-1') ),
        'name':                     (Platform.ESP32, '15s', 0x720,       (None, None,                           ('Management',  '"Template {{\\\"NAME\\\":\\\"{}\\\"}}".format($)' )) ),
        'gpio':                     (Platform.ESP32, 'B',   0x580,       ([36], None,                           ('Management',  '"Template {{\\\"GPIO\\\":{}}}".format(@["user_template_esp32"]["gpio"]) if 1==# else None')) ),
        'flag':                     (Platform.ESP32,{
            'adc0':                 (Platform.ESP32, 'B',  (0x5A4,4,0),  (None, None,                           ('Management',  '"Template {{\\\"FLAG\\\":{}}}".format($)')) ),
                                    },                      0x5A4,       (None, None,                           ('Management',  None))
                                    ),
                                    },                      0x71F,       (None, None,                           ('Management',  None))
                                    ),
                                    })
SETTING_8_2_0_3['user_template'][1].update ({
        'base':                     (Platform.ESP82, 'B',   0x71F,       (None, None,                           ('Management',  '"Template {{\\\"BASE\\\":{}}}".format($)')), ('$+1','$-1') ),
        'name':                     (Platform.ESP82, '15s', 0x720,       (None, None,                           ('Management',  '"Template {{\\\"NAME\\\":\\\"{}\\\"}}".format($)' )) ),
        'gpio':                     (Platform.ESP82, 'B',   0x72F,       ([13], None,                           ('Management',  '"Template {{\\\"GPIO\\\":{}}}".format(@["user_template"]["gpio"]) if 1==# else None')) ),
        'flag':                     (Platform.ESP82, {
            'adc0':                 (Platform.ESP82, 'B',  (0x73C,4,0),  (None, None,                           ('Management',  '"Template {{\\\"FLAG\\\":{}}}".format($)')) ),
                                    },                      0x73C,       (None, None,                           ('Management',  None))
                                    ),
                                    })
SETTING_8_2_0_3['flag3'][1].update ({
        'mqtt_buttons':             (Platform.ALL,   '<L', (0x3A0,1,23), (None, None,                           ('SetOption',   '"SetOption73 {}".format($)')) ),
                                    })
SETTING_8_2_0_3['flag4'][1].update ({
        'only_json_message':        (Platform.ALL,   '<L', (0xEF8,1, 8), (None, None,                           ('SetOption',   '"SetOption90 {}".format($)')) ),
        'fade_at_startup':          (Platform.ALL,   '<L', (0xEF8,1, 9), (None, None,                           ('SetOption',   '"SetOption91 {}".format($)')) ),
                                    })
SETTING_8_2_0_3['SensorBits1'][1].update ({
        'bh1750_resolution':        (Platform.ALL,   'B',  (0x717,2, 4), (None, '0 <= $ <= 2',                  ('Sensor',      '"Sensor10 {}".format($)')) ),
                                    })
# ======================================================================
SETTING_8_2_0_4 = copy.deepcopy(SETTING_8_2_0_3)
SETTING_8_2_0_4.update             ({
    'config_version':               (Platform.ALL,   'B',   0xF36,       (None, None,                           (INTERNAL,      None)), (None,      False) ),
                                    })
# ======================================================================
SETTINGS = [
            (0x8020004,0x1000, SETTING_8_2_0_4),
            (0x8020003,0x1000, SETTING_8_2_0_3),
            (0x8020000,0x1000, SETTING_8_2_0_0),
            (0x801000B,0x1000, SETTING_8_1_0_11),
            (0x801000A,0x1000, SETTING_8_1_0_10),
            (0x8010009,0x1000, SETTING_8_1_0_9),
            (0x8010006,0x1000, SETTING_8_1_0_6),
            (0x8010005,0x1000, SETTING_8_1_0_5),
            (0x8010004,0x1000, SETTING_8_1_0_4),
            (0x8010003,0x1000, SETTING_8_1_0_3),
            (0x8010002,0x1000, SETTING_8_1_0_2),
            (0x8010001,0x1000, SETTING_8_1_0_1),
            (0x8010000,0x1000, SETTING_8_1_0_0),
            (0x8000001,0x1000, SETTING_8_0_0_1),
            (0x7010206,0x1000, SETTING_7_1_2_6),
            (0x7010205,0x1000, SETTING_7_1_2_5),
            (0x7010203,0x1000, SETTING_7_1_2_3),
            (0x7010202,0x1000, SETTING_7_1_2_2),
            (0x7000006,0x1000, SETTING_7_0_0_6),
            (0x7000005,0x1000, SETTING_7_0_0_5),
            (0x7000004,0x1000, SETTING_7_0_0_4),
            (0x7000003,0x1000, SETTING_7_0_0_3),
            (0x7000002,0x1000, SETTING_7_0_0_2),
            (0x7000001,0x1000, SETTING_7_0_0_1),
            (0x6060015,0x1000, SETTING_6_6_0_21),
            (0x6060014,0x1000, SETTING_6_6_0_20),
            (0x6060012,0x1000, SETTING_6_6_0_18),
            (0x606000F,0x1000, SETTING_6_6_0_15),
            (0x606000E,0x1000, SETTING_6_6_0_14),
            (0x606000D,0x1000, SETTING_6_6_0_13),
            (0x606000C,0x1000, SETTING_6_6_0_12),
            (0x606000B,0x1000, SETTING_6_6_0_11),
            (0x606000A,0x1000, SETTING_6_6_0_10),
            (0x6060009,0x1000, SETTING_6_6_0_9),
            (0x6060008,0x1000, SETTING_6_6_0_8),
            (0x6060007,0x1000, SETTING_6_6_0_7),
            (0x6060006, 0xe00, SETTING_6_6_0_6),
            (0x6060005, 0xe00, SETTING_6_6_0_5),
            (0x6060003, 0xe00, SETTING_6_6_0_3),
            (0x6060002, 0xe00, SETTING_6_6_0_2),
            (0x6060001, 0xe00, SETTING_6_6_0_1),
            (0x605000F, 0xe00, SETTING_6_5_0_15),
            (0x605000C, 0xe00, SETTING_6_5_0_12),
            (0x605000B, 0xe00, SETTING_6_5_0_11),
            (0x605000A, 0xe00, SETTING_6_5_0_10),
            (0x6050009, 0xe00, SETTING_6_5_0_9),
            (0x6050007, 0xe00, SETTING_6_5_0_7),
            (0x6050006, 0xe00, SETTING_6_5_0_6),
            (0x6050003, 0xe00, SETTING_6_5_0_3),
            (0x6040112, 0xe00, SETTING_6_4_1_18),
            (0x6040111, 0xe00, SETTING_6_4_1_17),
            (0x6040110, 0xe00, SETTING_6_4_1_16),
            (0x604010D, 0xe00, SETTING_6_4_1_13),
            (0x604010B, 0xe00, SETTING_6_4_1_11),
            (0x6040108, 0xe00, SETTING_6_4_1_8),
            (0x6040107, 0xe00, SETTING_6_4_1_7),
            (0x6040104, 0xe00, SETTING_6_4_1_4),
            (0x6040002, 0xe00, SETTING_6_4_0_2),
            (0x6030010, 0xe00, SETTING_6_3_0_16),
            (0x603000F, 0xe00, SETTING_6_3_0_15),
            (0x603000E, 0xe00, SETTING_6_3_0_14),
            (0x603000D, 0xe00, SETTING_6_3_0_13),
            (0x603000B, 0xe00, SETTING_6_3_0_11),
            (0x603000A, 0xe00, SETTING_6_3_0_10),
            (0x6030008, 0xe00, SETTING_6_3_0_8),
            (0x6030004, 0xe00, SETTING_6_3_0_4),
            (0x6030002, 0xe00, SETTING_6_3_0_2),
            (0x6030000, 0xe00, SETTING_6_3_0),
            (0x6020114, 0xe00, SETTING_6_2_1_20),
            (0x6020113, 0xe00, SETTING_6_2_1_19),
            (0x602010E, 0xe00, SETTING_6_2_1_14),
            (0x602010A, 0xe00, SETTING_6_2_1_10),
            (0x6020106, 0xe00, SETTING_6_2_1_6),
            (0x6020103, 0xe00, SETTING_6_2_1_3),
            (0x6020102, 0xe00, SETTING_6_2_1_2),
            (0x6020100, 0xe00, SETTING_6_2_1),
            (0x6010100, 0xe00, SETTING_6_1_1),
            (0x6000000, 0xe00, SETTING_6_0_0),
            (0x50e0000, 0xa00, SETTING_5_14_0),
            (0x50d0100, 0xa00, SETTING_5_13_1),
            (0x50c0000, 0x670, SETTING_5_12_0),
            (0x50b0000, 0x670, SETTING_5_11_0),
            (0x50a0000, 0x670, SETTING_5_10_0),
           ]
# pylint: enable=bad-continuation,bad-whitespace,invalid-name

def check_setting_definition():
    """
    Check complete setting definition history

    @return: True if ok
    """
    for cfg in SETTINGS:
        setting = cfg[2]
        for key in setting:
            fielddef = setting[key]
            get_fielddef(fielddef)

    return True

# ======================================================================
# Common helper
# ======================================================================
class LogType:
    """
    Logging types
    """
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'

def message(msg, type_=None, status=None, line=None):
    """
    Writes a message to stdout

    @param msg:
        message to output
    @param type_:
        INFO, WARNING or ERROR
    @param status:
        status number
    """
    sdelimiter = ' ' if status is not None and type_ is not None and status > 0 else ''
    print('{styp}{sdelimiter}{sstatus}{sdelimiter}{slineno}{scolon}{smgs}'\
          .format(styp=type_ if type_ is not None else '',
                  sdelimiter=sdelimiter,
                  sstatus=status if status is not None and status > 0 else '',
                  scolon=': ' if type_ is not None or line is not None else '',
                  smgs=msg,
                  slineno='(@{:04d})'.format(line) if line is not None else ''),
          file=sys.stderr)

def exit_(status=0, msg="end", type_=LogType.ERROR, src=None, doexit=True, line=None):
    """
    Called when the program should be exit

    @param status:
        the exit status program returns to callert
    @param msg:
        the msg logged before exit
    @param type_:
        msg type: 'INFO', 'WARNING' or 'ERROR'
    @param doexit:
        True to exit program, otherwise return
    """
    global EXIT_CODE    # pylint: disable=global-statement

    if src is not None:
        msg = '{} ({})'.format(src, msg)
    message(msg, type_=type_ if status != ExitCode.OK else LogType.INFO, status=status, line=line)
    EXIT_CODE = status
    if doexit:
        message("Premature exit - {} #{}".format(ExitCode.str(status), status), type_=None, status=None, line=None)
        sys.exit(EXIT_CODE)

def debug(_args):
    """
    Get debug level

    @param _args:
        configargparse.parse_args() result

    @return:
        debug level
    """
    return 0 if _args.debug is None else _args.debug


def shorthelp(doexit=True):
    """
    Show short help (usage) only - ued by own -h handling

    @param doexit:
        sys.exit with OK if True
    """
    print(PARSER.description)
    print()
    PARSER.print_usage()
    print()
    print("For advanced help use '{prog} -H' or '{prog} --full-help'".format(prog=os.path.basename(sys.argv[0])))
    if doexit:
        sys.exit(ExitCode.OK)

# ======================================================================
# Tasmota config data handling
# ======================================================================
def get_jsonstr(configmapping, jsonsort, jsonindent, jsoncompact):
    """
    Get JSON string output from config mapping

    @param configmapping:
        binary config data (decrypted)
    @param jsonsort:
        True: output of dictionaries will be sorted by key
        Uppercase and lowercase main keys remain unaffected
    @param jsonindent:
        pretty-printed JSON output indent level (<0 disables indent)
    @param jsoncompact:
        True: output of dictionaries will be compacted (no space after , and :)

    @return:
        template sizes as list []
    """
    conv_keys = {}
    for key in configmapping:
        if key[0].isupper():
            conv_keys[key] = key.lower()
            configmapping[conv_keys[key]] = configmapping.pop(key)
    json_output = json.dumps(
        configmapping,
        ensure_ascii=False,
        sort_keys=jsonsort,
        indent=None if (jsonindent is None or ARGS.jsonindent < 0) else jsonindent,
        separators=(',', ':') if jsoncompact else (', ', ': ')
        )
    for str_ in conv_keys:
        json_output = json_output.replace('"'+conv_keys[str_]+'"', '"'+str_+'"')

    return json_output

def get_templatesizes():
    """
    Get all possible template sizes as list

    @return:
        template sizes as list []
    """
    sizes = []
    for cfg in SETTINGS:
        sizes.append(cfg[1])
    # return unique sizes only (remove duplicates)
    return list(set(sizes))

def get_config_info(decode_cfg):
    """
    Extract info about loaded config

    @param decode_cfg:
        binary config data (decrypted)

    @return: dict
        platform         int  config data hardware platform
        version          int  config data version
        template_version int  template version number
        template_size    int  config data size
        template         dict template dict (from SETTINGS)
    """
    version = 0x0
    size = setting = None
    version = get_field(decode_cfg, Platform.ALL, 'version', SETTING_6_2_1['version'], raw=True, ignoregroup=True)
    template_version = version

    # identify platform (config_version)
    config_version = PLATFORMS.index("ESP82xx")  # default legacy
    for cfg in sorted(SETTINGS, key=lambda s: s[0], reverse=True):
        if version >= cfg[0]:
            fielddef = cfg[2].get('config_version', None)
            if fielddef is not None:
                config_version = get_field(decode_cfg, Platform.ALL, 'config_version', fielddef, raw=True, ignoregroup=True)
                if config_version >= len(PLATFORMS):
                    exit_(ExitCode.INVALID_DATA, "Invalid data in config (config_version is {}, valid range [0,{}])".format(config_version, len(PLATFORMS)-1), type_=LogType.WARNING, line=inspect.getlineno(inspect.currentframe()))
                    config_version = PLATFORMS.index("ESP82xx")
            break
    # search setting definition for platform top-down
    for cfg in sorted(SETTINGS, key=lambda s: s[0], reverse=True):
        if version >= cfg[0]:
            template_version = cfg[0]
            size = cfg[1]
            setting = cfg[2]
            break

    if setting is None:
        exit_(ExitCode.UNSUPPORTED_VERSION, "Tasmota configuration version {} not supported".format(version), line=inspect.getlineno(inspect.currentframe()))

    return {
        'platform': config_version,
        'version': version,
        'template_version': template_version,
        'template_size': size,
        'template': setting
        }

def get_grouplist(setting):
    """
    Get all avilable group definition from setting

    @return:
        configargparse.parse_args() result
    """
    groups = set()

    for name in setting:
        dev = setting[name]
        format_, group = get_fielddef(dev, fields="format_, group")
        if group is not None and len(group) > 0:
            groups.add(group.title())
        if isinstance(format_, dict):
            subgroups = get_grouplist(format_)
            if subgroups is not None and len(subgroups) > 0:
                for group in subgroups:
                    groups.add(group.title())

    groups = list(groups)
    groups.sort()
    return groups

class FileType:
    """
    File type returns
    """
    FILE_NOT_FOUND = None
    DMP = 'dmp'
    JSON = 'json'
    BIN = 'bin'
    UNKNOWN = 'unknown'
    INCOMPLETE_JSON = 'incomplete json'
    INVALID_JSON = 'invalid json'
    INVALID_BIN = 'invalid bin'

def get_filetype(filename):
    """
    Get the FileType class member of a given filename

    @param filename:
        filename of the file to analyse

    @return:
        FileType class member
    """
    filetype = FileType.UNKNOWN

    # try filename
    try:
        with open(filename, "r") as file:
            try:
                # try reading as json
                json.load(file)
                filetype = FileType.JSON
            except ValueError:
                filetype = FileType.INVALID_JSON
                # not a valid json, get filesize and compare it with all possible sizes
                try:
                    size = os.path.getsize(filename)
                except:     # pylint: disable=bare-except
                    filetype = FileType.UNKNOWN

                header_format = '<L'
                sizes = get_templatesizes()
                # size is one of a dmp file size
                if size in sizes:
                    filetype = FileType.DMP
                elif size - struct.calcsize(header_format) in sizes:
                    # check if the binary file has the magic header
                    with open(filename, "rb") as inputfile:
                        inputbin = inputfile.read()
                    if struct.unpack_from(header_format, inputbin, 0)[0] == BINARYFILE_MAGIC or \
                       struct.unpack_from(header_format, inputbin, len(inputbin)-struct.calcsize(header_format))[0] == BINARYFILE_MAGIC:
                        filetype = FileType.BIN
                    else:
                        filetype = FileType.INVALID_BIN

    except:     # pylint: disable=bare-except
        filetype = FileType.FILE_NOT_FOUND

    return filetype

def get_platformstr(version):
    """
    Create platform string

    @param version:
        version integer

    @return:
        platform string
    """
    return PLATFORMS[version] if version is not None and version >= 0 and version < len(PLATFORMS) else PLATFORMS[0]

def get_versionstr(version):
    """
    Create human readable version string

    @param version:
        version integer

    @return:
        version string
    """
    if isinstance(version, str):
        version = int(version, 0)
    major = ((version>>24) & 0xff)
    minor = ((version>>16) & 0xff)
    release = ((version>> 8) & 0xff)
    subrelease = (version & 0xff)
    if major >= 6:
        if subrelease > 0:
            subreleasestr = str(subrelease)
        else:
            subreleasestr = ''
    else:
        if subrelease > 0:
            subreleasestr = str(chr(subrelease+ord('a')-1))
        else:
            subreleasestr = ''
    return "{:d}.{:d}.{:d}{}{}".format(major, minor, release, '.' if (major >= 6 and subreleasestr != '') else '', subreleasestr)

def make_filename(filename, filetype, configmapping):
    """
    Replace variables within a filename

    @param filename:
        original filename possible containing replacements:
        @v:
            Tasmota version from config data
        @f:
            friendlyname from config data
        @h:
            hostname from config data
        @H:
            hostname from device (-d arg only)
    @param filetype:
        FileType.x object - creates extension if not None
    @param configmapping:
        binary config data (decrypted)

    @return:
        New filename with replacements
    """
    config_version = config_friendlyname = config_hostname = device_hostname = ''

    config_version = configmapping.get('version', None)
    if config_version is not None:
        config_version = get_versionstr(int(str(config_version), 0))
    config_friendlyname = configmapping.get('friendlyname', None)
    if config_friendlyname is not None:
        config_friendlyname = re.sub('_{2,}', '_', "".join(itertools.islice((c for c in str(config_friendlyname[0]) if c.isprintable()), 256))).replace(' ', '_')
    config_hostname = configmapping.get('hostname', None)
    if config_hostname is not None:
        if str(config_hostname).find('%') < 0:
            config_hostname = re.sub('_{2,}', '_', re.sub('[^0-9a-zA-Z]', '_', str(config_hostname)).strip('_'))
    if filename.find('@H') >= 0 and ARGS.device is not None:
        device_hostname = get_tasmotahostname(ARGS.device, ARGS.port, username=ARGS.username, password=ARGS.password)
        if device_hostname is None:
            device_hostname = ''

    dirname = basename = ext = ''

    # split file parts
    dirname = os.path.normpath(os.path.dirname(filename))
    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)

    # make a valid filename
    try:
        name = name.translate(dict((ord(char), None) for char in r'\/*?:"<>|'))
    except:     # pylint: disable=bare-except
        pass
    name = name.replace(' ', '_')

    # append extension based on filetype if not given
    if len(ext) != 0 and ext[0] == '.':
        ext = ext[1:]
    if filetype is not None and ARGS.extension and (len(ext) < 2 or all(c.isdigit() for c in ext)):
        ext = filetype.lower()

    # join filename + extension
    if len(ext) != 0:
        name_ext = name+'.'+ext
    else:
        name_ext = name

    # join path and filename
    try:
        filename = os.path.join(dirname, name_ext)
    except:     # pylint: disable=bare-except
        pass

    filename = filename.replace('@v', config_version)
    filename = filename.replace('@f', config_friendlyname)
    filename = filename.replace('@h', config_hostname)
    filename = filename.replace('@H', device_hostname)

    return filename

def make_url(host, port=80, location=''):
    """
    Create a Tasmota host url

    @param host:
        hostname or IP of Tasmota host
    @param port:
        port number to use for http connection
    @param location:
        http url location

    @return:
        Tasmota http url
    """
    return "http://{shost}{sdelimiter}{sport}/{slocation}".format(\
            shost=host,
            sdelimiter=':' if port != 80 else '',
            sport=port if port != 80 else '',
            slocation=location)

def load_tasmotaconfig(filename):
    """
    Load config from Tasmota file

    @param filename:
        filename to load

    @return:
        binary config data (encrypted) or None on error
    """
    encode_cfg = None

    # read config from a file
    if not os.path.isfile(filename):    # check file exists
        exit_(ExitCode.FILE_NOT_FOUND, "File '{}' not found".format(filename), line=inspect.getlineno(inspect.currentframe()))

    if ARGS.verbose or ((ARGS.backupfile is not None or ARGS.restorefile is not None) and not ARGS.output):
        message("Load data from file '{}'".format(ARGS.tasmotafile), type_=LogType.INFO if ARGS.verbose else None)
    try:
        with open(filename, "rb") as tasmotafile:
            encode_cfg = tasmotafile.read()
    except Exception as err:    # pylint: disable=broad-except
        exit_(ExitCode.INTERNAL_ERROR, "'{}' {}".format(filename, err), line=inspect.getlineno(inspect.currentframe()))

    return encode_cfg

def get_tasmotaconfig(cmnd, host, port, username=DEFAULTS['source']['username'], password=None, contenttype=None):
    """
    Tasmota http request

    @param host:
        hostname or IP of Tasmota device
    @param port:
        http port of Tasmota device
    @param username:
        optional username for Tasmota web login
    @param password
        optional password for Tasmota web login

    @return:
        binary config data (encrypted) or None on error
    """
    # read config direct from device via http
    url = make_url(host, port, cmnd)
    auth = None
    if username is not None and password is not None:
        auth = (username, password)
    try:
        res = requests.get(url, auth=auth)
    except requests.exceptions.ConnectionError as _:
        exit_(ExitCode.HTTP_CONNECTION_ERROR, "Failed to establish HTTP connection")

    if not res.ok:
        exit_(res.status_code, "Error on http GET request for {} - {}".format(url, res.reason), line=inspect.getlineno(inspect.currentframe()))

    if contenttype is not None and res.headers['Content-Type'] != contenttype:
        exit_(ExitCode.DOWNLOAD_CONFIG_ERROR, "Device did not respond properly, maybe Tasmota webserver admin mode is disabled (WebServer 2)", line=inspect.getlineno(inspect.currentframe()))

    return res.status_code, res.content

def get_tasmotahostname(host, port, username=DEFAULTS['source']['username'], password=None):
    """
    Get Tasmota hostname from device

    @param host:
        hostname or IP of Tasmota device
    @param port:
        http port of Tasmota device
    @param username:
        optional username for Tasmota web login
    @param password
        optional password for Tasmota web login

    @return:
        Tasmota real hostname or None on error
    """
    hostname = None

    loginstr = ""
    if password is not None:
        loginstr = "user={}&password={}&".format(urllib.parse.quote(username), urllib.parse.quote(password))
    # get hostname
    _, body = get_tasmotaconfig("cm?{}cmnd=status%205".format(loginstr), host, port, username=username, password=password)
    if body is not None:
        jsonbody = json.loads(str(body, STR_ENCODING))
        statusnet = jsonbody.get('StatusNET', None)
        if statusnet is not None:
            hostname = statusnet.get('Hostname', None)
            if hostname is not None:
                if ARGS.verbose:
                    message("Hostname for '{}' retrieved: '{}'".format(host, hostname), type_=LogType.INFO)

    return hostname

def pull_tasmotaconfig(host, port, username=DEFAULTS['source']['username'], password=None):
    """
    Pull config from Tasmota device

    @param host:
        hostname or IP of Tasmota device
    @param port:
        http port of Tasmota device
    @param username:
        optional username for Tasmota web login
    @param password
        optional password for Tasmota web login

    @return:
        binary config data (encrypted) or None on error
    """
    if ARGS.verbose or ((ARGS.backupfile is not None or ARGS.restorefile is not None) and not ARGS.output):
        message("Load data from device '{}'".format(ARGS.device), type_=LogType.INFO if ARGS.verbose else None)

    _, body = get_tasmotaconfig('dl', host, port, username, password, contenttype='application/octet-stream')

    return body

def push_tasmotaconfig(encode_cfg, host, port, username=DEFAULTS['source']['username'], password=None, verbosemsg=""):
    """
    Upload binary data to a Tasmota host using http

    @param encode_cfg:
        encrypted binary data or filename containing Tasmota encrypted binary config
    @param host:
        hostname or IP of Tasmota device
    @param port:
        http port of Tasmota device
    @param username:
        optional username for Tasmota web login
    @param password
        optional password for Tasmota web login
    @param verbosemsg
        optional verbosemsg text

    @return
        errorcode, errorstring
        errorcode=0 if success, otherwise http response or exception code
    """
    if ARGS.verbose:
        message(verbosemsg, type_=LogType.INFO)

    if isinstance(encode_cfg, str):
        encode_cfg = bytearray(encode_cfg)

    # get restore config page first to set internal Tasmota vars
    responsecode, body = get_tasmotaconfig('rs?', host, port, username, password, contenttype='text/html')
    if body is None:
        return responsecode, "ERROR"

    # ~ # post data
    url = make_url(host, port, "u2")
    auth = None
    if username is not None and password is not None:
        auth = (username, password)
    files = {'u2':('{sprog}_v{sver}.dmp'.format(sprog=os.path.basename(sys.argv[0]), sver=VER), encode_cfg)}
    try:
        res = requests.post(url, auth=auth, files=files)
    except ConnectionError as err:
        exit_(ExitCode.UPLOAD_CONFIG_ERROR, "Error on http POST request for {} - {}".format(url, err), line=inspect.getlineno(inspect.currentframe()))

    if not res.ok:
        exit_(res.status_code, "Error on http POST request for {} - {}".format(url, res.reason), line=inspect.getlineno(inspect.currentframe()))

    if res.headers['Content-Type'] != 'text/html':
        exit_(ExitCode.UPLOAD_CONFIG_ERROR, "Device did not response properly, may be Tasmota webserver admin mode is disabled (WebServer 2)", line=inspect.getlineno(inspect.currentframe()))

    body = res.text

    find_upload = body.find("Upload")
    if find_upload < 0:
        return ExitCode.UPLOAD_CONFIG_ERROR, "Device did not response properly with upload result page"

    body = body[find_upload:]
    if body.find("Successful") < 0:
        errmatch = re.search(r"<font\s*color='[#0-9a-fA-F]+'>(\S*)</font></b><br><br>(.*)<br>", body)
        reason = "Unknown error"
        if errmatch and len(errmatch.groups()) > 1:
            reason = errmatch.group(2)
        return ExitCode.UPLOAD_CONFIG_ERROR, reason

    return 0, 'OK'

def decrypt_encrypt(obj):
    """
    Decrpt/Encrypt binary config data

    @param obj:
        binary config data

    @return:
        decrypted configuration (if obj contains encrypted data)
    """
    if isinstance(obj, str):
        obj = bytearray(obj)
    dobj = bytearray(obj[0:2])
    for i in range(2, len(obj)):
        dobj.append((obj[i] ^ (CONFIG_FILE_XOR +i)) & 0xff)
    return dobj

def get_settingcrc(dobj):
    """
    Return binary config data calclulated crc

    @param dobj:
        decrypted binary config data

    @return:
        2 byte unsigned integer crc value
    """
    if isinstance(dobj, str):
        dobj = bytearray(dobj)

    crc = 0
    config_info = get_config_info(dobj)
    for i in range(0, config_info['template_size']):
        if not i in [14, 15]: # Skip crc
            byte_ = dobj[i]
            crc += byte_ * (i+1)

    return crc & 0xffff

def get_settingcrc32(dobj):
    """
    Return binary config data calclulated crc32

    @param dobj:
        decrypted binary config data

    @return:
        4 byte unsigned integer crc value
    """
    if isinstance(dobj, str):
        dobj = bytearray(dobj)
    crc = 0
    for i in range(0, len(dobj)-4):
        crc ^= dobj[i]
        for _ in range(0, 8):
            crc = (crc >> 1) ^ (-int(crc & 1) & 0xEDB88320)

    return ~crc & 0xffffffff

def get_fielddef(fielddef, fields="platform_, format_, addrdef, baseaddr, bits, bitshift, strindex, datadef, arraydef, validate, cmd, group, tasmotacmnd, converter, readconverter, writeconverter"):
    """
    Get field definition items

    @param fielddef:
        field format - see "Settings dictionary" above
    @param fields:
        comma separated string list of values to be returned
        possible values see fields default

    @return:
        set of values defined in <fields>
    """
    platform_ = format_ = addrdef = baseaddr = datadef = arraydef = validate = cmd = group = tasmotacmnd = converter = readconverter = writeconverter = strindex = None
    bits = bitshift = 0
    raise_error = '<fielddef> error'

    # calling with None is wrong
    if fielddef is None:
        print('<fielddef> is None', file=sys.stderr)
        raise SyntaxError(raise_error)

    # check global format
    if not isinstance(fielddef, (dict, tuple)):
        print('wrong <fielddef> in setting {}'.format(fielddef), file=sys.stderr)
        raise SyntaxError(raise_error)

    # get top level items
    if len(fielddef) == 4:
        # converter not present
        platform_, format_, addrdef, datadef = fielddef
    elif len(fielddef) == 5:
        # converter present
        platform_, format_, addrdef, datadef, converter = fielddef
    else:
        print('wrong <fielddef> {} length ({}) in setting'.format(fielddef, len(fielddef)), file=sys.stderr)
        raise SyntaxError(raise_error)

    # ignore calls with 'root' setting
    if isinstance(format_, dict) and baseaddr is None and datadef is None:
        return eval(fields)     # pylint: disable=eval-used

    if not isinstance(platform_, int):
        print("baseaddr: {} datadef: {}".format(baseaddr, datadef))
        print('<platform> ({}) must be defined as integer in <fielddef> {}'.format(type(platform_), fielddef), file=sys.stderr)
        raise SyntaxError(raise_error)

    if not isinstance(format_, (str, dict)):
        print('wrong <format> {} type {} in <fielddef> {}'.format(format_, type(format_), fielddef), file=sys.stderr)
        raise SyntaxError(raise_error)

    # extract addrdef items
    baseaddr = addrdef
    if isinstance(baseaddr, (list, tuple)):
        if len(baseaddr) == 3:
            # baseaddr bit definition
            baseaddr, bits, bitshift = baseaddr
            if not isinstance(bits, int):
                print('<bits> must be defined as integer in <fielddef> {}'.format(fielddef), file=sys.stderr)
                raise SyntaxError(raise_error)
            if not isinstance(bitshift, int):
                print('<bitshift> must be defined as integer in <fielddef> {}'.format(fielddef), file=sys.stderr)
                raise SyntaxError(raise_error)
        elif len(baseaddr) == 2:
            # baseaddr string definition
            baseaddr, strindex = baseaddr
            if not isinstance(strindex, int):
                print('<strindex> must be defined as integer in <fielddef> {}'.format(fielddef), file=sys.stderr)
                raise SyntaxError(raise_error)
            if strindex >= SETTINGSTEXTINDEX.index('SET_MAX'):
                print('<strindex> out of range [0, {}] in <fielddef> {}'.format(SETTINGSTEXTINDEX.index('SET_MAX'), fielddef), file=sys.stderr)
                raise SyntaxError(raise_error)
        else:
            print('wrong <addrdef> {} length ({}) in <fielddef> {}'.format(addrdef, len(addrdef), fielddef), file=sys.stderr)
            raise SyntaxError(raise_error)
    if not isinstance(baseaddr, int):
        print('<baseaddr> {} must be defined as integer in <fielddef> {}'.format(baseaddr, fielddef), file=sys.stderr)
        raise SyntaxError(raise_error)

    # extract datadef items
    arraydef = datadef
    if isinstance(datadef, (tuple)):
        if len(datadef) == 2:
            # datadef has a validator
            arraydef, validate = datadef
        elif len(datadef) == 3:
            # datadef has a validator and cmd set
            arraydef, validate, cmd = datadef
            # cmd must be a tuple with 2 objects
            if isinstance(cmd, tuple) and len(cmd) == 2:
                group, tasmotacmnd = cmd
                if group is not None and not isinstance(group, str):
                    print('wrong <group> {} in <fielddef> {}'.format(group, fielddef), file=sys.stderr)
                    raise SyntaxError(raise_error)
                if isinstance(tasmotacmnd, tuple):
                    for tcmnd in tasmotacmnd:
                        if tcmnd is not None and not callable(tcmnd) and not isinstance(tcmnd, str):
                            print('wrong <tasmotacmnd> {} in <fielddef> {}'.format(tcmnd, fielddef), file=sys.stderr)
                            raise SyntaxError(raise_error)
                else:
                    if tasmotacmnd is not None and not callable(tasmotacmnd) and not isinstance(tasmotacmnd, str):
                        print('wrong <tasmotacmnd> {} in <fielddef> {}'.format(tasmotacmnd, fielddef), file=sys.stderr)
                        raise SyntaxError(raise_error)
            else:
                print('wrong <cmd> {} length ({}) in <fielddef> {}'.format(cmd, len(cmd), fielddef), file=sys.stderr)
                raise SyntaxError(raise_error)
        else:
            print('wrong <datadef> {} length ({}) in <fielddef> {}'.format(datadef, len(datadef), fielddef), file=sys.stderr)
            raise SyntaxError(raise_error)

        if validate is not None and (not isinstance(validate, str) and not callable(validate)):
            print('wrong <validate> {} type {} in <fielddef> {}'.format(validate, type(validate), fielddef), file=sys.stderr)
            raise SyntaxError(raise_error)

    # convert single int into one-dimensional list
    if isinstance(arraydef, int):
        arraydef = [arraydef]

    if arraydef is not None and not isinstance(arraydef, (list)):
        print('wrong <arraydef> {} type {} in <fielddef> {}'.format(arraydef, type(arraydef), fielddef), file=sys.stderr)
        raise SyntaxError(raise_error)

    # get read/write converter items
    readconverter = converter
    if isinstance(converter, (tuple)):
        if len(converter) == 2:
            # converter has read/write converter
            readconverter, writeconverter = converter
            if readconverter is not None  and not isinstance(readconverter, str) and not callable(readconverter):
                print('wrong <readconverter> {} type {} in <fielddef> {}'.format(readconverter, type(readconverter), fielddef), file=sys.stderr)
                raise SyntaxError(raise_error)
            if writeconverter is not None and (not isinstance(writeconverter, (bool, str)) and not callable(writeconverter)):
                print('wrong <writeconverter> {} type {} in <fielddef> {}'.format(writeconverter, type(writeconverter), fielddef), file=sys.stderr)
                raise SyntaxError(raise_error)
        else:
            print('wrong <converter> {} length ({}) in <fielddef> {}'.format(converter, len(converter), fielddef), file=sys.stderr)
            raise SyntaxError(raise_error)

    return eval(fields)     # pylint: disable=eval-used

def readwrite_converter(value, fielddef, read=True, raw=False):
    """
    Convert field value based on field desc

    @param value:
        original value
    @param fielddef
        field definition - see "Settings dictionary" above
    @param read
        use read conversion if True, otherwise use write conversion
    @param raw
        return raw values (True) or converted values (False)

    @return:
        (un)converted value
    """
    converter, readconverter, writeconverter = get_fielddef(fielddef, fields='converter, readconverter, writeconverter')

    # call password functions even if raw value should be processed
    if read and callable(readconverter) and passwordread == readconverter:          # pylint: disable=comparison-with-callable
        raw = False
    if not read and callable(writeconverter) and passwordwrite == writeconverter:   # pylint: disable=comparison-with-callable
        raw = False

    if not raw and converter is not None:
        conv = readconverter if read else writeconverter
        try:
            if isinstance(conv, str):
                # evaluate strings
                return eval(conv.replace('$', 'value'))     # pylint: disable=eval-used
            elif callable(conv):
                # use as format function
                return conv(value)
        except Exception as err:    # pylint: disable=broad-except
            exit_(ExitCode.INTERNAL_ERROR, '{}'.format(err), type_=LogType.WARNING, line=inspect.getlineno(inspect.currentframe()))

    return value

def cmnd_converter(valuemapping, value, idx, readconverter, writeconverter, tasmotacmnd):    # pylint: disable=unused-argument
    """
    Convert field value into Tasmota command if available

    @param valuemapping:
        data mapping
    @param value:
        original value
    @param readconverter
        <function> to convert value from binary object to JSON
    @param writeconverter
        <function> to convert value from JSON back to binary object
    @param tasmotacmnd
        <function> convert data into Tasmota command function

    @return:
        converted value, list of values or None if unable to convert
    """
    result = None

    if (callable(readconverter) and readconverter == passwordread) or (callable(writeconverter) and writeconverter == passwordwrite):   # pylint: disable=comparison-with-callable
        if value == HIDDEN_PASSWORD:
            return None
        else:
            result = value

    if tasmotacmnd is not None and (callable(tasmotacmnd) or len(tasmotacmnd) > 0):
        if idx is not None:
            idx += 1
        if isinstance(tasmotacmnd, str): # evaluate strings
            if idx is not None:
                evalstr = tasmotacmnd.replace('$', 'value').replace('#', 'idx').replace('@', 'valuemapping')
            else:
                evalstr = tasmotacmnd.replace('$', 'value').replace('@', 'valuemapping')
            result = eval(evalstr)      # pylint: disable=eval-used

        elif callable(tasmotacmnd):     # use as format function
            if idx is not None:
                result = tasmotacmnd(value, idx)
            else:
                result = tasmotacmnd(value)

    return result

def validate_value(value, fielddef):
    """
    Validate a value if validator is defined in fielddef

    @param value:
        original value
    @param fielddef
        field definition - see "Settings dictionary" above

    @return:
        True if value is valid, False if invalid
    """
    validate = get_fielddef(fielddef, fields='validate')

    if value == 0:
        # can not complete all validate condition
        # some Tasmota values are not allowed to be 0 on input
        # even though these values are set to 0 on Tasmota initial.
        # so we can't validate 0 values
        return True

    valid = True
    try:
        if isinstance(validate, str): # evaluate strings
            valid = eval(validate.replace('$', 'value'))    # pylint: disable=eval-used
        elif callable(validate):     # use as format function
            valid = validate(value)
    except:     # pylint: disable=bare-except
        valid = False

    return valid

def get_formatcount(format_):
    """
    Get format prefix count

    @param format_:
        format specifier

    @return:
        prefix count or 1 if not specified
    """
    if isinstance(format_, str):
        match = re.search(r'\s*(\d+)', format_)
        if match:
            return int(match.group(0))

    return 1

def get_formattype(format_):
    """
    Get format type and bitsize without prefix

    @param format_:
        format specifier

    @return:
        (format_, 0) or (format without prefix, bitsize)
    """
    formattype = format_
    bitsize = 0
    if isinstance(format_, str):
        match = re.search(r'\s*(\D+)', format_)
        if match:
            formattype = match.group(0)
            bitsize = struct.calcsize(formattype) * 8
    return formattype, bitsize

def get_fieldminmax(fielddef):
    """
    Get minimum, maximum of field based on field format definition

    @param fielddef:
        field format - see "Settings dictionary" above

    @return:
        min, max
    """
    # pylint: disable=bad-whitespace
    minmax = {'c': (0,                   0xff),
              '?': (0,                   1),
              'b': (~0x7f,               0x7f),
              'B': (0,                   0xff),
              'h': (~0x7fff,             0x7fff),
              'H': (0,                   0xffff),
              'i': (~0x7fffffff,         0x7fffffff),
              'I': (0,                   0xffffffff),
              'l': (~0x7fffffff,         0x7fffffff),
              'L': (0,                   0xffffffff),
              'q': (~0x7fffffffffffffff, 0x7fffffffffffffff),
              'Q': (0,                   0x7fffffffffffffff),
              'f': (sys.float_info.min,  sys.float_info.max),
              'd': (sys.float_info.min,  sys.float_info.max),
             }
    # pylint: enable=bad-whitespace
    format_ = get_fielddef(fielddef, fields='format_')
    min_ = 0
    max_ = 0

    minmax_format = minmax.get(format_[-1:], None)
    if minmax_format is not None:
        min_, max_ = minmax_format
        max_ *= get_formatcount(format_)
    elif format_[-1:].lower() in ['s', 'p']:
        # s and p may have a prefix as length
        max_ = get_formatcount(format_)

    return min_, max_

def get_fieldlength(fielddef):
    """
    Get length of a field in bytes based on field format definition

    @param fielddef:
        field format - see "Settings dictionary" above

    @return:
        length of field in bytes
    """
    length = 0
    platform_, format_, addrdef, arraydef = get_fielddef(fielddef, fields='platform_, format_, addrdef, arraydef')

    # <arraydef> contains a integer list
    if isinstance(arraydef, list) and len(arraydef) > 0:
        # arraydef contains a list
        # calc size recursive by sum of all elements
        for _ in range(0, arraydef[0]):
            subfielddef = get_subfielddef(fielddef)
            if len(arraydef) > 1:
                length += get_fieldlength((platform_, format_, addrdef, subfielddef))
            # single array
            else:
                length += get_fieldlength((platform_, format_, addrdef, None))

    elif isinstance(format_, dict):
        # -> iterate through format
        addr = None
        setting = format_
        for name in setting:
            baseaddr = get_fielddef(setting[name], fields='baseaddr')
            _len = get_fieldlength(setting[name])
            if addr != baseaddr:
                addr = baseaddr
                length += _len

    # a simple value
    elif isinstance(format_, str):
        length = struct.calcsize(format_)

    return length

def get_subfielddef(fielddef):
    """
    Get subfield definition from a given field definition

    @param fielddef:
        see Settings desc above

    @return:
        subfield definition
    """
    platform_, format_, addrdef, datadef, arraydef, validate, cmd, converter = get_fielddef(fielddef, fields='platform_, format_, addrdef, datadef, arraydef, validate, cmd, converter')

    # create new arraydef
    if len(arraydef) > 1:
        arraydef = arraydef[1:]
    else:
        arraydef = None

    # create new datadef
    if isinstance(datadef, tuple):
        if cmd is not None:
            datadef = (arraydef, validate, cmd)
        else:
            datadef = (arraydef, validate)
    else:
        datadef = arraydef

    # set new field def
    subfielddef = None
    if converter is not None:
        subfielddef = (platform_, format_, addrdef, datadef, converter)
    else:
        subfielddef = (platform_, format_, addrdef, datadef)

    return subfielddef

def is_filtergroup(group):
    """
    Check if group is valid on filter

    @param grooup:
        group name to check

    @return:
        True if group is in filter, otherwise False
    """
    if ARGS.filter is not None:
        if group is None:
            return False
        if group == VIRTUAL:
            return True
        if (INTERNAL.title() not in (groupname.title() for groupname in ARGS.filter) and group.title() == INTERNAL.title()) \
            or group.title() not in (groupname.title() for groupname in ARGS.filter):
            return False
    return True

def get_fieldvalue(fielddef, dobj, addr, idxoffset=0):
    """
    Get single field value from definition

    @param fielddef:
        see Settings desc
    @param dobj:
        decrypted binary config data
    @param addr
        addr within dobj

    @return:
        value read from dobj
    """
    format_, bits, bitshift, strindex = get_fielddef(fielddef, fields='format_, bits, bitshift, strindex')

    value_ = 0
    unpackedvalue = struct.unpack_from(format_, dobj, addr)
    _, bitsize = get_formattype(format_)

    if not format_[-1:].lower() in ['s', 'p']:
        for val in unpackedvalue:
            value_ <<= bitsize
            value_ = value_ + val
        value_ = bitsread(value_, bitshift, bits)
    else:
        value_ = ""

        # max length of this field
        maxlength = get_fieldlength(fielddef)

        # get unpacked binary value as stripped string
        str_ = str(unpackedvalue[0], STR_ENCODING, errors='ignore')
        # split into single or multiple list elements delimted by \0
        sarray = str_.split('\x00', SETTINGSTEXTINDEX.index('SET_MAX'))
        if isinstance(sarray, list):
            # strip trailing \0 bytes
            sarray = [element.rstrip('\x00') for element in sarray]
            if strindex is None:
                # single string
                str_ = sarray[0]
            else:
                # indexed string
                str_ = sarray[strindex+idxoffset]

        # remove unprintable char
        if maxlength:
            value_ = "".join(itertools.islice((c for c in str_ if c.isprintable()), maxlength))

    return value_

def set_fieldvalue(fielddef, dobj, addr, value):
    """
    Set single field value from definition

    @param fielddef:
        see Settings desc
    @param dobj:
        decrypted binary config data
    @param addr
        addr within dobj
    @param value
        new value

    @return:
        new decrypted binary config data
    """
    format_ = get_fielddef(fielddef, fields='format_')
    formatcnt = get_formatcount(format_)
    singletype, bitsize = get_formattype(format_)
    if debug(ARGS) >= 2:
        print("set_fieldvalue(): fielddef {}, addr 0x{:04x}  value {}  formatcnt {}  singletype {}  bitsize {}  ".format(fielddef, addr, value, formatcnt, singletype, bitsize), file=sys.stderr)
    if not format_[-1:].lower() in ['s', 'p']:
        addr += (bitsize // 8) * formatcnt
        for _ in range(0, formatcnt):
            addr -= (bitsize // 8)
            maxunsigned = ((2**bitsize) - 1)
            maxsigned = ((2**bitsize)>>1)-1
            val = value & maxunsigned
            if isinstance(value, int) and value < 0 and val > maxsigned:
                val = ((maxunsigned+1)-val) * (-1)
            if debug(ARGS) >= 3:
                print("set_fieldvalue(): Single type - fielddef {}, addr 0x{:04x}  value {}  singletype {}  bitsize {}".format(fielddef, addr, val, singletype, bitsize), file=sys.stderr)
            try:
                struct.pack_into(singletype, dobj, addr, val)
            except struct.error as err:
                exit_(ExitCode.RESTORE_DATA_ERROR,
                      "Single type {} [fielddef={}, addr=0x{:04x}, value={}] - skipped!".format(err, fielddef, addr, val),
                      type_=LogType.WARNING,
                      doexit=not ARGS.ignorewarning,
                      line=inspect.getlineno(inspect.currentframe()))
            value >>= bitsize
    else:
        if debug(ARGS) >= 3:
            print("set_fieldvalue(): String type - fielddef {}, addr 0x{:04x}  value {}  format_ {}".format(fielddef, addr, value, format_), file=sys.stderr)
        try:
            struct.pack_into(format_, dobj, addr, value)
        except struct.error as err:
            exit_(ExitCode.RESTORE_DATA_ERROR,
                  "String type {} [fielddef={}, addr=0x{:04x}, value={} - skipped!".format(err, fielddef, addr, value),
                  type_=LogType.WARNING,
                  doexit=not ARGS.ignorewarning,
                  line=inspect.getlineno(inspect.currentframe()))

    return dobj

def get_field(dobj, platform_bits, fieldname, fielddef, raw=False, addroffset=0, ignoregroup=False):
    """
    Get field value from definition

    @param dobj:
        decrypted binary config data
    @param platform_bits:
        platform bits is the bitmask for valid platform for this fielddef
    @param fieldname:
        name of the field
    @param fielddef:
        see Settings desc above
    @param raw
        return raw values (True) or converted values (False)
    @param addroffset
        use offset for baseaddr (used for recursive calls)
        for indexed strings: index into indexed string

    @return:
        field mapping
    """
    if isinstance(dobj, str):
        dobj = bytearray(dobj)

    valuemapping = None

    # get field definition
    platform_, format_, baseaddr, strindex, arraydef, group = get_fielddef(fielddef, fields='platform_, format_, baseaddr, strindex, arraydef, group')

    # filter platform
    if (platform_ & platform_bits) == 0:
        return valuemapping

    # filter groups
    if not ignoregroup and not is_filtergroup(group):
        return valuemapping

    # <arraydef> contains a integer list
    if isinstance(arraydef, list) and len(arraydef) > 0:
        valuemapping = []
        offset = 0
        for i in range(0, arraydef[0]):
            subfielddef = get_subfielddef(fielddef)
            length = get_fieldlength(subfielddef)
            if length != 0:
                if strindex is not None:
                    value = get_field(dobj, platform_bits, fieldname, subfielddef, raw=raw, addroffset=i)
                else:
                    value = get_field(dobj, platform_bits, fieldname, subfielddef, raw=raw, addroffset=addroffset+offset)
                valuemapping.append(value)
            offset += length

    # <format> contains a dict
    elif isinstance(format_, dict):
        mapping_value = {}
        # -> iterate through format
        for name in format_:
            value = None
            value = get_field(dobj, platform_bits, name, format_[name], raw=raw, addroffset=addroffset)
            if value is not None:
                mapping_value[name] = value
        # copy complete returned mapping
        valuemapping = copy.deepcopy(mapping_value)

    # a simple value
    elif isinstance(format_, (str, bool, int, float)):
        if get_fieldlength(fielddef) != 0:
            if strindex is not None:
                value = get_fieldvalue(fielddef, dobj, baseaddr, addroffset)
            else:
                value = get_fieldvalue(fielddef, dobj, baseaddr+addroffset)
            valuemapping = readwrite_converter(value, fielddef, read=True, raw=raw)

    else:
        exit_(ExitCode.INTERNAL_ERROR, "Wrong mapping format definition: '{}'".format(format_), type_=LogType.WARNING, doexit=not ARGS.ignorewarning, line=inspect.getlineno(inspect.currentframe()))

    return valuemapping

def set_field(dobj, platform_bits, fieldname, fielddef, restoremapping, addroffset=0, filename=""):
    """
    Get field value from definition

    @param dobj:
        decrypted binary config data
    @param platform_bits:
        platform bits is the bitmask for valid platform for this fielddef
    @param fieldname:
        name of the field
    @param fielddef:
        see Settings desc above
    @param restoremapping
        restore mapping with the new value(s)
    @param addroffset
        use offset for baseaddr (used for recursive calls)
    @param filename
        related filename (for messages only)

    @return:
        new decrypted binary config data
    """
    platform_, format_, baseaddr, bits, bitshift, strindex, arraydef, group, writeconverter = get_fielddef(fielddef, fields='platform_, format_, baseaddr, bits, bitshift, strindex, arraydef, group, writeconverter')
    # cast unicode
    fieldname = str(fieldname)

    # filter platform
    if (platform_ & platform_bits) == 0:
        return dobj

    # filter groups
    if not is_filtergroup(group):
        return dobj

    # do not write readonly values
    if writeconverter is False:
        if debug(ARGS) >= 2:
            print("set_field(): Readonly '{}' using '{}'/{}{} @{} skipped".format(fieldname, format_, arraydef, bits, hex(baseaddr+addroffset)), file=sys.stderr)
        return dobj

    # <arraydef> contains a list
    if isinstance(arraydef, list) and len(arraydef) > 0:
        offset = 0
        if len(restoremapping) > arraydef[0]:
            exit_(ExitCode.RESTORE_DATA_ERROR, "file '{sfile}', array '{sname}[{selem}]' exceeds max number of elements [{smax}]".format(sfile=filename, sname=fieldname, selem=len(restoremapping), smax=arraydef[0]), type_=LogType.WARNING, doexit=not ARGS.ignorewarning, line=inspect.getlineno(inspect.currentframe()))
        for i in range(0, arraydef[0]):
            subfielddef = get_subfielddef(fielddef)
            length = get_fieldlength(subfielddef)
            if length != 0:
                if i >= len(restoremapping): # restoremapping data list may be shorter than definition
                    break
                subrestore = restoremapping[i]
                if strindex is not None:
                    dobj = set_field(dobj, platform_bits, fieldname, subfielddef, subrestore, addroffset=i, filename=filename)
                else:
                    dobj = set_field(dobj, platform_bits, fieldname, subfielddef, subrestore, addroffset=addroffset+offset, filename=filename)
            offset += length

    # <format> contains a dict
    elif isinstance(format_, dict):
        for name, rm_fielddef in format_.items():    # -> iterate through format
            restoremap = restoremapping.get(name, None)
            if restoremap is not None:
                dobj = set_field(dobj, platform_bits, name, rm_fielddef, restoremap, addroffset=addroffset, filename=filename)

    # a simple value
    elif isinstance(format_, (str, bool, int, float)):
        valid = True
        err_text = ""
        errformat = ""

        min_, max_ = get_fieldminmax(fielddef)
        value = _value = None
        skip = False

        # simple char value
        if format_[-1:] in ['c']:
            try:
                value = readwrite_converter(restoremapping.encode(STR_ENCODING)[0], fielddef, read=False)
            except Exception as err:    # pylint: disable=broad-except
                exit_(ExitCode.INTERNAL_ERROR, '{}'.format(err), type_=LogType.WARNING, line=inspect.getlineno(inspect.currentframe()))
                valid = False

        # bool
        elif format_[-1:] in ['?']:
            try:
                value = readwrite_converter(bool(restoremapping), fielddef, read=False)
            except Exception as err:  # pylint: disable=broad-except
                exit_(ExitCode.INTERNAL_ERROR, '{}'.format(err), type_=LogType.WARNING, line=inspect.getlineno(inspect.currentframe()))
                valid = False

        # integer
        elif format_[-1:] in ['b', 'B', 'h', 'H', 'i', 'I', 'l', 'L', 'q', 'Q', 'P']:
            value = readwrite_converter(restoremapping, fielddef, read=False)
            if isinstance(value, str):
                value = int(value, 0)
            else:
                value = int(value)
            # bits
            if bits != 0:
                bitvalue = value
                value = struct.unpack_from(format_, dobj, baseaddr+addroffset)[0]
                # validate restoremapping value
                valid = validate_value(bitvalue, fielddef)
                if not valid:
                    err_text = "valid bit range exceeding"
                    value = bitvalue
                else:
                    mask = (1<<bits)-1
                    if bitvalue > mask:
                        min_ = 0
                        max_ = mask
                        _value = bitvalue
                        valid = False
                    else:
                        if bitshift >= 0:
                            bitvalue <<= bitshift
                            mask <<= bitshift
                        else:
                            bitvalue >>= abs(bitshift)
                            mask >>= abs(bitshift)
                        value &= (0xffffffff ^ mask)
                        value |= bitvalue

            # full size values
            else:
                # validate restoremapping function
                valid = validate_value(value, fielddef)
                if not valid:
                    err_text = "valid range exceeding"
                _value = value

        # float
        elif format_[-1:] in ['f', 'd']:
            try:
                value = readwrite_converter(float(restoremapping), fielddef, read=False)
            except:     # pylint: disable=bare-except
                valid = False

        # string
        elif format_[-1:].lower() in ['s', 'p']:
            value = readwrite_converter(restoremapping.encode(STR_ENCODING), fielddef, read=False)
            err_text = "string length exceeding"
            if value is not None:
                max_ -= 1
                valid = min_ <= len(value) <= max_
            else:
                skip = True
                valid = True
            # handle indexed strings
            if strindex is not None:
                # unpack index str from source baseaddr into str_
                unpackedvalue = struct.unpack_from(format_, dobj, baseaddr)
                str_ = str(unpackedvalue[0], STR_ENCODING, errors='ignore')
                # split into separate string values
                sarray = str_.split('\x00')
                if not isinstance(value, str):
                    value = str(value, STR_ENCODING, errors='ignore')
                # remember possible value changes
                prevvalue = sarray[strindex+addroffset]
                curvalue = value
                # change indexed string
                sarray[strindex+addroffset] = value
                # convert back to binary string stream
                value = '\0'.join(sarray).encode(STR_ENCODING)

        if value is None and not skip:
            # None is an invalid value
            valid = False

        if valid is None and not skip:
            # validate against object type size
            valid = min_ <= value <= max_
            if not valid:
                err_text = "type range exceeding"
                errformat = " [{smin}, {smax}]"

        if _value is None:
            # copy value before possible change below
            _value = value

        if isinstance(_value, str):
            _value = "'{}'".format(_value)

        if valid:
            if not skip:
                if debug(ARGS) >= 2:
                    sbits = " {} bits shift {}".format(bits, bitshift) if bits else ""
                    strvalue = "{} [{}]".format(_value, hex(value)) if isinstance(_value, int) else _value
                    print("set_field(): Set '{}' using '{}'/{}{} @{} to {}".format(fieldname, format_, arraydef, sbits, hex(baseaddr+addroffset), strvalue), file=sys.stderr)
                if fieldname != 'cfg_crc' and fieldname != 'cfg_crc32' and fieldname != 'cfg_timestamp'  and fieldname != '_':
                    if strindex is not None:
                        # do not use address offset for indexed strings
                        dobj = set_fieldvalue(fielddef, dobj, baseaddr, value)
                    else:
                        prevvalue = get_fieldvalue(fielddef, dobj, baseaddr+addroffset)
                        dobj = set_fieldvalue(fielddef, dobj, baseaddr+addroffset, value)
                        curvalue = get_fieldvalue(fielddef, dobj, baseaddr+addroffset)
                    if prevvalue != curvalue and ARGS.verbose:
                        message("Value for '{}' changed from {} to {}".format(fieldname, prevvalue, curvalue), type_=LogType.INFO)
                else:
                    if debug(ARGS) >= 2:
                        print("set_field(): Special field '{}' using '{}'/{}{} @{} skipped".format(fieldname, format_, arraydef, bits, hex(baseaddr+addroffset)), file=sys.stderr)
        else:
            sformat = "file '{sfile}' - {{'{sname}': {svalue}}} ({serror})"+errformat
            exit_(ExitCode.RESTORE_DATA_ERROR, sformat.format(sfile=filename, sname=fieldname, serror=err_text, svalue=_value, smin=min_, smax=max_), type_=LogType.WARNING, doexit=not ARGS.ignorewarning)

    return dobj

def set_cmnd(cmnds, platform_bits, fieldname, fielddef, valuemapping, mappedvalue, addroffset=0, idx=None):
    """
    Get Tasmota command mapping from given field value definition

    @param cmnds:
        Tasmota command mapping: { 'group': ['cmnd' <,'cmnd'...>] ... }
    @param platform_bits:
        platform bits is the bitmask for valid platform for this fielddef
    @param fieldname:
        name of the field
    @param fielddef:
        see Settings desc above
    @param valuemapping:
        data mapping
    @param mappedvalue
        mappedvalue mapping with the new value(s)
    @param addroffset
        use offset for baseaddr (used for recursive calls)
    @param idx
        optional array index

    @return:
        new Tasmota command mapping
    """
    def set_cmnds(cmnds, group, valuemapping, mappedvalue, idx, readconverter, writeconverter, tasmotacmnd):
        """
        Helper to append Tasmota commands to list
        """
        cmnd = cmnd_converter(valuemapping, mappedvalue, idx, readconverter, writeconverter, tasmotacmnd)
        if group is not None and cmnd is not None:
            if group not in cmnds:
                cmnds[group] = []
            if isinstance(cmnd, list):
                for command in cmnd:
                    cmnds[group].append(command)
            else:
                cmnds[group].append(cmnd)
        return cmnds

    platform_, format_, arraydef, group, readconverter, writeconverter, tasmotacmnd = get_fielddef(fielddef, fields='platform_, format_, arraydef, group, readconverter, writeconverter, tasmotacmnd')

    # cast unicode
    fieldname = str(fieldname)

    # filter platform
    if (platform_ & platform_bits) == 0:
        return cmnds

    # filter groups
    if not is_filtergroup(group):
        return cmnds

    # <arraydef> contains a list
    if isinstance(arraydef, list) and len(arraydef) > 0:
        offset = 0
        if len(mappedvalue) > arraydef[0]:
            exit_(ExitCode.RESTORE_DATA_ERROR, "array '{sname}[{selem}]' exceeds max number of elements [{smax}]".format(sname=fieldname, selem=len(mappedvalue), smax=arraydef[0]), type_=LogType.WARNING, doexit=not ARGS.ignorewarning, line=inspect.getlineno(inspect.currentframe()))
        for i in range(0, arraydef[0]):
            subfielddef = get_subfielddef(fielddef)
            length = get_fieldlength(subfielddef)
            if length != 0:
                if i >= len(mappedvalue): # mappedvalue data list may be shorter than definition
                    break
                subrestore = mappedvalue[i]
                cmnds = set_cmnd(cmnds, platform_bits, fieldname, subfielddef, valuemapping, subrestore, addroffset=addroffset+offset, idx=i)
            offset += length

    # <format> contains a dict
    elif isinstance(format_, dict):
        for name, rm_fielddef in format_.items():    # -> iterate through format
            mapped = mappedvalue.get(name, None)
            if mapped is not None:
                cmnds = set_cmnd(cmnds, platform_bits, name, rm_fielddef, valuemapping, mapped, addroffset=addroffset, idx=idx)

    # a simple value
    elif isinstance(format_, (str, bool, int, float)):
        if group is not None:
            group = group.title()
        if isinstance(tasmotacmnd, tuple):
            tasmotacmnds = tasmotacmnd
            for tasmotacmnd in tasmotacmnds:
                cmnds = set_cmnds(cmnds, group, valuemapping, mappedvalue, idx, readconverter, writeconverter, tasmotacmnd)
        else:
            cmnds = set_cmnds(cmnds, group, valuemapping, mappedvalue, idx, readconverter, writeconverter, tasmotacmnd)

    return cmnds

def bin2mapping(decode_cfg):
    """
    Decodes binary data stream into pyhton mappings dict

    @param decode_cfg:
        binary config data (decrypted)

    @return:
        valuemapping data as mapping dictionary
    """
    if isinstance(decode_cfg, str):
        decode_cfg = bytearray(decode_cfg)

    # get binary header and template to use
    config_info = get_config_info(decode_cfg)

    # check size if exists
    cfg_size = None
    cfg_size_fielddef = config_info['template'].get('cfg_size', None)
    if cfg_size_fielddef is not None:
        cfg_size = get_field(decode_cfg, Platform.ALL, 'cfg_size', cfg_size_fielddef, raw=True, ignoregroup=True)
        # read size should be same as definied in setting
        if cfg_size > config_info['template_size']:
            # may be processed
            exit_(ExitCode.DATA_SIZE_MISMATCH, "Number of bytes read does ot match - read {}, expected {} byte".format(cfg_size, config_info['template_size']), type_=LogType.ERROR, line=inspect.getlineno(inspect.currentframe()))
        elif cfg_size < config_info['template_size']:
            # less number of bytes can not be processed
            exit_(ExitCode.DATA_SIZE_MISMATCH, "Number of bytes read to small to process - read {}, expected {} byte".format(cfg_size, config_info['template_size']), type_=LogType.ERROR, line=inspect.getlineno(inspect.currentframe()))

    # check crc if exists
    cfg_crc_fielddef = config_info['template'].get('cfg_crc', None)
    if cfg_crc_fielddef is not None:
        cfg_crc = get_field(decode_cfg, Platform.ALL, 'cfg_crc', cfg_crc_fielddef, raw=True, ignoregroup=True)
    else:
        cfg_crc = get_settingcrc(decode_cfg)
    cfg_crc32 = None
    cfg_crc32_fielddef = config_info['template'].get('cfg_crc32', None)
    if cfg_crc32_fielddef is not None:
        cfg_crc32 = get_field(decode_cfg, Platform.ALL, 'cfg_crc32', cfg_crc32_fielddef, raw=True, ignoregroup=True)
    else:
        cfg_crc32 = get_settingcrc32(decode_cfg)
    cfg_timestamp = int(time.time())
    cfg_timestamp_fielddef = config_info['template'].get('cfg_timestamp', None)
    if cfg_timestamp_fielddef is not None:
        cfg_timestamp = get_field(decode_cfg, Platform.ALL, 'cfg_timestamp', cfg_timestamp_fielddef, raw=True, ignoregroup=True)

    if config_info['version'] < 0x0606000B:
        if cfg_crc != get_settingcrc(decode_cfg):
            exit_(ExitCode.DATA_CRC_ERROR, 'Data CRC error, read 0x{:4x} should be 0x{:4x}'.format(cfg_crc, get_settingcrc(decode_cfg)), type_=LogType.WARNING, doexit=not ARGS.ignorewarning, line=inspect.getlineno(inspect.currentframe()))
    else:
        if cfg_crc32 != get_settingcrc32(decode_cfg):
            exit_(ExitCode.DATA_CRC_ERROR, 'Data CRC32 error, read 0x{:8x} should be 0x{:8x}'.format(cfg_crc32, get_settingcrc32(decode_cfg)), type_=LogType.WARNING, doexit=not ARGS.ignorewarning, line=inspect.getlineno(inspect.currentframe()))

    # get valuemapping
    valuemapping = get_field(decode_cfg, 1<<config_info['platform'], None, (Platform.ALL, config_info['template'], 0, (None, None, ('System', None))), ignoregroup=True)

    # remove keys having empty object
    if valuemapping is not None:
        for key in {k: v for k, v in valuemapping.items() if isinstance(v, (dict, list, tuple)) and len(valuemapping[k]) == 0}:
            valuemapping.pop(key, None)

    # add header info
    valuemapping['header'] = {
        'timestamp':datetime.utcfromtimestamp(cfg_timestamp).strftime("%Y-%m-%d %H:%M:%S"),
        'format': {
            'jsonindent':   ARGS.jsonindent,
            'jsoncompact':  ARGS.jsoncompact,
            'jsonsort':     ARGS.jsonsort,
            'jsonhidepw':   ARGS.jsonhidepw,
        },
        'template': {
            'version':  hex(config_info['template_version']),
            'crc':      hex(cfg_crc),
        },
        'data': {
            'crc':      hex(get_settingcrc(decode_cfg)),
            'size':     len(decode_cfg),
        },
        'script': {
            'name':     os.path.basename(__file__),
            'version':  VER,
        },
        'os': (platform.machine(), platform.system(), platform.release(), platform.version(), platform.platform()),
        'python': platform.python_version()
        }
    if cfg_crc_fielddef is not None and cfg_size is not None:
        valuemapping['header']['template'].update({'size': cfg_size})
    if cfg_crc32_fielddef is not None:
        if cfg_crc32 is not None:
            valuemapping['header']['template'].update({'crc32': hex(cfg_crc32)})
        valuemapping['header']['data'].update({'crc32': hex(get_settingcrc32(decode_cfg))})
    if config_info['version'] != 0x0:
        valuemapping['header']['data'].update({'version': hex(config_info['version'])})

    return valuemapping

def mapping2bin(config, jsonconfig, filename=""):
    """
    Encodes into binary data stream

    @param config: dict
        'encode': encoded config data
        "decode": decoded config data
        "mapping": mapped config data
        'info': dict about config data (see get_config_info())
    @param jsonconfig:
        restore data mapping
    @param filename:
        name of the restore file (for error output only)

    @return:
        changed binary config data (decrypted) or None on error
    """
    # make empty binarray array
    _buffer = bytearray()
    # add data
    _buffer.extend(config['decode'])

    if config['info']['template'] is not None:
        # iterate through restore data mapping
        for name, data in jsonconfig.items():
            # key must exist in both dict
            setting_fielddef = config['info']['template'].get(name, None)
            if setting_fielddef is not None:
                set_field(_buffer, 1<<config['info']['platform'], name, setting_fielddef, data, addroffset=0, filename=filename)
            else:
                if name != 'header':
                    exit_(ExitCode.RESTORE_DATA_ERROR, "Restore file '{}' contains obsolete name '{}', skipped".format(filename, name), type_=LogType.WARNING, doexit=not ARGS.ignorewarning)

        # CRC32 calc takes precedence over CRC
        cfg_crc32_setting = config['info']['template'].get('cfg_crc32', None)
        if cfg_crc32_setting is not None:
            crc32 = get_settingcrc32(_buffer)
            struct.pack_into(cfg_crc32_setting[1], _buffer, cfg_crc32_setting[2], crc32)
        else:
            cfg_crc_setting = config['info']['template'].get('cfg_crc', None)
            if cfg_crc_setting is not None:
                crc = get_settingcrc(_buffer)
                struct.pack_into(cfg_crc_setting[1], _buffer, cfg_crc_setting[2], crc)
        return _buffer

    else:
        exit_(ExitCode.UNSUPPORTED_VERSION, "File '{}', Tasmota configuration version 0x{:x} not supported".format(filename, config['info']['version']), type_=LogType.WARNING, doexit=not ARGS.ignorewarning)

    return None

def mapping2cmnd(config):
    """
    Encodes mapping data into Tasmota command mapping

    @param config: dict
        'encode': encoded config data
        "decode": decoded config data
        "mapping": mapped config data
        'info': dict about config data (see get_config_info())

    @return:
        Tasmota command mapping {group: [cmnd <,cmnd <,...>>]}
    """
    cmnds = {}
    # iterate through restore data mapping
    for name, mapping in config['mapping'].items():
        # key must exist in both dict
        setting_fielddef = config['info']['template'].get(name, None)
        if setting_fielddef is not None:
            cmnds = set_cmnd(cmnds, 1<<config['info']['platform'], name, setting_fielddef, config['mapping'], mapping, addroffset=0)
        else:
            if name != 'header':
                exit_(ExitCode.RESTORE_DATA_ERROR, "Restore file contains obsolete name '{}', skipped".format(name), type_=LogType.WARNING, doexit=not ARGS.ignorewarning)

    return cmnds

def backup(backupfile, backupfileformat, config):
    """
    Create backup file

    @param backupfile:
        Raw backup filename from program args
    @param backupfileformat:
        Backup file format
    @param config: dict
        'encode': encoded config data
        "decode": decoded config data
        "mapping": mapped config data
        'info': dict about config data (see get_config_info())
    """
    def backup_dmp(backup_filename, config):
        # do dmp file write
        with open(backup_filename, "wb") as backupfp:
            backupfp.write(config['encode'])
    def backup_bin(backup_filename, config):
        # do bin file write
        with open(backup_filename, "wb") as backupfp:
            backupfp.write(config['decode'])
            backupfp.write(struct.pack('<L', BINARYFILE_MAGIC))
    def backup_json(backup_filename, config):
        # do json file write
        with codecs.open(backup_filename, "w", encoding="utf-8") as backupfp:
            backupfp.write(get_jsonstr(config['mapping'], ARGS.jsonsort, ARGS.jsonindent, ARGS.jsoncompact))

    backups = {
        FileType.DMP.lower():("Tasmota", FileType.DMP, backup_dmp),
        FileType.BIN.lower():("binary", FileType.BIN, backup_bin),
        FileType.JSON.lower():("JSON", FileType.JSON, backup_json)
        }

    # possible extension in filename overrules possible given -t/--backup-type parameter
    _, ext = os.path.splitext(backupfile)
    if ext.lower() == '.'+FileType.BIN.lower():
        backupfileformat = FileType.BIN
    elif ext.lower() == '.'+FileType.DMP.lower():
        backupfileformat = FileType.DMP
    elif ext.lower() == '.'+FileType.JSON.lower():
        backupfileformat = FileType.JSON

    dryrun = ""
    if ARGS.dryrun:
        if ARGS.verbose:
            message("Do not write backup files for dry run", type_=LogType.INFO)
        dryrun = "** Simulating ** "

    fileformat = None
    if backupfileformat.lower() in backups:
        _backup = backups[backupfileformat.lower()]
        fileformat = _backup[0]
        backup_filename = make_filename(backupfile, _backup[1], config['mapping'])
        if ARGS.verbose:
            message("{}Writing backup file '{}' ({} format)".format(dryrun, backup_filename, fileformat), type_=LogType.INFO)
        if not ARGS.dryrun:
            try:
                _backup[2](backup_filename, config)
            except Exception as err:    # pylint: disable=broad-except
                exit_(ExitCode.INTERNAL_ERROR, "'{}' {}".format(backup_filename, err), line=inspect.getlineno(inspect.currentframe()))

    if fileformat is not None and (ARGS.verbose or ((ARGS.backupfile is not None or ARGS.restorefile is not None) and not ARGS.output)):
        message("{}Backup successful to '{}' ({} format)"\
            .format(dryrun, backup_filename, fileformat), type_=LogType.INFO if ARGS.verbose else None)

def restore(restorefile, backupfileformat, config):
    """
    Restore from file

    @param encode_cfg:
        binary config data (encrypted)
    @param backupfileformat:
        Backup file format
    @param config: dict
        'encode': encoded config data
        "decode": decoded config data
        "mapping": mapped config data
        'info': dict about config data (see get_config_info())
    """
    global EXIT_CODE    # pylint: disable=global-statement

    new_encode_cfg = None

    restorefileformat = None
    if backupfileformat.lower() == 'bin':
        restorefileformat = FileType.BIN
    elif backupfileformat.lower() == 'dmp':
        restorefileformat = FileType.DMP
    elif backupfileformat.lower() == 'json':
        restorefileformat = FileType.JSON
    restorefilename = make_filename(restorefile, restorefileformat, config['mapping'])
    filetype = get_filetype(restorefilename)

    if filetype == FileType.DMP:
        if ARGS.verbose:
            message("Reading restore file '{}' (Tasmota format)".format(restorefilename), type_=LogType.INFO)
        try:
            with open(restorefilename, "rb") as restorefp:
                new_encode_cfg = restorefp.read()
        except Exception as err:    # pylint: disable=broad-except
            exit_(ExitCode.INTERNAL_ERROR, "'{}' {}".format(restorefilename, err), line=inspect.getlineno(inspect.currentframe()))

    elif filetype == FileType.BIN:
        if ARGS.verbose:
            message("Reading restore file '{}' (Binary format)".format(restorefilename), type_=LogType.INFO)
        try:
            with open(restorefilename, "rb") as restorefp:
                restorebin = restorefp.read()
        except Exception as err:    # pylint: disable=broad-except
            exit_(ExitCode.INTERNAL_ERROR, "'{}' {}".format(restorefilename, err), line=inspect.getlineno(inspect.currentframe()))
        decode_cfg = None
        header_format = '<L'
        if struct.unpack_from(header_format, restorebin, 0)[0] == BINARYFILE_MAGIC:
            # remove file format identifier (outdated header at the beginning)
            decode_cfg = restorebin[struct.calcsize(header_format):]
        elif struct.unpack_from(header_format, restorebin, len(restorebin)-struct.calcsize(header_format))[0] == BINARYFILE_MAGIC:
            # remove file format identifier (new append format)
            decode_cfg = restorebin[:len(restorebin)-struct.calcsize(header_format)]
        if decode_cfg is not None:
            # process binary to binary config
            new_encode_cfg = decrypt_encrypt(decode_cfg)

    elif filetype == FileType.JSON or filetype == FileType.INVALID_JSON:
        if ARGS.verbose:
            message("Reading restore file '{}' (JSON format)".format(restorefilename), type_=LogType.INFO)
        try:
            #with open(restorefilename, "r") as restorefp:
            with codecs.open(restorefilename, "r", encoding="utf-8") as restorefp:
                jsonconfig = json.load(restorefp)
        except ValueError as err:
            exit_(ExitCode.JSON_READ_ERROR, "File '{}' invalid JSON: {}".format(restorefilename, err), line=inspect.getlineno(inspect.currentframe()))
        # process json config to binary config
        new_decode_cfg = mapping2bin(config, jsonconfig, restorefilename)
        new_encode_cfg = decrypt_encrypt(new_decode_cfg)

    elif filetype == FileType.FILE_NOT_FOUND:
        exit_(ExitCode.FILE_NOT_FOUND, "File '{}' not found".format(restorefilename), line=inspect.getlineno(inspect.currentframe()))
    elif filetype == FileType.INCOMPLETE_JSON:
        exit_(ExitCode.JSON_READ_ERROR, "File '{}' incomplete JSON, missing name 'header'".format(restorefilename), line=inspect.getlineno(inspect.currentframe()))
    elif filetype == FileType.INVALID_BIN:
        exit_(ExitCode.FILE_READ_ERROR, "File '{}' invalid BIN format".format(restorefilename), line=inspect.getlineno(inspect.currentframe()))
    else:
        exit_(ExitCode.FILE_READ_ERROR, "File '{}' unknown error".format(restorefilename), line=inspect.getlineno(inspect.currentframe()))

    if new_encode_cfg is not None:
        new_decode_cfg = decrypt_encrypt(new_encode_cfg)
        if ARGS.verbose:
            # get binary header and template to use
            message("Config file contains data of Tasmota {}".format(get_versionstr(config['info']['version'])), type_=LogType.INFO)
        if ARGS.forcerestore or new_encode_cfg != config['encode']:
            dryrun = ""
            if ARGS.dryrun:
                if ARGS.verbose:
                    message("Configuration data changed but leaving untouched, simulating writes for dry run", type_=LogType.INFO)
                dryrun = "** Simulating ** "
                error_code = 0
            # write config direct to device via http
            if ARGS.device is not None:
                if not ARGS.dryrun:
                    error_code, error_str = push_tasmotaconfig(new_encode_cfg, ARGS.device, ARGS.port, ARGS.username, ARGS.password, verbosemsg="{}Push new data to '{}' using restore file '{}'".format(dryrun, ARGS.device, restorefilename))
                if error_code:
                    exit_(ExitCode.UPLOAD_CONFIG_ERROR, "Config data upload failed - {}".format(error_str), line=inspect.getlineno(inspect.currentframe()))
                else:
                    if ARGS.verbose or ((ARGS.backupfile is not None or ARGS.restorefile is not None) and not ARGS.output):
                        message("{}Restore successful to device '{}' from '{}'".format(dryrun, ARGS.device, restorefilename), type_=LogType.INFO if ARGS.verbose else None)

            # write config from a file
            elif ARGS.tasmotafile is not None:
                if ARGS.verbose:
                    message("{}Write new data to file '{}' using restore file '{}'".format(dryrun, ARGS.tasmotafile, restorefilename), type_=LogType.INFO)
                if not ARGS.dryrun:
                    try:
                        with open(ARGS.tasmotafile, "wb") as outputfile:
                            outputfile.write(new_encode_cfg)
                    except Exception as err:    # pylint: disable=broad-except
                        exit_(ExitCode.INTERNAL_ERROR, "'{}' {}".format(ARGS.tasmotafile, err), line=inspect.getlineno(inspect.currentframe()))
                if ARGS.verbose or ((ARGS.backupfile is not None or ARGS.restorefile is not None) and not ARGS.output):
                    message("{}Restore successful to file '{}' from '{}'".format(dryrun, ARGS.tasmotafile, restorefilename), type_=LogType.INFO if ARGS.verbose else None)

        else:
            EXIT_CODE = ExitCode.RESTORE_SKIPPED
            if ARGS.verbose or ((ARGS.backupfile is not None or ARGS.restorefile is not None) and not ARGS.output):
                message("Restore skipped, configuration data unchanged", type_=LogType.INFO if ARGS.verbose else None)

def output_tasmotacmnds(tasmotacmnds):
    """
    Print Tasmota command mapping

    @param tasmotacmnds:
        Tasmota command mapping {group: [cmnd <,cmnd <,...>>]}
    """
    def output_tasmotasubcmnds(cmnds):
        if ARGS.cmndsort:
            for cmnd in sorted(cmnds, key=lambda cmnd: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', cmnd)]):
                print("{}{}".format(" "*ARGS.cmndindent, cmnd))
        else:
            for cmnd in cmnds:
                print("{}{}".format(" "*ARGS.cmndindent, cmnd))

    groups = get_grouplist(SETTINGS[0][2])

    if ARGS.cmndgroup:
        for group in groups:
            if group.title() in (groupname.title() for groupname in tasmotacmnds):
                cmnds = tasmotacmnds[group]
                print()
                print("# {}:".format(group))
                output_tasmotasubcmnds(cmnds)

    else:
        cmnds = []
        for group in groups:
            if group.title() in (groupname.title() for groupname in tasmotacmnds):
                cmnds.extend(tasmotacmnds[group])
        output_tasmotasubcmnds(cmnds)

def parseargs():
    """
    Program argument parser

    @return:
        configargparse.parse_args() result
    """
    class HelpFormatter(configargparse.HelpFormatter):
        """
        Class for customizing the help output
        """

        def _format_action_invocation(self, action):
            """
            Reformat multiple metavar output
                -d <host>, --device <host>, --host <host>
            to single output
                -d, --device, --host <host>
            """

            orgstr = configargparse.HelpFormatter._format_action_invocation(self, action)
            if orgstr and orgstr[0] != '-': # only optional arguments
                return orgstr
            res = getattr(action, '_formatted_action_invocation', None)
            if res:
                return res

            options = orgstr.split(', ')
            if len(options) <= 1:
                action._formatted_action_invocation = orgstr    # pylint: disable=protected-access
                return orgstr

            return_list = []
            for option in options:
                meta = ""
                arg = option.split(' ')
                if len(arg) > 1:
                    meta = arg[1]
                return_list.append(arg[0])
            if len(meta) > 0 and len(return_list) > 0:
                return_list[len(return_list)-1] += " "+meta
            action._formatted_action_invocation = ', '.join(return_list)    # pylint: disable=protected-access
            return action._formatted_action_invocation  # pylint: disable=protected-access

    global PARSER   # pylint: disable=global-statement
    PARSER = configargparse.ArgumentParser(description='Backup/Restore Tasmota configuration data.',
                                           epilog='Either argument -d <host> or -f <filename> must be given.',
                                           add_help=False,
                                           formatter_class=lambda prog: HelpFormatter(prog))    # pylint: disable=unnecessary-lambda

    source = PARSER.add_argument_group('Source', 'Read/Write Tasmota configuration from/to')
    source.add_argument('-f', '--file',
                        metavar='<filename>',
                        dest='tasmotafile',
                        default=DEFAULTS['source']['tasmotafile'],
                        help="file to retrieve/write Tasmota configuration from/to (default: {})'".format(DEFAULTS['source']['tasmotafile']))
    source.add_argument('--tasmota-file', dest='tasmotafile', help=configargparse.SUPPRESS)
    source.add_argument('-d', '--device',
                        metavar='<host>',
                        dest='device',
                        default=DEFAULTS['source']['device'],
                        help="hostname or IP address to retrieve/send Tasmota configuration from/to (default: {})".format(DEFAULTS['source']['device']))
    source.add_argument('--host', dest='device', help=configargparse.SUPPRESS)
    source.add_argument('-P', '--port',
                        metavar='<port>',
                        dest='port',
                        default=DEFAULTS['source']['port'],
                        help="TCP/IP port number to use for the host connection (default: {})".format(DEFAULTS['source']['port']))
    source.add_argument('-u', '--username',
                        metavar='<username>',
                        dest='username',
                        default=DEFAULTS['source']['username'],
                        help="host HTTP access username (default: {})".format(DEFAULTS['source']['username']))
    source.add_argument('-p', '--password',
                        metavar='<password>',
                        dest='password',
                        default=DEFAULTS['source']['password'],
                        help="host HTTP access password (default: {})".format(DEFAULTS['source']['password']))

    backres = PARSER.add_argument_group('Backup/Restore', 'Backup & restore specification')
    backres.add_argument('-i', '--restore-file',
                         metavar='<filename>',
                         dest='restorefile',
                         default=DEFAULTS['backup']['backupfile'],
                         help="file to restore configuration from (default: {}). Replacements: @v=firmware version from config, @f=device friendly name from config, @h=device hostname from config, @H=device hostname from device (-d arg only)".format(DEFAULTS['backup']['restorefile']))
    backres.add_argument('-o', '--backup-file',
                         metavar='<filename>',
                         dest='backupfile',
                         default=DEFAULTS['backup']['backupfile'],
                         help="file to backup configuration to (default: {}). Replacements: @v=firmware version from config, @f=device friendly name from config, @h=device hostname from config, @H=device hostname from device (-d arg only)".format(DEFAULTS['backup']['backupfile']))
    backup_file_formats = ['json', 'bin', 'dmp']
    backres.add_argument('-t', '--backup-type',
                         metavar='|'.join(backup_file_formats),
                         dest='backupfileformat',
                         choices=backup_file_formats,
                         default=DEFAULTS['backup']['backupfileformat'],
                         help="backup filetype (default: '{}')".format(DEFAULTS['backup']['backupfileformat']))
    backres.add_argument('-E', '--extension',
                         dest='extension',
                         action='store_true',
                         default=DEFAULTS['backup']['extension'],
                         help="append filetype extension for -i and -o filename{}".format(' (default)' if DEFAULTS['backup']['extension'] else ''))
    backres.add_argument('-e', '--no-extension',
                         dest='extension',
                         action='store_false',
                         default=DEFAULTS['backup']['extension'],
                         help="do not append filetype extension, use -i and -o filename as passed{}".format(' (default)' if not DEFAULTS['backup']['extension'] else ''))
    backres.add_argument('-F', '--force-restore',
                         dest='forcerestore',
                         action='store_true',
                         default=DEFAULTS['backup']['forcerestore'],
                         help="force restore even configuration is identical{}".format(' (default)' if DEFAULTS['backup']['forcerestore'] else ''))

    jsonformat = PARSER.add_argument_group('JSON output', 'JSON format specification')
    jsonformat.add_argument('--json-indent',
                            metavar='<indent>',
                            dest='jsonindent',
                            type=int,
                            default=DEFAULTS['jsonformat']['jsonindent'],
                            help="pretty-printed JSON output using indent level (default: '{}'). -1 disables indent.".format(DEFAULTS['jsonformat']['jsonindent']))
    jsonformat.add_argument('--json-compact',
                            dest='jsoncompact',
                            action='store_true',
                            default=DEFAULTS['jsonformat']['jsoncompact'],
                            help="compact JSON output by eliminate whitespace{}".format(' (default)' if DEFAULTS['jsonformat']['jsoncompact'] else ''))

    jsonformat.add_argument('--json-sort',
                            dest='jsonsort',
                            action='store_true',
                            default=DEFAULTS['jsonformat']['jsonsort'],
                            help=configargparse.SUPPRESS) #"sort json keywords{}".format(' (default)' if DEFAULTS['jsonformat']['jsonsort'] else ''))
    jsonformat.add_argument('--json-unsort',
                            dest='jsonsort',
                            action='store_false',
                            default=DEFAULTS['jsonformat']['jsonsort'],
                            help=configargparse.SUPPRESS) #"do not sort json keywords{}".format(' (default)' if not DEFAULTS['jsonformat']['jsonsort'] else ''))

    jsonformat.add_argument('--json-hide-pw',
                            dest='jsonhidepw',
                            action='store_true',
                            default=DEFAULTS['jsonformat']['jsonhidepw'],
                            help="hide passwords{}".format(' (default)' if DEFAULTS['jsonformat']['jsonhidepw'] else ''))
    jsonformat.add_argument('--json-show-pw',
                            dest='jsonhidepw',
                            action='store_false',
                            default=DEFAULTS['jsonformat']['jsonhidepw'],
                            help="unhide passwords{}".format(' (default)' if not DEFAULTS['jsonformat']['jsonhidepw'] else ''))
    jsonformat.add_argument('--json-unhide-pw', dest='jsonhidepw', help=configargparse.SUPPRESS)

    cmndformat = PARSER.add_argument_group('Tasmota command output', 'Tasmota command output format specification')
    cmndformat.add_argument('--cmnd-indent',
                            metavar='<indent>',
                            dest='cmndindent',
                            type=int,
                            default=DEFAULTS['cmndformat']['cmndindent'],
                            help="Tasmota command grouping indent level (default: '{}'). 0 disables indent".format(DEFAULTS['cmndformat']['cmndindent']))
    cmndformat.add_argument('--cmnd-groups',
                            dest='cmndgroup',
                            action='store_true',
                            default=DEFAULTS['cmndformat']['cmndgroup'],
                            help="group Tasmota commands{}".format(' (default)' if DEFAULTS['cmndformat']['cmndgroup'] else ''))
    cmndformat.add_argument('--cmnd-nogroups',
                            dest='cmndgroup',
                            action='store_false',
                            default=DEFAULTS['cmndformat']['cmndgroup'],
                            help="leave Tasmota commands ungrouped{}".format(' (default)' if not DEFAULTS['cmndformat']['cmndgroup'] else ''))
    cmndformat.add_argument('--cmnd-sort',
                            dest='cmndsort',
                            action='store_true',
                            default=DEFAULTS['cmndformat']['cmndsort'],
                            help="sort Tasmota commands{}".format(' (default)' if DEFAULTS['cmndformat']['cmndsort'] else ''))
    cmndformat.add_argument('--cmnd-unsort',
                            dest='cmndsort',
                            action='store_false',
                            default=DEFAULTS['cmndformat']['cmndsort'],
                            help="leave Tasmota commands unsorted{}".format(' (default)' if not DEFAULTS['cmndformat']['cmndsort'] else ''))

    common = PARSER.add_argument_group('Common', 'Optional arguments')
    common.add_argument('-c', '--config',
                        metavar='<filename>',
                        dest='configfile',
                        default=DEFAULTS['common']['configfile'],
                        is_config_file=True,
                        help="program config file - can be used to set default command parameters (default: {})".format(DEFAULTS['common']['configfile']))

    common.add_argument('-S', '--output',
                        dest='output',
                        action='store_true',
                        default=DEFAULTS['common']['output'],
                        help="display output regardsless of backup/restore usage{}".format(" (default)" if DEFAULTS['common']['output'] else " (default do not output on backup or restore usage)"))
    output_formats = ['json', 'cmnd', 'command']
    common.add_argument('-T', '--output-format',
                        metavar='|'.join(output_formats),
                        dest='outputformat',
                        choices=output_formats,
                        default=DEFAULTS['common']['outputformat'],
                        help="display output format (default: '{}')".format(DEFAULTS['common']['outputformat']))
    groups = get_grouplist(SETTINGS[0][2])
    if VIRTUAL in groups:
        groups.remove(VIRTUAL)
    common.add_argument('-g', '--group',
                        dest='filter',
                        choices=groups,
                        nargs='+',
                        type=lambda s: s.title(),
                        default=DEFAULTS['common']['filter'],
                        help="limit data processing to command groups (default {})".format("no filter" if DEFAULTS['common']['filter'] is None else DEFAULTS['common']['filter']))
    common.add_argument('--ignore-warnings',
                        dest='ignorewarning',
                        action='store_true',
                        default=DEFAULTS['common']['ignorewarning'],
                        help="do not exit on warnings{}. Not recommended, used by your own responsibility!".format(' (default)' if DEFAULTS['common']['ignorewarning'] else ''))
    common.add_argument('--dry-run',
                        dest='dryrun',
                        action='store_true',
                        default=DEFAULTS['common']['ignorewarning'],
                        help="test program without changing configuration data on device or file{}".format(' (default)' if DEFAULTS['common']['dryrun'] else ''))


    info = PARSER.add_argument_group('Info', 'Extra information')
    info.add_argument('-D', '--debug',
                      dest='debug',
                      action='count',
                      help=configargparse.SUPPRESS)
    info.add_argument('-h', '--help',
                      dest='shorthelp',
                      action='store_true',
                      help='show usage help message and exit')
    info.add_argument("-H", "--full-help",
                      action="help",
                      help="show full help message and exit")
    info.add_argument('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      help='produce more output about what the program does')
    info.add_argument('-V', '--version',
                      dest='version',
                      action='count',
                      help="show program's version number and exit")

    _args = PARSER.parse_args()

    if debug(_args) >= 1:
        print(PARSER.format_values(), file=sys.stderr)
        print("Settings:", file=sys.stderr)
        for k in _args.__dict__:
            print("  "+str(k), "= ", eval('_args.{}'.format(k)), file=sys.stderr)    # pylint: disable=eval-used

    if _args.version is not None:
        print(PROG)
        if _args.version > 1 or debug(_args) >= 1:
            print()
            print("Script:   {}".format(os.path.basename(__file__)))
            print("Python:   {}".format(platform.python_version()))
            print("Platform: {} - {}".format(platform.platform(), platform.machine()))
            print("OS:       {} {} {}".format(platform.system(), platform.release(), platform.version()))
            print("Time:     {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        sys.exit(ExitCode.OK)

    return _args

if __name__ == "__main__":
    ARGS = parseargs()
    if ARGS.shorthelp:
        shorthelp()

    # check source args
    if ARGS.device is not None and ARGS.tasmotafile is not None:
        exit_(ExitCode.ARGUMENT_ERROR, "Unable to select source, do not use -d and -f together", line=inspect.getlineno(inspect.currentframe()))

    # default no configuration available
    ENCODE_CONFIG = None

    if debug(ARGS) >= 1:
        print("Checking setting definition")
        check_setting_definition()

    # pull config from Tasmota device
    if ARGS.tasmotafile is not None:
        ENCODE_CONFIG = load_tasmotaconfig(ARGS.tasmotafile)

    # load config from Tasmota file
    if ARGS.device is not None:
        ENCODE_CONFIG = pull_tasmotaconfig(ARGS.device, ARGS.port, username=ARGS.username, password=ARGS.password)

    if ENCODE_CONFIG is None:
        # no config source given
        shorthelp(False)
        print()
        print(PARSER.epilog)
        sys.exit(ExitCode.OK)

    if len(ENCODE_CONFIG) == 0:
        exit_(ExitCode.FILE_READ_ERROR,
              "Unable to read configuration data from {} '{}'"\
              .format('device' if ARGS.device is not None else 'file',
                      ARGS.device if ARGS.device is not None else ARGS.tasmotafile),
              line=inspect.getlineno(inspect.currentframe()))

    # decrypt Tasmota config
    DECODE_CONFIG = decrypt_encrypt(ENCODE_CONFIG)

    # decode into mappings dictionary
    CONFIG_MAPPING = bin2mapping(DECODE_CONFIG)

    # config dict
    CONFIG_INFO = get_config_info(DECODE_CONFIG)
    CONFIG = {
        'encode': ENCODE_CONFIG,
        "decode": DECODE_CONFIG,
        "mapping": CONFIG_MAPPING,
        'info': CONFIG_INFO
        }

    # check version compatibility
    if CONFIG['info']['version'] is not None:
        if ARGS.verbose:
            message("{} '{}' is using Tasmota v{} on {}"\
                .format('File' if ARGS.tasmotafile is not None else 'Device',
                        ARGS.tasmotafile if ARGS.tasmotafile is not None else ARGS.device,
                        get_versionstr(CONFIG['info']['version']),
                        get_platformstr(CONFIG['info']['platform'])),
                    type_=LogType.INFO)
        SUPPORTED_VERSION = sorted(SETTINGS, key=lambda s: s[0], reverse=True)[0][0]
        if CONFIG['info']['version'] > SUPPORTED_VERSION and not ARGS.ignorewarning:
            exit_(ExitCode.UNSUPPORTED_VERSION, \
                "Tasmota configuration data v{} currently unsupported!\n"
                "           The read configuration data is newer than the last\n"
                "           supported v{} by this program.\n"
                "           Newer Tasmota versions may contain changed data struc-\n"
                "           tures so that the data with older versions may become\n"
                "           incompatible. You can force proceeding at your own risk\n"
                "           by appending the parameter '--ignore-warnings'\n"
                "           Be warned: Forcing can lead to unpredictable results for\n"
                "           your Tasmota device. In the worst case, your Tasmota device\n"
                "           will not respond and you will have to flash it again using\n"
                "           the serial interface. If you are unsure and do not know the\n"
                "           changes in the configuration structure, you may able to use\n"
                "           the developer version of this program from\n"
                "           https://github.com/tasmota/decode-config/tree/development."\
                  .format(get_versionstr(CONFIG['info']['version']), get_versionstr(SUPPORTED_VERSION)),
                  type_=LogType.WARNING, doexit=not ARGS.ignorewarning)

    if ARGS.backupfile is not None:
        # backup to file
        backup(ARGS.backupfile, ARGS.backupfileformat, CONFIG)

    if ARGS.restorefile is not None:
        # restore from file
        restore(ARGS.restorefile, ARGS.backupfileformat, CONFIG)

    if (ARGS.backupfile is None and ARGS.restorefile is None) or ARGS.output:
        if ARGS.outputformat == 'json':
            # json screen output
            print(get_jsonstr(CONFIG['mapping'], ARGS.jsonsort, ARGS.jsonindent, ARGS.jsoncompact))

        if ARGS.outputformat == 'cmnd' or ARGS.outputformat == 'command':
            # Tasmota command output
            output_tasmotacmnds(mapping2cmnd(CONFIG))

    sys.exit(EXIT_CODE)
