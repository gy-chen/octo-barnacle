import {
    START_BATCH_REQUEST,
    BATCH_REQUEST_DONE,
    BatchStickeretData,
    BatchActionTypes
} from './types';


interface BatchState {
    data: BatchStickeretData[];
    isBatchRequesting: boolean;
}

const initialState: BatchState = {
    data: [],
    isBatchRequesting: false,
};

export const reducer = (state = initialState, action: BatchActionTypes): BatchState => {
    switch (action.type) {
        case START_BATCH_REQUEST:
            return {
                data: [],
                isBatchRequesting: true
            };
        case BATCH_REQUEST_DONE:
            return {
                data: action.payload,
                isBatchRequesting: false
            };
        default:
            return state;
    }
};