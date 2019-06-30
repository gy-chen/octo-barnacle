import * as React from 'react';
import * as styles from './markStickersetForm.css';
import StickerComponent_ from '../Sticker';
import { Stickerset, Sticker } from '../../store/batch/types';
import { MarkType, MarkResult } from '../../store/mark/types';
import { getErrorMessage } from './utils';

interface Props {
    stickerset: Stickerset;
    stickers: Sticker[];
    markResult?: MarkResult;
    selectedMarkType?: MarkType;
    onMarkTypeChange?: (stickersetName: string, markType: MarkType) => any;
    StickerComponent?: (props: { sticker: Sticker }) => JSX.Element;
}

const _getErrorClassName = (markResult?: MarkResult): string => {
    switch (markResult) {
        case MarkResult.SUCCESS:
            return styles.resultSuccess;
        case MarkResult.INVALID_PARAMETERS:
            return styles.resultInvalidParameters;
        case MarkResult.RESOURCE_EXPIRES:
            return styles.resultResourceExpires;
        case MarkResult.STICKETSET_NOT_FOUND:
            return styles.resultStickersetNotFound;
        case MarkResult.OTHER:
            return styles.resultOther;
        default:
            return "";
    }
}

class MarkStickersetForm extends React.Component<Props> {

    _renderRadioInput(label: string, name: string, markType: MarkType, markResult?: MarkResult) {
        const { selectedMarkType, onMarkTypeChange } = this.props;

        return (
            <label>
                <input
                    type="radio"
                    value={markType}
                    name={name}
                    checked={markType === selectedMarkType}
                    disabled={!!markResult}
                    onChange={() => onMarkTypeChange && onMarkTypeChange(name, markType)}
                />
                <span>{label}</span>
            </label>
        );
    }

    _renderErrorMessage(markResult?: MarkResult) {
        if (!markResult) {
            return;
        }
        return (
            <div className={styles.errorMessage}>
                {getErrorMessage(markResult)}
            </div>
        );
    }

    render() {
        const { stickerset, stickers, StickerComponent = StickerComponent_, markResult } = this.props;

        return (
            <div className={`${styles.container} ${_getErrorClassName(markResult)}`}>
                <div className={styles.imageSlideContainer}>
                    {stickers.map(sticker => <StickerComponent sticker={sticker} />)}
                </div>
                <div className={styles.optionsContainer}>
                    {this._renderRadioInput('OK', stickerset.name, MarkType.OK, markResult)}
                    {this._renderRadioInput('MISLABEL', stickerset.name, MarkType.MISLABEL, markResult)}
                    {this._renderRadioInput('NOT ANIME', stickerset.name, MarkType.NOT_ANIME, markResult)}
                    {this._renderRadioInput('STRANGE MEME', stickerset.name, MarkType.STRANGE_MEME, markResult)}
                    {this._renderRadioInput('EMPTY', stickerset.name, MarkType.EMPTY, markResult)}
                    {this._renderRadioInput('OTHER', stickerset.name, MarkType.OTHER, markResult)}
                </div>
                {this._renderErrorMessage(markResult)}
            </div>
        );
    }
}

export default MarkStickersetForm;