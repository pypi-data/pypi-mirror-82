import abc
import datetime
from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from lime_etl.adapters import timestamp_adapter
from lime_etl.domain import batch, value_objects


class BatchRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, new_batch: batch.Batch, /) -> batch.Batch:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_old_entries(self, days_to_keep: value_objects.DaysToKeep, /) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_batch_by_id(
        self, batch_id: value_objects.UniqueId, /
    ) -> Optional[batch.Batch]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_latest(self) -> Optional[batch.Batch]:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, batch_to_update: batch.Batch) -> batch.Batch:
        raise NotImplementedError


class SqlAlchemyBatchRepository(BatchRepository):
    def __init__(
        self, session: Session, ts_adapter: timestamp_adapter.TimestampAdapter
    ):
        self._session = session
        self._ts_adapter = ts_adapter
        super().__init__()

    def add(self, new_batch: batch.Batch) -> batch.Batch:
        dto = new_batch.to_dto()
        self._session.add(dto)
        return new_batch

    def delete_old_entries(self, days_to_keep: value_objects.DaysToKeep, /) -> int:
        ts = self._ts_adapter.now().value
        cutoff: datetime.datetime = ts - datetime.timedelta(days=days_to_keep.value)
        # We need to delete batches one by one to trigger cascade deletes, a bulk update will
        # not trigger them, and we don't want to rely on specific database implementations, so
        # we cannot use ondelete='CASCADE' on the foreign key columns.
        batches: List[batch.BatchDTO] = (
            self._session.query(batch.BatchDTO).filter(batch.BatchDTO.ts < cutoff).all()
        )
        for b in batches:
            self._session.delete(b)
        return len(batches)

    def get_batch_by_id(
        self, batch_id: value_objects.UniqueId, /
    ) -> Optional[batch.Batch]:
        result: Optional[batch.BatchDTO] = (
            self._session.query(batch.BatchDTO)
            .filter(batch.BatchDTO.id == batch_id.value)
            .first()
        )
        if result is None:
            return None
        else:
            return result.to_domain()

    def get_latest(self) -> Optional[batch.Batch]:
        result: Optional[batch.BatchDTO] = (
            self._session.query(batch.BatchDTO)
            .order_by(desc(batch.BatchDTO.ts))  # type: ignore
            .first()
        )
        if result is None:
            return None
        else:
            return result.to_domain()

    def update(self, batch_to_update: batch.Batch, /) -> batch.Batch:
        dto = batch_to_update.to_dto()
        self._session.merge(dto)
        return batch_to_update
