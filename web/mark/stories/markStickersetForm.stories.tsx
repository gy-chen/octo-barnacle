import { h } from 'preact';
import { storiesOf } from '@storybook/preact';
import { action } from '@storybook/addon-actions';
import MarkStickersetForm from '../src/components/MarkStickersetForm';
import Sticker from '../src/components/Sticker';
import { MarkType, MarkResult } from '../src/store/mark/types';


const mockStickerset = {
    stickersetName: 'HiStickerset',
    title: 'Hi Stickerset'
};

const mockStickers = [
    {
        fileId: 'sticker1',
        emoji: '😀'
    },
    {
        fileId: 'sticker1',
        emoji: '😊'
    }
];

const toStickerImageUrl = () => 'http://placehold.jp/120x120.png';
const mockStickerComponent = (props: any) => <Sticker {...props} toStickerImageUrl={toStickerImageUrl} />;

storiesOf('MarkStickersetForm', module)
    .add('basic', () => <MarkStickersetForm
        stickerset={mockStickerset}
        stickers={mockStickers}
        StickerComponent={mockStickerComponent}
    />
    )
    .add('preselect OK', () => <MarkStickersetForm
        stickerset={mockStickerset}
        stickers={mockStickers}
        StickerComponent={mockStickerComponent}
        selectedMarkType={MarkType.OK}
    />)
    .add('onChange', () => <MarkStickersetForm
        stickerset={mockStickerset}
        stickers={mockStickers}
        StickerComponent={mockStickerComponent}
        onMarkTypeChange={action('onSelect')}
    />)
    .add('result: undefined', () => <MarkStickersetForm
        stickerset={mockStickerset}
        stickers={mockStickers}
        StickerComponent={mockStickerComponent}
    />)
    .add('result: None', () => <MarkStickersetForm
        stickerset={mockStickerset}
        stickers={mockStickers}
        StickerComponent={mockStickerComponent}
        markResult={MarkResult.NONE}
    />)
    .add('result: Success', () => <MarkStickersetForm
        stickerset={mockStickerset}
        stickers={mockStickers}
        StickerComponent={mockStickerComponent}
        markResult={MarkResult.SUCCESS}
    />)
    .add('result: InvalidParameters', () => <MarkStickersetForm
        stickerset={mockStickerset}
        stickers={mockStickers}
        StickerComponent={mockStickerComponent}
        markResult={MarkResult.INVALID_PARAMETERS}
    />)
    .add('result: ResourceExpires', () => <MarkStickersetForm
        stickerset={mockStickerset}
        stickers={mockStickers}
        StickerComponent={mockStickerComponent}
        markResult={MarkResult.RESOURCE_EXPIRES}
    />)
    .add('result: StickersetNotFound', () => <MarkStickersetForm
        stickerset={mockStickerset}
        stickers={mockStickers}
        StickerComponent={mockStickerComponent}
        markResult={MarkResult.STICKETSET_NOT_FOUND}
    />);