import os
import typing

from datetime import date, datetime
from typing import Optional
from uuid import UUID

import attr

from dbnd._core.configuration.environ_config import (
    DBND_PARENT_TASK_RUN_ATTEMPT_UID,
    DBND_PARENT_TASK_RUN_UID,
    DBND_ROOT_RUN_TRACKER_URL,
    DBND_ROOT_RUN_UID,
    SCHEDULED_DAG_RUN_ID_ENV,
    SCHEDULED_DATE_ENV,
    SCHEDULED_JOB_UID_ENV,
)
from dbnd._core.constants import RunState, _DbndDataClass
from dbnd._core.current import try_get_current_task_run, try_get_databand_run
from dbnd._core.utils import timezone


if typing.TYPE_CHECKING:
    from dbnd._core.run.databand_run import DatabandRun


@attr.s
class RunInfo(_DbndDataClass):
    run_uid = attr.ib()  # type: UUID

    job_name = attr.ib()  # type: str
    user = attr.ib()  # type: str

    name = attr.ib()  # type: str
    description = attr.ib()  # type: str

    state = attr.ib()  # type: RunState
    start_time = attr.ib()  # type: datetime
    end_time = attr.ib()  # type: Optional[datetime]

    # deprecate
    dag_id = attr.ib()  # type: str
    execution_date = attr.ib()  # type: datetime
    cmd_name = attr.ib()  # type: Optional[str]

    # task attributes
    target_date = attr.ib()  # type: Optional[date]
    version = attr.ib()  # type: Optional[str]

    driver_name = attr.ib()  # type: str
    is_archived = attr.ib()  # type: bool
    env_name = attr.ib()  # type: Optional[str]
    cloud_type = attr.ib()  # type: str
    trigger = attr.ib()  # type: str

    # runs from same run group will have same root_run_uid
    root_run = attr.ib()  # type: RootRunInfo
    scheduled_run = attr.ib()  # type: Optional[ScheduledRunInfo]

    sends_heartbeat = attr.ib()  # type: bool
    task_executor = attr.ib(default=None)  # type: str


@attr.s
class ScheduledRunInfo(_DbndDataClass):
    scheduled_job_uid = attr.ib(default=None)  # type: Optional[UUID]
    scheduled_date = attr.ib(default=None)  # type: datetime
    scheduled_job_dag_run_id = attr.ib(default=None)  # type: int
    # for manual association with scheduled job from dbnd run cli
    scheduled_job_name = attr.ib(default=None)  # type: Optional[str]

    @classmethod
    def from_env(cls, run_uid):
        scheduled_job_uid = os.environ.get(SCHEDULED_JOB_UID_ENV, None)
        if not scheduled_job_uid:
            # there is no scheduled job
            return
        scheduled_date = os.environ.get(SCHEDULED_DATE_ENV, None)
        if scheduled_date:
            scheduled_date = timezone.parse(scheduled_date)
        scheduled_date = scheduled_date
        scheduled_job_dag_run_id = os.environ.get(SCHEDULED_DAG_RUN_ID_ENV, None)
        return cls(
            scheduled_date=scheduled_date,
            scheduled_job_dag_run_id=scheduled_job_dag_run_id,
            scheduled_job_uid=scheduled_job_uid,
        )


@attr.s
class RootRunInfo(_DbndDataClass):
    root_run_uid = attr.ib(default=None)  # type: UUID

    root_run_url = attr.ib(default=None)  # type: Optional[str]
    root_task_run_uid = attr.ib(default=None)  # type: Optional[UUID]
    root_task_run_attempt_uid = attr.ib(default=None)  # type: Optional[UUID]

    @classmethod
    def from_env(cls, current_run):
        # type: (DatabandRun) -> RootRunInfo
        parent_run = try_get_databand_run()
        if parent_run:
            # take from parent
            root_run_info = parent_run.root_run_info
            # update parent run info if required
            root_task_run = try_get_current_task_run()
            if root_task_run:
                root_run_info = attr.evolve(
                    root_run_info,
                    root_task_run_uid=root_task_run.task_run_uid,
                    root_task_run_attempt_uid=root_task_run.task_run_attempt_uid,
                )

            return root_run_info

        # take from env
        root_run_uid = os.environ.get(DBND_ROOT_RUN_UID)
        root_run_url = os.environ.get(DBND_ROOT_RUN_TRACKER_URL)
        root_task_run_uid = os.environ.get(DBND_PARENT_TASK_RUN_UID)
        root_task_run_attempt_uid = os.environ.get(DBND_PARENT_TASK_RUN_ATTEMPT_UID)

        if not root_run_uid:
            # current run is the main run
            root_run_uid = current_run.run_uid
            root_run_url = current_run.tracker.run_url

        return cls(
            root_run_uid=root_run_uid,
            root_run_url=root_run_url,
            root_task_run_uid=root_task_run_uid,
            root_task_run_attempt_uid=root_task_run_attempt_uid,
        )
