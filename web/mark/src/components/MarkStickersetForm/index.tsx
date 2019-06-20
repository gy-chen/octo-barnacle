import { h, Component } from 'preact';
import * as styles from './markStickersetForm.css';
import StickerComponent_ from '../Sticker';
import { Stickerset, Sticker } from '../../store/batch/types';
import { MarkType } from '../../store/mark/types';

interface Props {
    stickerset: Stickerset;
    stickers: Sticker[];
    selectedMarkType?: MarkType;
    onMarkTypeChange?: (stickersetName: string, markType: MarkType) => any;
    StickerComponent?: (props: { sticker: Sticker }) => JSX.Element;
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

    render() {
        const { stickerset, stickers, StickerComponent = StickerComponent_ } = this.props;

        return (
            <div className={styles.container}>
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
            </div>
        );
    }
}

export default MarkStickerForm;