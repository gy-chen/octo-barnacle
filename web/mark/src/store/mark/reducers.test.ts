
import {
    _startMarkRequestAction,
    _updateMarkResultAction,
    _markRequestDoneAction,
    updateMarkFormAction
} from './actions';
import { reducer as markReducer } from './reducers';
import {
    MarkType,
    MarkResult
} from './types';
import { AppState } from '../';

describe('test mark reducer', () => {
    it('test StartMarkRequestAction', () => {
        const mockState: AppState['mark'] = {
            isMarkRequesting: false,
            markResults: {},
            markForms: {}
        };

        expect(markReducer(mockState, _startMarkRequestAction())).toEqual({
            isMarkRequesting: true,
            markResults: {},
            markForms: {}
        });
    });

    it('test UpdateMarkFormAction', () => {
        const mockState: AppState['mark'] = {
            isMarkRequesting: true,
            markResults: {},
            markForms: {}
        };

        expect(markReducer(mockState, updateMarkFormAction('stickerset1', MarkType.OK))).toEqual({
            isMarkRequesting: true,
            markResults: {},
            markForms: {
                stickerset1: MarkType.OK
            }
        })
    });

    it('test UpdateMarkResultAction', () => {
        const mockState: AppState['mark'] = {
            isMarkRequesting: true,
            markResults: {},
            markForms: {}
        };

        expect(markReducer(mockState, _updateMarkResultAction('stickerset1', MarkResult.SUCCESS))).toEqual({
            isMarkRequesting: true,
            markResults: {
                stickerset1: MarkResult.SUCCESS
            },
            markForms: {}
        });
    });

    it('test MarkRequestDoneAction', () => {
        const mockState: AppState['mark'] = {
            isMarkRequesting: true,
            markResults: {},
            markForms: {}
        };

        expect(markReducer(mockState, _markRequestDoneAction())).toEqual({
            isMarkRequesting: false,
            markResults: {},
            markForms: {}
        });
    })
});