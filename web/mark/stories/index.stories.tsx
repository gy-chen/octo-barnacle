import { h } from 'preact';

import { storiesOf } from '@storybook/preact';

import MarkStickersetForm from '../src/components/MarkStickersetForm';
import MarkButton from '../src/components/MarkButton';
import NextBatchButton from '../src/components/NextBatchButton';


storiesOf('MarkStickersetForm', module)
  .add('basic', () => <MarkStickersetForm />);

storiesOf('MarkButton', module)
  .add('basic', () => <MarkButton />);

storiesOf('NextBatchButton', module)
  .add('basic', () => <NextBatchButton />);