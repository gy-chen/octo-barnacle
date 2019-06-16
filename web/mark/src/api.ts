import axios from 'axios';
import { BatchStickersetData } from './store/batch/types';
import { MarkType, MarkResult } from './store/mark/types';

const client = axios.create({
    baseURL: process.env.OCTO_BARNACLE_MARK_BASEURL
});

export const nextBatch = (): Promise<BatchStickersetData[]> => {
    return client.post('/stickerset/mark/next_batch')
        .then(res => res.data);
};

export const mark = (stickersetName: string, resource: string, mark: MarkType): Promise<MarkResult> => {
    return client.post(
        `/stickerset/${stickersetName}/mark`, {
            resource,
            mark
        })
        .then(() => MarkResult.SUCCESS)
        .catch(res => {
            switch (res.status) {
                case 400:
                    return MarkResult.INVALID_PARAMETERS;
                case 401:
                    return MarkResult.RESOURCE_EXPIRES;
                case 404:
                    return MarkResult.STICKETSET_NOT_FOUND;
                default:
                    return MarkResult.OTHER;
            }
        });
};