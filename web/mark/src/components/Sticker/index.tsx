import * as React from 'react';
import { Sticker } from '../../store/batch/types';
import * as styles from './sticker.css';

interface Props {
    sticker: Sticker;
    toStickerImageUrl?: (stickerFileId: Sticker['fileId']) => string;
}

const toStickerImageUrl_ = (stickerFileId: Sticker['fileId']) => `${process.env.OCTO_BARNACLE_MARK_BASEURL}/file/${stickerFileId}`;

const Sticker = (props: Props) => {
    const { sticker, toStickerImageUrl = toStickerImageUrl_ } = props;

    return (
        <div className={styles.container}>
            <img className={styles.stickerImage} src={toStickerImageUrl(sticker.fileId)} />
            <p className={styles.emoji}>{sticker.emoji}</p>
        </div>
    );
};

export default Sticker;