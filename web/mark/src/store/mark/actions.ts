import { ThunkAction } from 'redux-thunk';
import {
    START_MARK_REQUEST,
    UPDATE_MARK_FORM,
    UPDATE_MARK_RESULT,
    MARK_REQUEST_DONE,
    StartMarkRequestAction,
    UpdateMarkFormAction,
    UpdateMarkResultAction,
    MarkRequestDoneAction,
    MarkType,
    MarkResult,
    MarkActionTypes
} from './types';
import {
    AppState
} from '..';

type ThunkResult<R> = ThunkAction<R, AppState, undefined, MarkActionTypes>;

export const _startMarkRequestAction = (): StartMarkRequestAction => ({
    type: START_MARK_REQUEST
});

export const _updateMarkResultAction = (stickersetName: string, result: MarkResult): UpdateMarkResultAction => ({
    type: UPDATE_MARK_RESULT,
    payload: {
        stickersetName,
        result
    }
});

export const _markRequestDoneAction = (): MarkRequestDoneAction => ({
    type: MARK_REQUEST_DONE
});

export const updateMarkFormAction = (stickersetName: string, mark: MarkType): UpdateMarkFormAction => ({
    type: UPDATE_MARK_FORM,
    payload: {
        stickersetName,
        mark
    }
});

export const startMarkRequestAction = (markRequest: (stickersetName: string, resource: string, mark: MarkType) => Promise<MarkResult>): ThunkResult<void> => {
    return async (dispatch, getState) => {
        dispatch(_startMarkRequestAction());
        const { mark: { markForms, markResults }, batch: { resources } } = getState();
        for (const stickersetName of Object.keys(markForms)) {
            if (markResults[stickersetName] !== undefined) {
                continue;
            }
            const resource = resources[stickersetName];
            const markResult = await markRequest(stickersetName, resource, markForms[stickersetName]);
            dispatch(_updateMarkResultAction(stickersetName, markResult));
        }
        dispatch(_markRequestDoneAction());
    };
};
