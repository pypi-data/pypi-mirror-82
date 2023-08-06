#!/usr/bin/env python

# Copyright 2017 Earth Sciences Department, BSC-CNS

# This file is part of Autosubmit.

# Autosubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Autosubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Autosubmit.  If not, see <http://www.gnu.org/licenses/>.
import textwrap


class Status:
    """
    Class to handle the status of a job
    """
    WAITING = 0
    READY = 1
    SUBMITTED = 2
    QUEUING = 3
    RUNNING = 4
    COMPLETED = 5
    FAILED = -1
    UNKNOWN = -2
    SUSPENDED = -3
    #######
    # Note: any change on constants must be applied on the dict below!!!
    VALUE_TO_KEY = {-3: 'SUSPENDED', -2: 'UNKNOWN', -1: 'FAILED', 0: 'WAITING', 1: 'READY',
                    2: 'SUBMITTED', 3: 'QUEUING', 4: 'RUNNING', 5: 'COMPLETED'}

    def retval(self, value):
        return getattr(self, value)


class Type:
    """
    Class to handle the status of a job
    """
    BASH = 0
    PYTHON = 1
    R = 2

    def retval(self, value):
        return getattr(self, value)


# TODO: Statistics classes refactor proposal: replace tailer by footer


class StatisticsSnippetBash:
    """
    Class to handle the statistics snippet of a job. It contains header and tailer for
    local and remote jobs
    """

    @staticmethod
    def as_header(scheduler_header):
        return textwrap.dedent("""\
            #!/bin/bash

            """) + \
            scheduler_header + \
            textwrap.dedent("""\
            ###################
            # Autosubmit header
            ###################
            set -xuve
            job_name_ptrn='%CURRENT_LOGDIR%/%JOBNAME%'
            echo $(date +%s) > ${job_name_ptrn}_STAT

            ###################
            # Autosubmit job
            ###################
            
            """)

    @staticmethod
    def as_tailer():
        return textwrap.dedent("""\

                ###################
                # Autosubmit tailer
                ###################
                set -xuve
                echo $(date +%s) >> ${job_name_ptrn}_STAT
                touch ${job_name_ptrn}_COMPLETED
                exit 0
                
                """)


class StatisticsSnippetPython:
    """
    Class to handle the statistics snippet of a job. It contains header and tailer for
    local and remote jobs
    """

    @staticmethod
    def as_header(scheduler_header):
        return textwrap.dedent("""\
            #!/usr/bin/env python

            """) + \
            scheduler_header + \
            textwrap.dedent("""\
            ###################
            # Autosubmit header
            ###################

            import time

            job_name_ptrn = '%CURRENT_LOGDIR%/%JOBNAME%'
            stat_file = open(job_name_ptrn + '_STAT', 'w')
            stat_file.write('{0:.0f}\\n'.format(time.time()))
            stat_file.close()


            ###################
            # Autosubmit job
            ###################

            """)

    @staticmethod
    def as_tailer():
        return textwrap.dedent("""\

                ###################
                # Autosubmit tailer
                ###################

                stat_file = open(job_name_ptrn + '_STAT', 'a')
                stat_file.write('{0:.0f}\\n'.format(time.time()))
                stat_file.close()
                open(job_name_ptrn + '_COMPLETED', 'a').close()
                exit(0)
                """)


class StatisticsSnippetR:
    """
    Class to handle the statistics snippet of a job. It contains header and tailer for
    local and remote jobs
    """

    @staticmethod
    def as_header(scheduler_header):
        return textwrap.dedent("""\
            #!/usr/bin/env Rscript

            """) + \
            scheduler_header + \
            textwrap.dedent("""\
            ###################
            # Autosubmit header
            ###################

            job_name_ptrn = '%CURRENT_LOGDIR%/%JOBNAME%'    

            fileConn<-file(paste(job_name_ptrn,"_STAT", sep = ''),"w")
            writeLines(toString(trunc(as.numeric(Sys.time()))), fileConn)
            close(fileConn)

            ###################
            # Autosubmit job
            ###################

            """)

    @staticmethod
    def as_tailer():
        return textwrap.dedent("""\

            ###################
            # Autosubmit tailer
            ###################

            fileConn<-file(paste(job_name_ptrn,"_STAT", sep = ''),"a")
            writeLines(toString(trunc(as.numeric(Sys.time()))), fileConn)
            close(fileConn)

            fileConn<-file(paste(job_name_ptrn,'_COMPLETED', sep = ''), 'a')
            close(fileConn)
            quit(save = 'no', status = 0)
            """)


class StatisticsSnippetEmpty:
    """
    Class to handle the statistics snippet of a job. It contains header and footer for
    local and remote jobs
    """

    @staticmethod
    def as_header(scheduler_header):
        return textwrap.dedent("""\
            #!/bin/bash

            """) + \
            scheduler_header

    @staticmethod
    def as_tailer():
        return ''
