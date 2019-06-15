import { ThunkAction } from 'redux-thunk';
import {
    START_BATCH_REQUEST,
    BATCH_REQUEST_DONE,
    StartBatchRequestAction,
    BatchRequestDoneAction,
    BatchStickersetData,
    BatchActionTypes
} from './types';
import {
    AppState
} from '../';

type ThunkResult<R> = ThunkAction<R, AppState, undefined, BatchActionTypes>;

export const _startBatchRequestAction = (): StartBatchRequestAction => ({
    type: START_BATCH_REQUEST
});

export const _batchRequestDoneAction = (batchData: BatchStickersetData[]): BatchRequestDoneAction => ({
    type: BATCH_REQUEST_DONE,
    payload: batchData
});

export const startBatchRequestAction = (batchRequest: () => Promise<BatchStickersetData[]>): ThunkResult<void> => {
    return async dispatch => {
        dispatch(_startBatchRequestAction());
        const batchData = await batchRequest();
        dispatch(_batchRequestDoneAction(batchData));
    };
}
