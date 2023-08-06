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
try:
    # noinspection PyCompatibility
    from configparser import SafeConfigParser
except ImportError:
    # noinspection PyCompatibility
    from ConfigParser import SafeConfigParser
import json

import os
import pickle
from time import localtime, strftime
from sys import setrecursionlimit
from shutil import move

from autosubmit.job.job import Job
from bscearth.utils.log import Log
from autosubmit.job.job_dict import DicJobs
from autosubmit.job.job_utils import Dependency
from autosubmit.job.job_common import Status, Type
from bscearth.utils.date import date2str, parse_date, sum_str_hours
from autosubmit.job.job_packages import JobPackageSimple, JobPackageArray, JobPackageThread

from networkx import DiGraph
from autosubmit.job.job_utils import transitive_reduction


class JobList:
    """
    Class to manage the list of jobs to be run by autosubmit

    """

    def __init__(self, expid, config, parser_factory, job_list_persistence):
        self._persistence_path = os.path.join(config.LOCAL_ROOT_DIR, expid, "pkl")
        self._update_file = "updated_list_" + expid + ".txt"
        self._failed_file = "failed_job_list_" + expid + ".pkl"
        self._persistence_file = "job_list_" + expid
        self._job_list = list()
        self._expid = expid
        self._config = config
        self._parser_factory = parser_factory
        self._stat_val = Status()
        self._parameters = []
        self._date_list = []
        self._member_list = []
        self._chunk_list = []
        self._dic_jobs = dict()
        self._persistence = job_list_persistence
        self._graph = DiGraph()

        self.packages_dict = dict()
        self._ordered_jobs_by_date_member = dict()

        self.packages_id = dict()
        self.job_package_map = dict()
        self.sections_checked = set()

    @property
    def expid(self):
        """
        Returns the experiment identifier

        :return: experiment's identifier
        :rtype: str
        """
        return self._expid

    @property
    def graph(self):
        """
        Returns the graph

        :return: graph
        :rtype: networkx graph
        """
        return self._graph

    @graph.setter
    def graph(self, value):
        self._graph = value

    def generate(self, date_list, member_list, num_chunks, chunk_ini, parameters, date_format, default_retrials,
                 default_job_type, wrapper_type=None, wrapper_jobs=None,new=True, notransitive=False):
        """
        Creates all jobs needed for the current workflow

        :param default_job_type: default type for jobs
        :type default_job_type: str
        :param date_list: start dates
        :type date_list: list
        :param member_list: members
        :type member_list: list
        :param num_chunks: number of chunks to run
        :type num_chunks: int
        :param chunk_ini: the experiment will start by the given chunk
        :type chunk_ini: int
        :param parameters: parameters for the jobs
        :type parameters: dict
        :param date_format: option to format dates
        :type date_format: str
        :param default_retrials: default retrials for ech job
        :type default_retrials: int
        :param new: is it a new generation?
        :type new: bool
        """
        self._parameters = parameters
        self._date_list = date_list
        self._member_list = member_list

        chunk_list = range(chunk_ini, num_chunks + 1)
        self._chunk_list = chunk_list

        jobs_parser = self._get_jobs_parser()

        dic_jobs = DicJobs(self, jobs_parser, date_list, member_list, chunk_list, date_format, default_retrials)
        self._dic_jobs = dic_jobs
        priority = 0

        Log.info("Creating jobs...")
        jobs_data = dict()
        if not new:
            jobs_data = {str(row[0]): row for row in self.load()}
        self._create_jobs(dic_jobs, jobs_parser, priority, default_job_type, jobs_data)
        Log.info("Adding dependencies...")
        self._add_dependencies(date_list, member_list, chunk_list, dic_jobs, jobs_parser, self.graph)

        Log.info("Removing redundant dependencies...")
        self.update_genealogy(new, notransitive)
        for job in self._job_list:
            job.parameters = parameters

        if wrapper_type == 'vertical-mixed':
            self._ordered_jobs_by_date_member = self._create_sorted_dict_jobs(wrapper_jobs)


    @staticmethod
    def _add_dependencies(date_list, member_list, chunk_list, dic_jobs, jobs_parser, graph, option="DEPENDENCIES"):
        for job_section in jobs_parser.sections():
            Log.debug("Adding dependencies for {0} jobs".format(job_section))

            # If does not have dependencies, do nothing
            if not jobs_parser.has_option(job_section, option):
                continue

            dependencies_keys = jobs_parser.get(job_section, option).split()
            dependencies = JobList._manage_dependencies(dependencies_keys, dic_jobs)

            for job in dic_jobs.get_jobs(job_section):
                num_jobs = 1
                if isinstance(job, list):
                    num_jobs = len(job)
                for i in range(num_jobs):
                    _job = job[i] if num_jobs > 1 else job
                    JobList._manage_job_dependencies(dic_jobs, _job, date_list, member_list, chunk_list, dependencies_keys,
                                                     dependencies, graph)

    @staticmethod
    def _manage_dependencies(dependencies_keys, dic_jobs):
        dependencies = dict()
        for key in dependencies_keys:
            distance = None
            splits = None
            sign = None

            if '-' not in key and '+' not in key:
                section = key
            else:
                sign = '-' if '-' in key else '+'
                key_split = key.split(sign)
                section = key_split[0]
                distance = int(key_split[1])

            if '[' in section:
                section_name = section[0:section.find("[")]
                splits_section = int(dic_jobs.get_option(section_name, 'SPLITS', 0))
                splits = JobList._calculate_splits_dependencies(section, splits_section)
                section = section_name

            dependency_running_type = dic_jobs.get_option(section, 'RUNNING', 'once').lower()
            delay = int(dic_jobs.get_option(section, 'DELAY', -1))
            dependency = Dependency(section, distance, dependency_running_type, sign, delay, splits)
            dependencies[key] = dependency
        return dependencies

    @staticmethod
    def _calculate_splits_dependencies(section, max_splits):
        splits_list = section[section.find("[") + 1:section.find("]")]
        splits = []
        for str_split in splits_list.split(","):
            if str_split.find(":") != -1:
                numbers = str_split.split(":")
                # change this to be checked in job_common.py
                max_splits = min(int(numbers[1]), max_splits)
                for count in range(int(numbers[0]), max_splits+1):
                    splits.append(int(str(count).zfill(len(numbers[0]))))
            else:
                if int(str_split) <= max_splits:
                    splits.append(int(str_split))
        return splits

    @staticmethod
    def _manage_job_dependencies(dic_jobs, job, date_list, member_list, chunk_list, dependencies_keys, dependencies,
                                 graph):
        for key in dependencies_keys:
            dependency = dependencies[key]

            skip, (chunk, member, date) = JobList._calculate_dependency_metadata(job.chunk, chunk_list,
                                                                                 job.member, member_list,
                                                                                 job.date, date_list,
                                                                                 dependency)
            if skip:
                continue

            for parent in dic_jobs.get_jobs(dependency.section, date, member, chunk):
                if dependency.delay == -1 or chunk > dependency.delay:
                    if isinstance(parent, list):
                        if job.split is not None:
                            parent = filter(lambda _parent: _parent.split == job.split, parent)[0]
                        else:
                            if dependency.splits is not None:
                                parent = filter(lambda _parent: _parent.split in dependency.splits, parent)

                    job.add_parent(parent)
                    JobList._add_edge(graph, job, parent)

            JobList.handle_frequency_interval_dependencies(chunk, chunk_list, date, date_list, dic_jobs, job, member,
                                                           member_list, dependency.section, graph)

    @staticmethod
    def _calculate_dependency_metadata(chunk, chunk_list, member, member_list, date, date_list, dependency):
        skip = False
        if dependency.sign is '-':
            if chunk is not None and dependency.running == 'chunk':
                chunk_index = chunk_list.index(chunk)
                if chunk_index >= dependency.distance:
                    chunk = chunk_list[chunk_index - dependency.distance]
                else:
                    skip = True
            elif member is not None and dependency.running in ['chunk', 'member']:
                member_index = member_list.index(member)
                if member_index >= dependency.distance:
                    member = member_list[member_index - dependency.distance]
                else:
                    skip = True
            elif date is not None and dependency.running in ['chunk', 'member', 'startdate']:
                date_index = date_list.index(date)
                if date_index >= dependency.distance:
                    date = date_list[date_index - dependency.distance]
                else:
                    skip = True

        if dependency.sign is '+':
            if chunk is not None and dependency.running == 'chunk':
                chunk_index = chunk_list.index(chunk)
                if (chunk_index + dependency.distance) < len(chunk_list):
                    chunk = chunk_list[chunk_index + dependency.distance]
                else:  # calculating the next one possible
                    temp_distance = dependency.distance
                    while temp_distance > 0:
                        temp_distance -= 1
                        if (chunk_index + temp_distance) < len(chunk_list):
                            chunk = chunk_list[chunk_index + temp_distance]
                            break

            elif member is not None and dependency.running in ['chunk', 'member']:
                member_index = member_list.index(member)
                if (member_index + dependency.distance) < len(member_list):
                    member = member_list[member_index + dependency.distance]
                else:
                    skip = True
            elif date is not None and dependency.running in ['chunk', 'member', 'startdate']:
                date_index = date_list.index(date)
                if (date_index + dependency.distance) < len(date_list):
                    date = date_list[date_index - dependency.distance]
                else:
                    skip = True
        return skip, (chunk, member, date)

    @staticmethod
    def handle_frequency_interval_dependencies(chunk, chunk_list, date, date_list, dic_jobs, job, member, member_list,
                                               section_name, graph):
        if job.wait and job.frequency > 1:
            if job.chunk is not None:
                max_distance = (chunk_list.index(chunk) + 1) % job.frequency
                if max_distance == 0:
                    max_distance = job.frequency
                for distance in range(1, max_distance):
                    for parent in dic_jobs.get_jobs(section_name, date, member, chunk - distance):
                        job.add_parent(parent)
                        JobList._add_edge(graph, job, parent)
            elif job.member is not None:
                member_index = member_list.index(job.member)
                max_distance = (member_index + 1) % job.frequency
                if max_distance == 0:
                    max_distance = job.frequency
                for distance in range(1, max_distance, 1):
                    for parent in dic_jobs.get_jobs(section_name, date,
                                                    member_list[member_index - distance], chunk):
                        job.add_parent(parent)
                        JobList._add_edge(graph, job, parent)
            elif job.date is not None:
                date_index = date_list.index(job.date)
                max_distance = (date_index + 1) % job.frequency
                if max_distance == 0:
                    max_distance = job.frequency
                for distance in range(1, max_distance, 1):
                    for parent in dic_jobs.get_jobs(section_name, date_list[date_index - distance],
                                                    member, chunk):
                        job.add_parent(parent)
                        JobList._add_edge(graph, job, parent)

    @staticmethod
    def _add_edge(graph, job, parents):
        num_parents = 1
        if isinstance(parents, list):
            num_parents = len(parents)
        for i in range(num_parents):
            parent = parents[i] if isinstance(parents, list) else parents
            graph.add_edge(parent.name, job.name)

    @staticmethod
    def _create_jobs(dic_jobs, parser, priority, default_job_type, jobs_data=dict()):
        for section in parser.sections():
            Log.debug("Creating {0} jobs".format(section))
            dic_jobs.read_section(section, priority, default_job_type, jobs_data)
            priority += 1

    def _create_sorted_dict_jobs(self, wrapper_jobs):
        dict_jobs = dict()
        for date in self._date_list:
            dict_jobs[date] = dict()
            for member in self._member_list:
                dict_jobs[date][member] = list()
        num_chunks = len(self._chunk_list)

        filtered_jobs_list = filter(lambda job: job.section in wrapper_jobs, self._job_list)

        filtered_jobs_fake_date_member, fake_original_job_map = self._create_fake_dates_members(filtered_jobs_list)

        sections_running_type_map = dict()
        for section in wrapper_jobs.split(" "):
            sections_running_type_map[section] = self._dic_jobs.get_option(section, "RUNNING", 'once')

        for date in self._date_list:
            str_date = self._get_date(date)
            for member in self._member_list:
                sorted_jobs_list = filter(lambda job: job.name.split("_")[1] == str_date and
                                                      job.name.split("_")[2] == member, filtered_jobs_fake_date_member)

                previous_job = sorted_jobs_list[0]
                section_running_type = sections_running_type_map[previous_job.section]

                jobs_to_sort = [previous_job]
                previous_section_running_type = None

                for index in range(1, len(sorted_jobs_list) + 1):
                    if index < len(sorted_jobs_list):
                        job = sorted_jobs_list[index]

                        if previous_job.section != job.section:
                            previous_section_running_type = section_running_type
                            section_running_type = sections_running_type_map[job.section]

                    if (previous_section_running_type != None and previous_section_running_type != section_running_type) \
                      or index == len(sorted_jobs_list):

                        jobs_to_sort = sorted(jobs_to_sort, key=lambda k: (k.name.split('_')[1], (k.name.split('_')[2]),
                                                                           (int(k.name.split('_')[3])
                                                                            if len(k.name.split('_')) == 5 else num_chunks + 1)))

                        for idx in range(0, len(jobs_to_sort)):
                            if jobs_to_sort[idx] in fake_original_job_map:
                                fake_job = jobs_to_sort[idx]
                                jobs_to_sort[idx] = fake_original_job_map[fake_job]

                        dict_jobs[date][member] += jobs_to_sort
                        jobs_to_sort = []

                    jobs_to_sort.append(job)
                    previous_job = job

        return dict_jobs

    def _create_fake_dates_members(self, filtered_jobs_list):
        filtered_jobs_fake_date_member = []
        fake_original_job_map = dict()

        import copy
        for job in filtered_jobs_list:
            fake_job = None
            # running once and synchronize date
            if job.date is None and job.member is None:
                date = self._date_list[-1]
                member = self._member_list[-1]

                fake_job = copy.deepcopy(job)
                fake_job.name = fake_job.name.split('_', 1)[0] + "_" + self._get_date(date) + "_" \
                                + member + "_" + fake_job.name.split("_", 1)[1]
                filtered_jobs_fake_date_member.append(fake_job)
                fake_original_job_map[fake_job] = job
            # running date or synchronize member
            elif job.member is None:
                member = self._member_list[-1]
                fake_job = copy.deepcopy(job)
                fake_job.name = fake_job.name.split('_', 2)[0] + "_" + fake_job.name.split('_', 2)[
                    1] + "_" + member + "_" + fake_job.name.split("_", 2)[2]
                filtered_jobs_fake_date_member.append(fake_job)
                fake_original_job_map[fake_job] = job

            if fake_job is None:
                filtered_jobs_fake_date_member.append(job)

        return filtered_jobs_fake_date_member, fake_original_job_map

    def _get_date(self, date):
        date_format = ''
        if date.hour > 1:
            date_format = 'H'
        if date.minute > 1:
            date_format = 'M'
        str_date = date2str(date, date_format)
        return str_date

    def __len__(self):
        return self._job_list.__len__()

    def get_date_list(self):
        """
        Get inner date list

        :return: date list
        :rtype: list
        """
        return self._date_list

    def get_member_list(self):

        """
        Get inner member list

        :return: member list
        :rtype: list
        """
        return self._member_list

    def get_chunk_list(self):
        """
        Get inner chunk list

        :return: chunk list
        :rtype: list
        """
        return self._chunk_list

    def get_job_list(self):
        """
        Get inner job list

        :return: job list
        :rtype: list
        """
        return self._job_list

    def get_date_format(self):
        date_format = ''
        for date in self.get_date_list():
            if date.hour > 1:
                date_format = 'H'
            if date.minute > 1:
                date_format = 'M'
        return date_format

    def get_ordered_jobs_by_date_member(self):
        """
        Get the dictionary of jobs ordered according to wrapper's expression divided by date and member

        :return: jobs ordered divided by date and member
        :rtype: dict
        """
        return self._ordered_jobs_by_date_member

    def get_completed(self, platform=None):
        """
        Returns a list of completed jobs

        :param platform: job platform
        :type platform: HPCPlatform
        :return: completed jobs
        :rtype: list
        """
        return [job for job in self._job_list if (platform is None or job.platform is platform) and
                job.status == Status.COMPLETED]
    def get_uncompleted(self, platform=None):
        """
        Returns a list of completed jobs

        :param platform: job platform
        :type platform: HPCPlatform
        :return: completed jobs
        :rtype: list
        """
        return [job for job in self._job_list if (platform is None or job.platform is platform) and
                job.status != Status.COMPLETED]
    def get_submitted(self, platform=None):
        """
        Returns a list of submitted jobs

        :param platform: job platform
        :type platform: HPCPlatform
        :return: submitted jobs
        :rtype: list
        """
        return [job for job in self._job_list if (platform is None or job.platform is platform) and
                job.status == Status.SUBMITTED]

    def get_running(self, platform=None):
        """
        Returns a list of jobs running

        :param platform: job platform
        :type platform: HPCPlatform
        :return: running jobs
        :rtype: list
        """
        return [job for job in self._job_list if (platform is None or job.platform is platform) and
                job.status == Status.RUNNING]

    def get_queuing(self, platform=None):
        """
        Returns a list of jobs queuing

        :param platform: job platform
        :type platform: HPCPlatform
        :return: queuedjobs
        :rtype: list
        """
        return [job for job in self._job_list if (platform is None or job.platform is platform) and
                job.status == Status.QUEUING]

    def get_failed(self, platform=None):
        """
        Returns a list of failed jobs

        :param platform: job platform
        :type platform: HPCPlatform
        :return: failed jobs
        :rtype: list
        """
        return [job for job in self._job_list if (platform is None or job.platform is platform) and
                job.status == Status.FAILED]

    def get_unsubmitted(self, platform=None):
        """
        Returns a list of unsummited jobs

        :param platform: job platform
        :type platform: HPCPlatform
        :return: all jobs
        :rtype: list
        """
        return [job for job in self._job_list if (platform is None or job.platform is platform) and
                ( job.status != Status.SUBMITTED and job.status != Status.QUEUING and job.status == Status.RUNNING and job.status == Status.COMPLETED ) ]
    def get_all(self, platform=None):
        """
        Returns a list of all jobs

        :param platform: job platform
        :type platform: HPCPlatform
        :return: all jobs
        :rtype: list
        """
        return [job for job in self._job_list]
    def get_ready(self, platform=None):
        """
        Returns a list of ready jobs

        :param platform: job platform
        :type platform: HPCPlatform
        :return: ready jobs
        :rtype: list
        """
        return [job for job in self._job_list if (platform is None or job.platform is platform) and
                job.status == Status.READY]

    def get_waiting(self, platform=None):
        """
        Returns a list of jobs waiting

        :param platform: job platform
        :type platform: HPCPlatform
        :return: waiting jobs
        :rtype: list
        """
        return [job for job in self._job_list if (platform is None or job.platform is platform) and
                job.status == Status.WAITING]

    def get_unknown(self, platform=None):
        """
        Returns a list of jobs on unknown state

        :param platform: job platform
        :type platform: HPCPlatform
        :return: unknown state jobs
        :rtype: list
        """
        return [job for job in self._job_list if (platform is None or job.platform is platform) and
                job.status == Status.UNKNOWN]

    def get_suspended(self, platform=None):
        """
        Returns a list of jobs on unknown state

        :param platform: job platform
        :type platform: HPCPlatform
        :return: unknown state jobs
        :rtype: list
        """
        return [job for job in self._job_list if (platform is None or job.platform is platform) and
                job.status == Status.SUSPENDED]

    def get_in_queue(self, platform=None):
        """
        Returns a list of jobs in the platforms (Submitted, Running, Queuing, Unknown)

        :param platform: job platform
        :type platform: HPCPlatform
        :return: jobs in platforms
        :rtype: list
        """
        return self.get_submitted(platform) + self.get_running(platform) + self.get_queuing(
            platform) + self.get_unknown(platform)

    def get_not_in_queue(self, platform=None):
        """
        Returns a list of jobs NOT in the platforms (Ready, Waiting)

        :param platform: job platform
        :type platform: HPCPlatform
        :return: jobs not in platforms
        :rtype: list
        """
        return self.get_ready(platform) + self.get_waiting(platform)

    def get_finished(self, platform=None):
        """
        Returns a list of jobs finished (Completed, Failed)


        :param platform: job platform
        :type platform: HPCPlatform
        :return: finished jobs
        :rtype: list
        """
        return self.get_completed(platform) + self.get_failed(platform)

    def get_active(self, platform=None):
        """
        Returns a list of active jobs (In platforms, Ready)

        :param platform: job platform
        :type platform: HPCPlatform
        :return: active jobs
        :rtype: list
        """
        return self.get_in_queue(platform) + self.get_ready(platform)

    def get_job_by_name(self, name):
        """
        Returns the job that its name matches parameter name

        :parameter name: name to look for
        :type name: str
        :return: found job
        :rtype: job
        """
        for job in self._job_list:
            if job.name == name:
                return job
        Log.warning("We could not find that job {0} in the list!!!!", name)

    def get_in_queue_grouped_id(self, platform):
        jobs = self.get_in_queue(platform)
        jobs_by_id = dict()
        for job in jobs:
            if job.id not in jobs_by_id:
                jobs_by_id[job.id] = list()
            jobs_by_id[job.id].append(job)
        return jobs_by_id

    def get_in_ready_grouped_id(self, platform):
        jobs=[]
        [jobs.append(job) for job in jobs if (platform is None or job._platform.name is platform.name)]

        jobs_by_id = dict()
        for job in jobs:
            if job.id not in jobs_by_id:
                jobs_by_id[job.id] = list()
            jobs_by_id[job.id].append(job)
        return jobs_by_id

    def sort_by_name(self):
        """
        Returns a list of jobs sorted by name

        :return: jobs sorted by name
        :rtype: list
        """
        return sorted(self._job_list, key=lambda k: k.name)

    def sort_by_id(self):
        """
        Returns a list of jobs sorted by id

        :return: jobs sorted by ID
        :rtype: list
        """
        return sorted(self._job_list, key=lambda k: k.id)

    def sort_by_type(self):
        """
        Returns a list of jobs sorted by type

        :return: job sorted by type
        :rtype: list
        """
        return sorted(self._job_list, key=lambda k: k.type)

    def sort_by_status(self):
        """
        Returns a list of jobs sorted by status

        :return: job sorted by status
        :rtype: list
        """
        return sorted(self._job_list, key=lambda k: k.status)

    @staticmethod
    def load_file(filename):
        """
        Recreates an stored joblist from the pickle file

        :param filename: pickle file to load
        :type filename: str
        :return: loaded joblist object
        :rtype: JobList
        """
        if os.path.exists(filename):
            fd = open(filename, 'rw')
            return pickle.load(fd)
        else:
            Log.critical('File {0} does not exist'.format(filename))
            return list()

    def load(self):
        """
        Recreates an stored job list from the persistence

        :return: loaded job list object
        :rtype: JobList
        """
        Log.info("Loading JobList")
        return self._persistence.load(self._persistence_path, self._persistence_file)

    def save(self):
        """
        Persists the job list
        """
        self._persistence.save(self._persistence_path, self._persistence_file, self._job_list)

    def update_from_file(self, store_change=True):
        """
        Updates jobs list on the fly from and update file
        :param store_change: if True, renames the update file to avoid reloading it at the next iteration
        """
        if os.path.exists(os.path.join(self._persistence_path, self._update_file)):
            Log.info("Loading updated list: {0}".format(os.path.join(self._persistence_path, self._update_file)))
            for line in open(os.path.join(self._persistence_path, self._update_file)):
                if line.strip() == '':
                    continue
                job = self.get_job_by_name(line.split()[0])
                if job:
                    job.status = self._stat_val.retval(line.split()[1])
                    job.fail_count = 0
            now = localtime()
            output_date = strftime("%Y%m%d_%H%M", now)
            if store_change:
                move(os.path.join(self._persistence_path, self._update_file),
                     os.path.join(self._persistence_path, self._update_file +
                                  "_" + output_date))

    @property
    def parameters(self):
        """
        List of parameters common to all jobs
        :return: parameters
        :rtype: dict
        """
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = value

    def update_list(self, as_conf,store_change=True,fromSetStatus=False):
        """
        Updates job list, resetting failed jobs and changing to READY all WAITING jobs with all parents COMPLETED

        :param as_conf: autosubmit config object
        :type as_conf: AutosubmitConfig
        :return: True if job status were modified, False otherwise
        :rtype: bool
        """
        # load updated file list
        save = False
        if self.update_from_file(store_change):
            save = store_change

        # reset jobs that has failed less than 10 times
        Log.debug('Updating FAILED jobs')
        for job in self.get_failed():
            job.inc_fail_count()
            if not hasattr(job, 'retrials') or job.retrials is None:
                retrials = as_conf.get_retrials()
            else:
                retrials = job.retrials

            if job.fail_count <= retrials:
                tmp = [parent for parent in job.parents if parent.status == Status.COMPLETED]
                if len(tmp) == len(job.parents):
                    job.status = Status.READY
                    job.packed = False
                    save = True
                    Log.debug("Resetting job: {0} status to: READY for retrial...".format(job.name))
                else:
                    job.status = Status.WAITING
                    save = True
                    job.packed = False
                    Log.debug("Resetting job: {0} status to: WAITING for parents completion...".format(job.name))

        # if waiting jobs has all parents completed change its State to READY


        for job in self.get_completed():

            if job.synchronize is not None: #and job in self.get_active():
                Log.debug('Updating SYNC jobs')
                tmp = [parent for parent in job.parents if parent.status == Status.COMPLETED]
                if len(tmp) != len(job.parents):
                    job.status = Status.WAITING
                    save = True
                    Log.debug("Resetting sync job: {0} status to: WAITING for parents completion...".format(job.name))
        Log.debug('Update finished')


        Log.debug('Updating WAITING jobs')
        for job in self.get_waiting():
            if not fromSetStatus:
                tmp = [parent for parent in job.parents if parent.status == Status.COMPLETED]
                if len(tmp) == len(job.parents):
                    job.status = Status.READY
                    save = True
                    Log.debug("Resetting job: {0} status to: READY (all parents completed)...".format(job.name))
        Log.debug('Update finished')

        return save

    def update_genealogy(self, new=True, notransitive=False):
        """
        When we have created the job list, every type of job is created.
        Update genealogy remove jobs that have no templates
        :param new: if it is a new job list or not
        :type new: bool
        """

        # Use a copy of job_list because original is modified along iterations
        for job in self._job_list[:]:
            if job.file is None or job.file == '':
                self._remove_job(job)

        # Simplifying dependencies: if a parent is already an ancestor of another parent,
        # we remove parent dependency
        if not notransitive:
            self.graph = transitive_reduction(self.graph)
            for job in self._job_list:
                children_to_remove = [child for child in job.children if child.name not in self.graph.neighbors(job.name)]
                for child in children_to_remove:
                    job.children.remove(child)
                    child.parents.remove(job)

        for job in self._job_list:
            if not job.has_parents() and new:
                job.status = Status.READY

    def check_scripts(self, as_conf):
        """
        When we have created the scripts, all parameters should have been substituted.
        %PARAMETER% handlers not allowed

        :param as_conf: experiment configuration
        :type as_conf: AutosubmitConfig
        """
        Log.info("Checking scripts...")
        out = True
        for job in self._job_list:
            if job.check.lower() == 'on_submission':
                continue
            if job.check.lower() != 'true':
                show_logs = False
                if job.section not in self.sections_checked:
                    Log.warning('Template {0} will be checked without logs'.format(job.section))
            elif job.section in self.sections_checked:
                show_logs = False
            else:
                show_logs = True

            if not job.check_script(as_conf, self.parameters,show_logs):
                out = False
                if show_logs:
                    Log.warning("Invalid parameter substitution in {0} template", job.section)

            self.sections_checked.add(job.section)
        if out:
            Log.result("Scripts OK")
        else:
            Log.warning("Scripts check failed")
            Log.user_warning("Running after failed scripts check is at your own risk!")
        return out

    def _remove_job(self, job):
        """
        Remove a job from the list

        :param job: job to remove
        :type job: Job
        """
        for child in job.children:
            for parent in job.parents:
                child.add_parent(parent)
            child.delete_parent(job)

        for parent in job.parents:
            parent.children.remove(job)

        self._job_list.remove(job)

    def rerun(self, chunk_list, notransitive=False,monitor=False):
        """
        Updates job list to rerun the jobs specified by chunk_list

        :param chunk_list: list of chunks to rerun
        :type chunk_list: str
        """
        jobs_parser = self._get_jobs_parser()

        Log.info("Adding dependencies...")
        dependencies = dict()
        for job_section in jobs_parser.sections():
            Log.debug("Reading rerun dependencies for {0} jobs".format(job_section))

            # If does not has rerun dependencies, do nothing
            if not jobs_parser.has_option(job_section, "RERUN_DEPENDENCIES"):
                continue

            dependencies_keys = jobs_parser.get(job_section, "RERUN_DEPENDENCIES").split()
            dependencies = JobList._manage_dependencies(dependencies_keys, self._dic_jobs)

        for job in self._job_list:
            job.status = Status.COMPLETED

        data = json.loads(chunk_list)
        for d in data['sds']:
            date = parse_date(d['sd'])
            Log.debug("Date: {0}", date)
            for m in d['ms']:
                member = m['m']
                Log.debug("Member: " + member)
                previous_chunk = 0
                for c in m['cs']:
                    Log.debug("Chunk: " + c)
                    chunk = int(c)
                    for job in [i for i in self._job_list if i.date == date and i.member == member and  (i.chunk == chunk ) ]:

                        if not job.rerun_only or chunk != previous_chunk + 1:
                            job.status = Status.WAITING
                            Log.debug("Job: " + job.name)

                        job_section = job.section
                        if job_section not in dependencies:
                            continue

                        for key in dependencies_keys:
                            skip, (current_chunk, current_member, current_date) = JobList._calculate_dependency_metadata(chunk, member, date,
                                                                                                 dependencies[key])
                            if skip:
                                continue

                            section_name = dependencies[key].section
                            for parent in self._dic_jobs.get_jobs(section_name, current_date, current_member,
                                                                  current_chunk):
                                parent.status = Status.WAITING
                                Log.debug("Parent: " + parent.name)


        for job in [j for j in self._job_list if j.status == Status.COMPLETED]:
            if job.synchronize is None:
                self._remove_job(job)

        self.update_genealogy(notransitive=notransitive)
        for job in [j for j in self._job_list if j.synchronize !=None]:
            if job.status == Status.COMPLETED:
                job.status = Status.WAITING
            else:
                self._remove_job(job)

    def _get_jobs_parser(self):
        jobs_parser = self._parser_factory.create_parser()
        jobs_parser.optionxform = str
        jobs_parser.read(
            os.path.join(self._config.LOCAL_ROOT_DIR, self._expid, 'conf', "jobs_" + self._expid + ".conf"))
        return jobs_parser

    def remove_rerun_only_jobs(self, notransitive=False):
        """
        Removes all jobs to be run only in reruns
        """
        flag = False
        for job in set(self._job_list):
            if job.rerun_only:
                self._remove_job(job)
                flag = True

        if flag:
            self.update_genealogy(notransitive=notransitive)
        del self._dic_jobs
