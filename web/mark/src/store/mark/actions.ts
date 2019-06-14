import {
    START_MARK_REQUEST,
    UPDATE_MARK_RESULT,
    MARK_REQUEST_DONE,
    StartMarkRequestAction,
    UpdateMarkResultAction,
    MarkRequestDoneAction,
    MarkResult
} from './types';

// TODO turn this into thunk action
export const startMarkRequestAction = (): StartMarkRequestAction => ({
    type: START_MARK_REQUEST
});

export const updateMarkResultAction = (stickersetName: string, result: MarkResult): UpdateMarkResultAction => ({
    type: UPDATE_MARK_RESULT,
    payload: {
        stickersetName,
        result
    }
});

export const markRequestDoneAction = (): MarkRequestDoneAction => ({
    type: MARK_REQUEST_DONE
});