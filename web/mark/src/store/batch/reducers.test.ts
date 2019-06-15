import { _startBatchRequestAction, _batchRequestDoneAction } from './actions';
import { reducer as batchReducer } from './reducers';
import { BatchStickersetData } from './types';
import { AppState } from '../';

describe('test batch reducer', () => {
    it('test StartBatchRequestAction', () => {
        const mockState: AppState['batch'] = {
            isBatchRequesting: false,
            stickersets: [],
            stickers: {},
            resources: {}
        };

        expect(batchReducer(mockState, _startBatchRequestAction())).toEqual({
            isBatchRequesting: true,
            stickersets: [],
            stickers: {},
            resources: {}
        });
    });

    it('test BatchRequestDoneAction', () => {
        const mockState: AppState['batch'] = {
            isBatchRequesting: true,
            stickersets: [],
            stickers: {},
            resources: {}
        };

        const batchData: BatchStickersetData[] = [
            {
                stickerset: {
                    stickersetName: 'stickerset1',
                    title: 'StickerSet1'
                },
                resource: 'resource1',
                stickers: [
                    {
                        fileId: 'stickerset1sticker1',
                        emoji: 'stickerset1emoji1'
                    },
                    {
                        fileId: 'stickerset1sticker2',
                        emoji: 'stickerset1emoji2'
                    }
                ]
            },
            {
                stickerset: {
                    stickersetName: 'stickerset2',
                    title: 'StickerSet2'
                },
                resource: 'resource2',
                stickers: [
                    {
                        fileId: 'stickerset2sticker1',
                        emoji: 'stickerset2emoji1'
                    },
                    {
                        fileId: 'stickerset2sticker2',
                        emoji: 'stickerset2emoji2'
                    }
                ]
            }
        ];

        expect(batchReducer(mockState, _batchRequestDoneAction(batchData))).toEqual({
            isBatchRequesting: false,
            stickersets: [
                {
                    stickersetName: 'stickerset1',
                    title: 'StickerSet1'
                },
                {
                    stickersetName: 'stickerset2',
                    title: 'StickerSet2'
                }
            ],
            stickers: {
                stickerset1: [
                    {
                        fileId: 'stickerset1sticker1',
                        emoji: 'stickerset1emoji1'
                    },
                    {
                        fileId: 'stickerset1sticker2',
                        emoji: 'stickerset1emoji2'
                    }
                ],
                stickerset2: [
                    {
                        fileId: 'stickerset2sticker1',
                        emoji: 'stickerset2emoji1'
                    },
                    {
                        fileId: 'stickerset2sticker2',
                        emoji: 'stickerset2emoji2'
                    }
                ]
            },
            resources: {
                stickerset1: 'resource1',
                stickerset2: 'resource2'
            }
        });
    });
});