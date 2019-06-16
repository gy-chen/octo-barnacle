export const START_MARK_REQUEST = 'START_MARK_REQUEST';
export const UPDATE_MARK_FORM = 'UPDATE_MARK_FORM';
export const UPDATE_MARK_RESULT = 'UPDATE_MARK_RESULT';
export const MARK_REQUEST_DONE = 'MARK_REQUEST_DONE';

export enum MarkType {
    OK = "OK",
    EMPTY = "EMPTY",
    MISLABEL = "MISLABEL",
    NOT_ANIME = "NOT_ANIME",
    STRANGE_MEME = "STRANGE_MEME",
    OTHER = "OTHER"
}

export enum MarkResult {
    SUCCESS,
    INVALID_PARAMETERS,
    RESOURCE_EXPIRES,
    STICKETSET_NOT_FOUND,
    OTHER
}

export interface StartMarkRequestAction {
    type: typeof START_MARK_REQUEST;
};

export interface UpdateMarkFormAction {
    type: typeof UPDATE_MARK_FORM,
    payload: {
        stickersetName: string,
        mark: MarkType
    }
}

export interface UpdateMarkResultAction {
    type: typeof UPDATE_MARK_RESULT;
    payload: {
        stickersetName: string,
        result: MarkResult
    };
}

export interface MarkRequestDoneAction {
    type: typeof MARK_REQUEST_DONE
}

export type MarkActionTypes = StartMarkRequestAction | UpdateMarkFormAction | UpdateMarkResultAction | MarkRequestDoneAction;