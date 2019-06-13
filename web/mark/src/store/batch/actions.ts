import {
    UPDATE_BATCH_DATA,
    NEXT_BATCH_REQUEST,
    BATCH_REQUEST_DONE,
    UpdateBatchAction,
    NextBatchRequestAction,
    BatchRequestDoneAction,
    BatchStickeretData
} from './types';

export const updateBatchDataAction = (batchData: BatchStickeretData[]): UpdateBatchAction => ({
    type: UPDATE_BATCH_DATA,
    payload: batchData
});

// TODO make this as a thunk action
export const nextBatchRequestAction = (): NextBatchRequestAction => ({
    type: NEXT_BATCH_REQUEST
});

export const batchRequestDoneAction = (): BatchRequestDoneAction => ({
    type: BATCH_REQUEST_DONE
});