import { startMarkRequestAction } from './actions';
import { AppState } from '../';
import {
    START_MARK_REQUEST,
    UPDATE_MARK_RESULT,
    MARK_REQUEST_DONE,
    MarkType,
    MarkResult
} from './types';

describe('test startMarkRequestAction', () => {
    it('expect dispatch correct actions', async () => {
        const mockDispatch = jest.fn();
        const mockState: AppState = {
            batch: {
                stickersets: [],
                stickers: {},
                resources: {
                    stickerset1: 'resource1',
                    stickerset2: 'resource2',
                    stickerset3: 'resource3'
                },
                isBatchRequesting: false,
            },
            mark: {
                isMarkRequesting: false,
                markResults: {
                    stickerset3: MarkResult.SUCCESS
                },
                markForms: {
                    stickerset1: MarkType.OK,
                    stickerset2: MarkType.MISLABEL
                }
            }
        };
        const mockGetState = jest.fn(() => mockState);
        const mockMarkRequest = jest.fn(() => new Promise<MarkResult>(r => r(MarkResult.SUCCESS)));

        const startMarkRequestThunk = startMarkRequestAction(mockMarkRequest);
        await startMarkRequestThunk(mockDispatch, mockGetState, undefined);

        expect(mockDispatch.mock.calls.length).toBe(4);
        expect(mockDispatch.mock.calls[0][0]).toEqual({
            type: START_MARK_REQUEST
        });
        expect(mockDispatch.mock.calls[1][0]).toEqual({
            type: UPDATE_MARK_RESULT,
            payload: {
                stickersetName: 'stickerset1',
                result: MarkResult.SUCCESS
            }
        });
        expect(mockDispatch.mock.calls[2][0]).toEqual({
            type: UPDATE_MARK_RESULT,
            payload: {
                stickersetName: 'stickerset2',
                result: MarkResult.SUCCESS
            }
        });
        expect(mockDispatch.mock.calls[3][0]).toEqual({
            type: MARK_REQUEST_DONE
        });

        expect(mockMarkRequest.mock.calls.length).toBe(2);
        expect(mockMarkRequest.mock.calls[0]).toEqual(['stickerset1', 'resource1', MarkType.OK]);
        expect(mockMarkRequest.mock.calls[1]).toEqual(['stickerset2', 'resource2', MarkType.MISLABEL]);
    });
});