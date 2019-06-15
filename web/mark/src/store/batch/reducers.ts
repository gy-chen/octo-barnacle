import {
    START_BATCH_REQUEST,
    BATCH_REQUEST_DONE,
    BatchStickersetData,
    Sticker,
    Stickerset,
    BatchActionTypes
} from './types';


interface BatchState {
    stickersets: Stickerset[],
    stickers: { [stickersetName: string]: Sticker[] };
    resources: { [stickersetName: string]: string };
    isBatchRequesting: boolean;
}

const initialState: BatchState = {
    stickersets: [],
    stickers: {},
    resources: {},
    isBatchRequesting: false,
};

export const reducer = (state = initialState, action: BatchActionTypes): BatchState => {
    switch (action.type) {
        case START_BATCH_REQUEST:
            return {
                stickersets: [],
                resources: {},
                stickers: {},
                isBatchRequesting: true
            };
        case BATCH_REQUEST_DONE:
            return {
                stickersets: action.payload.map(d => d.stickerset),
                stickers: _extractStickers(action.payload),
                resources: _extractResources(action.payload),
                isBatchRequesting: false
            };
        default:
            return state;
    }
};

const _extractResources = (batchStickersetsData: BatchStickersetData[]): BatchState["resources"] => {
    const resources: BatchState["resources"] = {};
    for (const stickersetData of batchStickersetsData) {
        resources[stickersetData["stickerset"]["stickersetName"]] = stickersetData["resource"];
    }
    return resources;
};

const _extractStickers = (batchStickersetsData: BatchStickersetData[]): BatchState["stickers"] => {
    const stickers: BatchState["stickers"] = {};
    for (const stickersetData of batchStickersetsData) {
        stickers[stickersetData["stickerset"]["stickersetName"]] = stickersetData["stickers"];
    }
    return stickers;
}