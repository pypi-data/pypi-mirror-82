from __future__ import annotations

import abc
from typing import Any

from sqlalchemy.orm import sessionmaker

from lime_etl.adapters import (
    batch_log_repository,
    batch_repository,
    email_adapter,
    job_repository,
    job_log_repository,
    timestamp_adapter,
)


class UnitOfWork(abc.ABC):
    ts_adapter: timestamp_adapter.TimestampAdapter
    batches: batch_repository.BatchRepository
    jobs: job_repository.JobRepository
    batch_log: batch_log_repository.BatchLogRepository
    job_log: job_log_repository.JobLogRepository
    emailer: email_adapter.EmailAdapter

    def __enter__(self) -> UnitOfWork:
        return self

    def __exit__(self, *args: Any) -> None:
        self.rollback()

    @abc.abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class DefaultUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory
        self.ts_adapter = timestamp_adapter.LocalTimestampAdapter()

    def __enter__(self) -> UnitOfWork:
        self._session = self._session_factory()
        self.batches = batch_repository.SqlAlchemyBatchRepository(
            session=self._session,
            ts_adapter=self.ts_adapter,
        )
        self.jobs = job_repository.SqlAlchemyJobRepository(
            session=self._session,
            ts_adapter=self.ts_adapter,
        )
        self.batch_log = batch_log_repository.SqlAlchemyBatchLogRepository(
            session=self._session,
            ts_adapter=self.ts_adapter,
        )
        self.job_log = job_log_repository.SqlAlchemyJobLogRepository(
            session=self._session,
            ts_adapter=self.ts_adapter,
        )
        return super().__enter__()

    def __exit__(self, *args: Any) -> None:
        super().__exit__(*args)
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
