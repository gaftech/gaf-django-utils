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
        
    
