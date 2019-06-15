
import {
    START_MARK_REQUEST,
    UPDATE_MARK_FORM,
    UPDATE_MARK_RESULT,
    MARK_REQUEST_DONE,
    MarkResult,
    MarkActionTypes,
    MarkType
} from './types';


interface MarkState {
    isMarkRequesting: boolean;
    markResults: { [stickersetName: string]: MarkResult };
    markForms: { [stickersetName: string]: MarkType };
}

const initialState: MarkState = {
    isMarkRequesting: false,
    markResults: {},
    markForms: {}
};

export const reducer = (state = initialState, action: MarkActionTypes): MarkState => {
    switch (action.type) {
        case START_MARK_REQUEST:
            return {
                isMarkRequesting: true,
                markResults: {},
                markForms: {}
            };
        case UPDATE_MARK_FORM:
            return {
                ...state,
                markForms: {
                    ...state.markForms,
                    [action.payload.stickersetName]: action.payload.mark
                }
            };
        case UPDATE_MARK_RESULT:
            return {
                ...state,
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