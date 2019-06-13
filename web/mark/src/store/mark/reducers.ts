
import {
    MARK_REQUEST,
    UPDATE_MARK_RESULT,
    MARK_REQUEST_DONE,
    MarkResult,
    MarkActionTypes
} from './types';


interface MarkState {
    isMarkRequesting: boolean;
    markResults: { [stickerset_name: string]: MarkResult };
}

const initialState: MarkState = {
    isMarkRequesting: false,
    markResults: {}
};

export const reducer = (state = initialState, action: MarkActionTypes): MarkState => {
    switch (action.type) {
        case MARK_REQUEST:
            return {
                isMarkRequesting: true,
                markResults: {}
            };
        case UPDATE_MARK_RESULT:
            return {
                isMarkRequesting: state.isMarkRequesting,
                markResults: {
                    ...state.markResults,
                    [action.payload.stickersetName]: action.payload.result
                }
            };
        case MARK_REQUEST_DONE:
            return {
                ...state,
                isMarkRequesting: false,
            };
        default:
            return state;
    }
};