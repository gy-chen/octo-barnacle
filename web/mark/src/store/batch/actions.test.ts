import { startBatchRequestAction } from './actions';
import {
    START_BATCH_REQUEST,
    BATCH_REQUEST_DONE
} from './types';

describe('startBatchRequestAction', () => {
    it('expect startBatchRequestAction dispath correct actions', async () => {
        const mockDispatch = jest.fn();
        const mockGetState = jest.fn();
        const mockBatchRequest = jest.fn(() => new Promise<[]>(r => r([])));

        const startBatchRequestThunk = startBatchRequestAction(mockBatchRequest);
        await startBatchRequestThunk(mockDispatch, mockGetState, undefined);

        expect(mockDispatch.mock.calls.length).toBe(2);
        expect(mockDispatch.mock.calls[0][0]).toEqual({
            type: START_BATCH_REQUEST
        });
        expect(mockDispatch.mock.calls[1][0]).toEqual({
            type: BATCH_REQUEST_DONE,
            payload: []
        });
    });
});