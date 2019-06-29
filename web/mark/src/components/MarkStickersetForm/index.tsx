import { h, Component } from 'preact';
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

class MarkStickerForm extends Component<Props> {

    _renderRadioInput(label: string, name: string, markType: MarkType) {
        const { selectedMarkType, onMarkTypeChange } = this.props;

        return (
            <label>
                <input
                    type="radio"
                    value={markType}
                    name={name}
                    checked={markType === selectedMarkType}
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
                    {this._renderRadioInput('OK', stickerset.stickersetName, MarkType.OK)}
                    {this._renderRadioInput('MISLABEL', stickerset.stickersetName, MarkType.MISLABEL)}
                    {this._renderRadioInput('NOT ANIME', stickerset.stickersetName, MarkType.NOT_ANIME)}
                    {this._renderRadioInput('STRANGE MEME', stickerset.stickersetName, MarkType.STRANGE_MEME)}
                    {this._renderRadioInput('EMPTY', stickerset.stickersetName, MarkType.EMPTY)}
                    {this._renderRadioInput('OTHER', stickerset.stickersetName, MarkType.OTHER)}
                </div>
                {this._renderErrorMessage(markResult)}
            </div>
        );
    }
}

export default MarkStickerForm;