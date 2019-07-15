import * as React from 'react';
import { Sticker } from '../../store/batch/types';
import * as styles from './sticker.css';

interface Props {
    sticker: Sticker;
    toStickerImageUrl?: (stickerFileId: Sticker['fileId']) => string;
}

const toStickerImageUrl_ = (stickerFileId: Sticker['fileId']) => new URL(`file/${stickerFileId}`, process.env.OCTO_BARNACLE_FILE_BASEURL).href;

class StickerComponent extends React.Component<Props> {

    private _imgRef = React.createRef<HTMLImageElement>();

    componentDidMount() {
        const { sticker, toStickerImageUrl = toStickerImageUrl_ } = this.props;

        if (this._imgRef.current) {
            this._imgRef.current.style.setProperty('--stickerImageUrl', `url(${toStickerImageUrl(sticker.fileId)}`);
        }
    }

    render() {
        const { sticker } = this.props;

        return (
            <div className={styles.container}>
                <div className={styles.stickerImage} ref={this._imgRef} />
                <p className={styles.emoji}>{sticker.emoji}</p>
            </div>
        );
    }
}


export default StickerComponent;