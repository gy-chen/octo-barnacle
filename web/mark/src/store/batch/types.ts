
export const START_BATCH_REQUEST = 'START_BATCH_REQUEST';
export const BATCH_REQUEST_DONE = 'BATCH_REQUEST_DONE';

export interface BatchStickeretData {
    // TODO
}

export interface StartBatchRequestAction {
    type: typeof START_BATCH_REQUEST;
}

export interface BatchRequestDoneAction {
    type: typeof BATCH_REQUEST_DONE;
    payload: BatchStickeretData[]
}

export type BatchActionTypes = StartBatchRequestAction | BatchRequestDoneAction;