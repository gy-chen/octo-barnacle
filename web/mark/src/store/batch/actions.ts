import {
    START_BATCH_REQUEST,
    BATCH_REQUEST_DONE,
    StartBatchRequestAction,
    BatchRequestDoneAction,
    BatchStickeretData
} from './types';

// TODO make this as a thunk action
export const startBatchRequestAction = (): StartBatchRequestAction => ({
    type: START_BATCH_REQUEST
});

export const batchRequestDoneAction = (batchData: BatchStickeretData[]): BatchRequestDoneAction => ({
    type: BATCH_REQUEST_DONE,
    payload: batchData
});