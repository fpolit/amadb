#!/usr/bin/env python3

from __future__ import annotations
from collections.abc import Iterable

from amadb.dbmanager import BaseDBManager

# protobuf messages
from amadb.proto.job_pb2 import Job
from amadb.proto.utils_pb2 import ReturnStatus
from amadb.proto.requests_pb2 import JobFilterRequest

class JobDBManager(BaseDBManager):
    @classmethod
    def register_job(cls, Job) -> ReturnStatus:
        pass

    @classmethod
    def get_all_job(cls) -> Iterable[Job]:
        pass

    @classmethod
    def get_job_info(cls) -> Job:
        pass

    @classmethod
    def filter_jobs(cls,  jobfilter: JobFilterRequest) -> Iterable[Job]:
        pass
