import { h } from 'preact';
import { storiesOf } from '@storybook/preact';
import MarkStickersetForm from '../src/components/MarkStickersetForm';
import StickersetFormsPanel from '../src/components/StickersetFormsPanel';
import Sticker from '../src/components/Sticker';
import { MarkType } from '../src/store/mark/types';

const generateMockStickerset = (appendix: string | number) => ({
    stickersetName: `HiStickerset${appendix}`,
    title: `Hi Stickerset${appendix}`
});

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

storiesOf('StickersetFormsPanel', module)
    .add('basic', () => {
        const children = Array.from({ length: 12 }, (_, i) => <MarkStickersetForm
            stickers={mockStickers}
            stickerset={generateMockStickerset(i)}
            StickerComponent={mockStickerComponent}
            selectedMarkType={MarkType.OK}
        />);

        return (
            <StickersetFormsPanel>
                {children}
            </StickersetFormsPanel>
        );
    });