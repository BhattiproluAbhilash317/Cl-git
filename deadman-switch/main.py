"""
 Module documentation
--------------------------------------------------------------------------------
 This script is used to monitor the online status of a server
 If a particular server is offline for too long, this script sends an automated
 email to a responsible system owner to identify further issues. 

 Story:  Power Outage
--------------------------------------------------------------------------------
 This script is installed and run as a daemont at a colocation and is 
 configured to monitor core server at a questionable datacenter.
 The questionable datacenter experiences a power outage.  The relevant UPS in
 the datacenter attempt to send a notificate, but a result of the outage 
 extends to network connectivity.  This script registers several consecutive
 failures and sends an email notifcation because the core server is was out of
 contact for too long, signalling a problem.

 Requirements:
-------------------------------------------------------------------------------
 Python 2.7
 ping must be installed and in default path
 installation for service/daemon

 Configuration
------------------------------------------------------------------------------
 included in a JSON configuration file. 
 logging: dictionary entry contains logging configuration for python logging.
     see python logging configuration for more details
 ping_host: is configurable entry to monitor network connectivity via ping 
 max_fail: is the maximum number of consecutive ping failures that the script 
    will accept before triggering an email message
 sleep: dictionary entry containing configuration for sleep intervals between
     ping attempts
     success: indicates the number of seconds to wait between pings on a 
         succesfull ping attempts
     fail: indicates the number of seconds to wait if a ping attempt fails
 mail: dictionary entry contains configuration for the email to send on trigger
    server: email relay server
    origin: who the mail is from
    destination: address for the system
    message: content of the message

 Installation
-------------------------------------------------------------------------------
 Windows 7 installation:
   windows service wrapper: https://github.com/kohsuke/winsw
   example provided in xml document 
 Linux system daemon installation:
   TODO:
       
"""


import sys
import subprocess
import time
import platform
import logging.config
import argparse
import json

from mailer import SimpleBulkMailer

log = logging.getLogger(__name__)

def load_json_file(filename):
    """ load a json configuration file from a filename
    parameters:
    filename:  name of the file that contains the json data
    return:
    python dict type representative of the contents of the JSON file
    or None type if something went wrong.
    """
    config = None
    log.debug('loading json file {}'.format(filename))
    try:
        with open(filename, 'r') as config_file:
            config = json.load(config_file)
    except (IOError, OSError) as ex: 
        log.critical('Error: cannot access file: {}'.format(filename))
        log.critical('IO Error: {} {}'.format(ex.errno, ex.strerror))
    except ValueError as ex: 
        log.critical('Error: bad json format file {}'.format(filename))
        log.critical(ex.message)
    log.debug('data loaded {}'.format(config))
    return config

def parse_arguments():
    """ logical division to organize command line argument gathering
        not intended for use beyond module
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("config_file", help="main configuration file for program")
    args = arg_parser.parse_args() 
    return args

def ping_host(host):
    """ send icmp echo to a host on IPv4 network
    parameters:
    host: string type that describes a IPv4
    return:
    boolean TRUE if host responds
    boolean FALSE if the host does not respond
    """
    cmd = []
    output = None
    if platform.system() == 'Windows':
        cmd = 'ping -n 1 {}'.format(host).split()
    else:
        cmd = 'ping -c 1 {}'.format(host).split()
    try:
        output = subprocess.check_output(cmd)
    except OSError as err:
        log.critical('{} is seems to be missing in your system or path'.format(cmd[0]))
        log.critical(err)
    except subprocess.CalledProcessError as ex:
        log.debug('no working {} {}'.format(ex.returncode, ex.message))
        return False
    except Exception as err:
        log.debug('exception? respond')
        log.debug('err')
        return False 
    log.debug('ping no other exception: {}'.format(output))
    return True

if __name__ == "__main__":
    LOGFORMAT = '%(asctime)s | %(levelname)-8s |  %(module)-16s | %(funcName)-16s | %(message)s'
    logging.basicConfig(format=LOGFORMAT,level=logging.DEBUG)
    arg = parse_arguments()
    cfg = load_json_file(arg.config_file)
    logging.config.dictConfig(cfg['logging'])

    mcfg = cfg['mail']
    mailer = SimpleBulkMailer(mcfg['server'], origin=mcfg['origin'])
    mailer.create_message(mcfg['subject'], mcfg['message'], mcfg['destination'])

    HOST = cfg['ping_host']
    SSLEEP = cfg['sleep']['success']
    FSLEEP = cfg['sleep']['fail']
    MAX_FAIL = cfg['max_fail']

    fail_count = 0
    loops = 0
    while True:
        if ping_host(HOST):
            failcount = 0
            log.debug('host {} ping respond'.format(HOST))
            time.sleep(SSLEEP)
        else:
            fail_count = fail_count + 1
            log.info('host {} did not respond, logging consecutive failure {}'.format(HOST, fail_count))
            time.sleep(FSLEEP)
        if fail_count >= MAX_FAIL:
            log.info('host {} indicated {} consecutive failures. Trigger engaged'.format(HOST, fail_count))
            mailer.send()
            fail_count = 0
        loops = loops + 1
        if loops == 100:
            log.info('application heartbeat:  main event loop')
            loops = 0

