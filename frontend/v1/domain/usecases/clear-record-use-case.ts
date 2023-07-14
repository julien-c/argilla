import { IEventDispatcher } from "@codescouts/events";
import { RecordResponseUpdated } from "../events/RecordResponseUpdated";
import { Record } from "@/v1/domain/entities/record/Record";
import { RecordRepository } from "@/v1/infrastructure/repositories";

export class ClearRecordUseCase {
  constructor(
    private readonly recordRepository: RecordRepository,
    private readonly eventDispatcher: IEventDispatcher
  ) {}

  async execute(record: Record) {
    if (record.answer) {
      await this.recordRepository.deleteRecordResponse(record.answer);

      this.eventDispatcher.dispatch(new RecordResponseUpdated(record));
    }

    record.clear();
  }
}
