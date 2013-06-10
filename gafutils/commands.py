# -*- coding: utf-8 -*- 
'''
Base command classes.

Created on 24 mars 2013

@author: gabriel
'''
from django.core.management.base import BaseCommand
from optparse import make_option
import os
from django.core.management.base import CommandError
from subprocess import check_call
import shlex
import logging

class SudoCommand(BaseCommand):
    """
    Base command supposed to be run as root user.
    Root user checking may be disabled by `--non-root` option.
    """
    
    option_list = BaseCommand.option_list + (
        make_option("--non-root",
            action="store_true",
            default=False,
            help=u"Skip user-is-root check"
        ),
    )
    
    def handle(self, *args, **options):
        
        if not os.getuid() is 0 and not options['non_root']:
            raise CommandError(u"This command must be run as root")
        
        self.sudo_handle(*args, **options)
        
class ExtendedBaseCommand(BaseCommand):
    """
    Extended command class
    """
    
    logger_name = None
    
    def handle(self, *args, **options):
        self.init_logging(*args, **options)
        return self.do_handle(*args, **options)
        
        
        
    def init_logging(self, *args, **options):
        self.logger = logging.getLogger(self.get_logger_name())
        if options['verbosity'] == "3":
            logging.getLogger().setLevel(logging.DEBUG)    
    
    def get_logger_name(self):
        if self.logger_name is not None:
            return self.logger_name
        module = self.__class__.__module__.split('.')
        cmd_name = module[-1]
        app_name = module[-4]
        
        return "%s.cmd.%s" % (app_name, cmd_name)
        
    def do_handle(self, *args, **options):
        raise NotImplementedError(u"Subclasses must override ExtendedBaseCommand.do_handle()")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



