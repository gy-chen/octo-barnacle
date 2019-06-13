
export const UPDATE_BATCH_DATA = 'UPDATE_BATCH_DATA';
export const NEXT_BATCH_REQUEST = 'NEXT_BATCH_REQUEST';
export const BATCH_REQUEST_DONE = 'BATCH_REQUEST_DONE';

export interface BatchStickeretData {
    // TODO
}

export interface UpdateBatchAction {
    type: typeof UPDATE_BATCH_DATA;
    payload: BatchStickeretData[]
}

export interface NextBatchRequestAction {
    type: typeof NEXT_BATCH_REQUEST;
}

export interface BatchRequestDoneAction {
    type: typeof BATCH_REQUEST_DONE;
}

export type BatchActionTypes = UpdateBatchAction | NextBatchRequestAction | BatchRequestDoneAction;