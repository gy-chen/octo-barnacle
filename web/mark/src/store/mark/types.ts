export const START_MARK_REQUEST = 'START_MARK_REQUEST';
export const UPDATE_MARK_RESULT = 'UPDATE_MARK_RESULT';
export const MARK_REQUEST_DONE = 'MARK_REQUEST_DONE';

// TODO
export enum MarkResult {

}

export interface StartMarkRequestAction {
    type: typeof START_MARK_REQUEST;
};

export interface UpdateMarkResultAction {
    type: typeof UPDATE_MARK_RESULT;
    payload: {
        stickersetName: string;
        result: MarkResult;
    };
}

export interface MarkRequestDoneAction {
    type: typeof MARK_REQUEST_DONE
}

export type MarkActionTypes = StartMarkRequestAction | UpdateMarkResultAction | MarkRequestDoneAction;