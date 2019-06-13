import {
    NEXT_BATCH_REQUEST,
    UPDATE_BATCH_DATA,
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
        case NEXT_BATCH_REQUEST:
            return {
                data: [],
                isBatchRequesting: true
            };
        case UPDATE_BATCH_DATA:
            return {
                ...state,
                data: action.payload,
            };
        case BATCH_REQUEST_DONE:
            return {
                ...state,
                isBatchRequesting: false
            };
        default:
            return state;
    }
};