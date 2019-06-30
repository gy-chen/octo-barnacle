import * as React from 'react';

import { storiesOf } from '@storybook/react';
import { action } from '@storybook/addon-actions';

import MarkButton from '../src/components/MarkButton';
import NextBatchButton from '../src/components/NextBatchButton';
import Sticker from '../src/components/Sticker';


storiesOf('MarkButton', module)
  .add('basic', () => <MarkButton />)
  .add('disabled', () => <MarkButton disabled />)
  .add('onClick', () => <MarkButton onClick={action('onClick')} />);

storiesOf('NextBatchButton', module)
  .add('basic', () => <NextBatchButton />)
  .add('disabled', () => <NextBatchButton disabled />)
  .add('onClick', () => <NextBatchButton onClick={action('onClick')} />);

storiesOf('Sticker', module)
  .add('basic', () => {
    const toStickerImageUrl = () => 'http://placehold.jp/120x120.png';
    const sticker = {
      fileId: 'demo',
      emoji: '😀'
    };
    return <Sticker sticker={sticker} toStickerImageUrl={toStickerImageUrl} />;
  });