
export const START_BATCH_REQUEST = 'START_BATCH_REQUEST';
export const BATCH_REQUEST_DONE = 'BATCH_REQUEST_DONE';

export interface Stickerset {
    stickersetName: string;
    title: string;
}

export interface Sticker {
    fileId: string;
    emoji: string;
}

export interface BatchStickersetData {
    stickerset: Stickerset;
    resource: string;
    stickers: Sticker[];
}

export interface StartBatchRequestAction {
    type: typeof START_BATCH_REQUEST;
}

export interface BatchRequestDoneAction {
    type: typeof BATCH_REQUEST_DONE;
    payload: BatchStickersetData[]
}

export type BatchActionTypes = StartBatchRequestAction | BatchRequestDoneAction;