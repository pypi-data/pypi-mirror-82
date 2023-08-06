from time import sleep

import os
import paramiko
import datetime
import time
import select
from bscearth.utils.log import Log
from autosubmit.job.job_common import Status
from autosubmit.job.job_common import Type
from autosubmit.platforms.platform import Platform
from bscearth.utils.date import date2str


class ParamikoPlatform(Platform):
    """
    Class to manage the connections to the different platforms with the Paramiko library.
    """

    def __init__(self, expid, name, config):
        """

        :param config:
        :param expid:
        :param name:
        """
        Platform.__init__(self, expid, name, config)
        self._default_queue = None
        self.job_status = None
        self._ssh = None
        self._ssh_config = None
        self._ssh_output = None
        self._user_config_file = None
        self._host_config = None
        self._host_config_id = None

    @property
    def header(self):
        """
        Header to add to jobs for scheduler configuration

        :return: header
        :rtype: object
        """
        return self._header

    @property
    def wrapper(self):
        """
        Handler to manage wrappers

        :return: wrapper-handler
        :rtype: object
        """
        return self._wrapper

    def connect(self):
        """
        Creates ssh connection to host

        :return: True if connection is created, False otherwise
        :rtype: bool
        """
        try:
            self._ssh = paramiko.SSHClient()
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh_config = paramiko.SSHConfig()
            self._user_config_file = os.path.expanduser("~/.ssh/config")
            if os.path.exists(self._user_config_file):
                with open(self._user_config_file) as f:
                    # noinspection PyTypeChecker
                    self._ssh_config.parse(f)
            self._host_config = self._ssh_config.lookup(self.host)
            if 'identityfile' in self._host_config:
                self._host_config_id = self._host_config['identityfile']
            if 'proxycommand' in self._host_config:
                self._proxy = paramiko.ProxyCommand(self._host_config['proxycommand'])
                self._ssh.connect(self._host_config['hostname'], 22, username=self.user,
                                  key_filename=self._host_config_id, sock=self._proxy)
            else:
                self._ssh.connect(self._host_config['hostname'], 22, username=self.user,
                                  key_filename=self._host_config_id)
            return True
        except IOError as e:
            Log.error('Can not create ssh connection to {0}: {1}', self.host, e.strerror)
            return False

    def check_completed_files(self, sections=None):
        if self.host == 'localhost':
            return None

        command = "find %s " % self.remote_log_dir
        if sections:
            for i, section in enumerate(sections.split()):
                command += " -name \*%s_COMPLETED" % section
                if i < len(sections.split())-1:
                    command += " -o "
        else:
            command += " -name \*_COMPLETED"

        if self.send_command(command):
            return self._ssh_output
        else:
            return None

    def remove_multiple_files(self, filenames):
        command = "rm " + filenames

        if self.send_command(command, ignore_log=True):
            return self._ssh_output
        else:
            return None

    def send_file(self, filename, check=True):
        """
        Sends a local file to the platform
        :param filename: name of the file to send
        :type filename: str
        """

        if self._ssh is None:
            if not self.connect():
                return None
        if check:
            self.check_remote_log_dir()
            self.delete_file(filename)

        try:
            ftp = self._ssh.open_sftp()
            ftp.put(os.path.join(self.tmp_path, filename), os.path.join(self.get_files_path(), filename))
            ftp.chmod(os.path.join(self.get_files_path(), filename),
                      os.stat(os.path.join(self.tmp_path, filename)).st_mode)
            ftp.close()
            return True
        except BaseException as e:
            Log.error('Can not send file {0} to {1}', os.path.join(self.tmp_path, filename),
                      os.path.join(self.get_files_path(), filename))
            raise

    def get_file(self, filename, must_exist=True, relative_path=''):
        """
        Copies a file from the current platform to experiment's tmp folder

        :param filename: file name
        :type filename: str
        :param must_exist: If True, raises an exception if file can not be copied
        :type must_exist: bool
        :param relative_path: path inside the tmp folder
        :type relative_path: str
        :return: True if file is copied successfully, false otherwise
        :rtype: bool
        """

        local_path = os.path.join(self.tmp_path, relative_path)
        if not os.path.exists(local_path):
            os.makedirs(local_path)

        file_path = os.path.join(local_path, filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        if self._ssh is None:
            if not self.connect():
                return None

        try:
            ftp = self._ssh.open_sftp()
            ftp.get(os.path.join(self.get_files_path(), filename), file_path)
            ftp.close()
            return True
        except BaseException:
            # ftp.get creates a local file anyway
            if os.path.exists(file_path):
                os.remove(file_path)
            if must_exist:
                raise Exception('File {0} does not exists'.format(filename))
            return False

    def delete_file(self, filename):
        """
        Deletes a file from this platform

        :param filename: file name
        :type filename: str
        :return: True if successful or file does no exists
        :rtype: bool
        """
        if self._ssh is None:
            if not self.connect():
                return None

        try:
            ftp = self._ssh.open_sftp()
            ftp.remove(os.path.join(self.get_files_path(), filename))
            ftp.close()
            return True
        except IOError:
            return True
        except BaseException as e:
            Log.debug('Could not remove file {0}'.format(os.path.join(self.get_files_path(), filename)))
            return False

    def move_file(self, src, dest,migrate=False):
        """
        Moves a file on the platform
        :param src: source name
        :type src: str
        :param dest: destination name
        :param migrate: ignore if file exist or not
        :type dest: str
        """
        if self._ssh is None:
            if not self.connect():
                return None

        try:
            ftp = self._ssh.open_sftp()
            if not migrate:
                ftp.rename(os.path.join(self.get_files_path(), src), os.path.join(self.get_files_path(), dest))
            else:
                try:
                    ftp.chdir((os.path.join(self.get_files_path(), src)))
                    ftp.rename(os.path.join(self.get_files_path(), src), os.path.join(self.get_files_path(),dest))
                except (IOError):
                    pass
            ftp.close()
            return True
        except BaseException:
            Log.debug('Could not move (rename) file {0} to {1}'.format(os.path.join(self.get_files_path(), src),
                                                                       os.path.join(self.get_files_path(), dest)))
            return False

    def submit_job(self, job, script_name):
        """
        Submit a job from a given job object.

        :param job: job object
        :type job: autosubmit.job.job.Job
        :param script_name: job script's name
        :rtype scriptname: str
        :return: job id for the submitted job
        :rtype: int
        """
        if self.send_command(self.get_submit_cmd(script_name, job)):
            job_id = self.get_submitted_job_id(self.get_ssh_output())
            Log.debug("Job ID: {0}", job_id)
            return int(job_id)
        else:
            return None

    def check_job(self, job_id, default_status=Status.COMPLETED, retries=5):
        """
        Checks job running status

        :param retries: retries
        :param job_id: job id
        :type job_id: str
        :param default_status: status to assign if it can be retrieved from the platform
        :type default_status: autosubmit.job.job_common.Status
        :return: current job status
        :rtype: autosubmit.job.job_common.Status
        """
        job_status = Status.UNKNOWN

        if type(job_id) is not int and type(job_id) is not str:
            # URi: logger
            Log.error('check_job() The job id ({0}) is not an integer neither a string.', job_id)
            # URi: value ?
            return job_status
        while not ( self.send_command(self.get_checkjob_cmd(job_id)) or (self.get_ssh_output() == "") ) and retries > 0:
            Log.warning('Retrying check job command: {0}', self.get_checkjob_cmd(job_id))
            Log.error('Can not get job status for job id ({0}), retrying in 5 sec', job_id)
            retries -= 1
            sleep(5)

        if retries > 0:
            Log.debug('Successful check job command: {0}', self.get_checkjob_cmd(job_id))
            job_status = self.parse_job_output(self.get_ssh_output()).strip("\n")
            # URi: define status list in HPC Queue Class
            if job_status in self.job_status['COMPLETED']:
                job_status = Status.COMPLETED
            elif job_status in self.job_status['RUNNING']:
                job_status = Status.RUNNING
            elif job_status in self.job_status['QUEUING']:
                job_status = Status.QUEUING
            elif job_status in self.job_status['FAILED']:
                job_status = Status.FAILED
            else:
                job_status = Status.UNKNOWN
        else:
            job_status = Status.UNKNOWN
            Log.error('check_job() The job id ({0}) status is {1}.', job_id, job_status)
        return job_status

    def get_checkjob_cmd(self, job_id):
        """
        Returns command to check job status on remote platforms

        :param job_id: id of job to check
        :param job_id: int
        :return: command to check job status
        :rtype: str
        """
        raise NotImplementedError
    def send_command(self, command, ignore_log=False):
        """
        Sends given command to HPC

        :param command: command to send
        :type command: str
        :return: True if executed, False if failed
        :rtype: bool
        """

        if self._ssh is None:
            if not self.connect():
                return None
        if "-rP" or "mv" or "find" or "convertLink" in command:
            timeout = 3600.0  # Max Wait 1hour if the command is a copy or simbolic links ( migrate can trigger long times)
        else:
            timeout = 1200.0  # Max Wait 20min in the normal workflow.
        try:
            stdin, stdout, stderr = self._ssh.exec_command(command)
            channel = stdout.channel
            channel.settimeout(timeout)
            stdin.close()
            channel.shutdown_write()
            stdout_chunks = []
            stdout_chunks.append(stdout.channel.recv(len(stdout.channel.in_buffer)))
            stderr_readlines = []

            while not channel.closed or channel.recv_ready() or channel.recv_stderr_ready():
                # stop if channel was closed prematurely, and there is no data in the buffers.
                got_chunk = False
                readq, _, _ = select.select([stdout.channel], [], [], timeout)
                for c in readq:
                    if c.recv_ready():
                        chunk_read=stdout.channel.recv(len(c.in_buffer))
                        if chunk_read != "\n":
                            stdout_chunks.append(chunk_read)
                        got_chunk = True
                    if c.recv_stderr_ready():
                        # make sure to read stderr to prevent stall
                        chunk_read = stderr.channel.recv_stderr(len(c.in_stderr_buffer))
                        if chunk_read != "\n":
                            stderr_readlines.append(chunk_read)
                        got_chunk = True
                if not got_chunk and stdout.channel.exit_status_ready() and not stderr.channel.recv_stderr_ready() and not stdout.channel.recv_ready():
                    # indicate that we're not going to read from this channel anymore
                    stdout.channel.shutdown_read()
                    # close the channel
                    stdout.channel.close()
                    break
            # close all the pseudofiles
            stdout.close()
            stderr.close()
            self._ssh_output = ""
            if len(stdout_chunks) > 0 :
                for s in stdout_chunks:
                    if s is not None:
                        self._ssh_output += s


            if len(stderr_readlines) > 0:
                if not ignore_log:
                    if len(stdout_chunks) > 0:
                        Log.warning('Command {0} in {1} warning: {2}', command, self.host, '\n'.join(stderr_readlines))
                else:
                    Log.debug('Command {0} in {1} warning: {2}', command, self.host, '\n'.join(stderr_readlines))
                if len(stdout_chunks) <= 0:
                    Log.critical('Command {0} in {1} warning: {2}', command, self.host, '\n'.join(stderr_readlines))
                    return False
            Log.debug('Command {0} in {1} successful with out message: {2}', command, self.host, self._ssh_output)
            return True
        except BaseException as e:
            Log.error('Can not send command {0} to {1}: {2}', command, self.host, e.message)
            return False

    def parse_job_output(self, output):
        """
        Parses check job command output so it can be interpreted by autosubmit

        :param output: output to parse
        :type output: str
        :return: job status
        :rtype: str
        """
        raise NotImplementedError

    def get_submit_cmd(self, job_script, job_type):
        """
        Get command to add job to scheduler

        :param job_type:
        :param job_script: path to job script
        :param job_script: str
        :return: command to submit job to platforms
        :rtype: str
        """
        raise NotImplementedError

    def get_mkdir_cmd(self):
        """
        Gets command to create directories on HPC

        :return: command to create directories on HPC
        :rtype: str
        """
        raise NotImplementedError

    def parse_queue_reason(self, output):
        raise NotImplementedError

    def get_ssh_output(self):
        """
        Gets output from last command executed

        :return: output from last command
        :rtype: str
        """
        Log.debug('Output {0}', self._ssh_output)
        return self._ssh_output

    def get_call(self, job_script, job):
        """
        Gets execution command for given job

        :param job: job
        :type job: Job
        :param job_script: script to run
        :type job_script: str
        :return: command to execute script
        :rtype: str
        """
        executable = ''
        if job.type == Type.BASH:
            executable = 'bash'
        elif job.type == Type.PYTHON:
            executable = 'python'
        elif job.type == Type.R:
            executable = 'Rscript'
        return 'nohup ' + executable + ' {0} > {1} 2> {2} & echo $!'.format(
            os.path.join(self.remote_log_dir, job_script),
            os.path.join(self.remote_log_dir, job.remote_logs[0]),
            os.path.join(self.remote_log_dir, job.remote_logs[1])
        )

    @staticmethod
    def get_pscall(job_id):
        """
        Gets command to check if a job is running given process identifier

        :param job_id: process indentifier
        :type job_id: int
        :return: command to check job status script
        :rtype: str
        """
        return 'nohup kill -0 {0} >& /dev/null; echo $?'.format(job_id)

    def get_submitted_job_id(self, output):
        """
        Parses submit command output to extract job id
        :param output: output to parse
        :type output: str
        :return: job id
        :rtype: str
        """
        raise NotImplementedError

    def get_header(self, job):
        """
        Gets header to be used by the job

        :param job: job
        :type job: Job
        :return: header to use
        :rtype: str
        """
        if str(job.processors) == '1':
            header = self.header.SERIAL
        else:
            header = self.header.PARALLEL

        str_datetime = date2str(datetime.datetime.now(), 'S')
        out_filename = "{0}.{1}.out".format(job.name, str_datetime)
        err_filename = "{0}.{1}.err".format(job.name, str_datetime)
        job.local_logs = (out_filename, err_filename)
        header = header.replace('%OUT_LOG_DIRECTIVE%', out_filename)
        header = header.replace('%ERR_LOG_DIRECTIVE%', err_filename)

        if hasattr(self.header, 'get_queue_directive'):
            header = header.replace('%QUEUE_DIRECTIVE%', self.header.get_queue_directive(job))
        if hasattr(self.header, 'get_tasks_per_node'):
            header = header.replace('%TASKS_PER_NODE_DIRECTIVE%', self.header.get_tasks_per_node(job))
        if hasattr(self.header, 'get_threads_per_task'):
            header = header.replace('%THREADS%', self.header.get_threads_per_task(job))
        if hasattr(self.header, 'get_scratch_free_space'):
            header = header.replace('%SCRATCH_FREE_SPACE_DIRECTIVE%', self.header.get_scratch_free_space(job))
        if hasattr(self.header, 'get_custom_directives'):
            header = header.replace('%CUSTOM_DIRECTIVES%', self.header.get_custom_directives(job))
        if hasattr(self.header, 'get_exclusivity'):
            header = header.replace('%EXCLUSIVITY_DIRECTIVE%', self.header.get_exclusivity(job))
        if hasattr(self.header, 'get_account_directive'):
            header = header.replace('%ACCOUNT_DIRECTIVE%', self.header.get_account_directive(job))
        if hasattr(self.header, 'get_memory_directive'):
            header = header.replace('%MEMORY_DIRECTIVE%', self.header.get_memory_directive(job))
        if hasattr(self.header, 'get_memory_per_task_directive'):
            header = header.replace('%MEMORY_PER_TASK_DIRECTIVE%', self.header.get_memory_per_task_directive(job))
        if hasattr(self.header, 'get_hyperthreading_directive'):
            header = header.replace('%HYPERTHREADING_DIRECTIVE%', self.header.get_hyperthreading_directive(job))
        return header

    def check_remote_log_dir(self):
        """
        Creates log dir on remote host
        """
        if self.send_command(self.get_mkdir_cmd()):
            Log.debug('{0} has been created on {1} .', self.remote_log_dir, self.host)
        else:
            Log.error('Could not create the DIR {0} on HPC {1}'.format(self.remote_log_dir, self.host))


class ParamikoPlatformException(Exception):
    """
    Exception raised from HPC queues
    """

    def __init__(self, msg):
        self.message = msg
