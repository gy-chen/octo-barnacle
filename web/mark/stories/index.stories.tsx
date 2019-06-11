import { h } from 'preact';

import { storiesOf } from '@storybook/preact';

import MarkStickersetForm from '../src/MarkStickersetForm';
import MarkButton from '../src/MarkButton';
import NextBatchButton from '../src/NextBatchButton';


storiesOf('MarkStickersetForm', module)
  .add('basic', () => <MarkStickersetForm />);

storiesOf('MarkButton', module)
  .add('basic', () => <MarkButton />);

storiesOf('NextBatchButton', module)
  .add('basic', () => <NextBatchButton />);