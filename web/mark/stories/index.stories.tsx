import { h } from 'preact';

import { storiesOf } from '@storybook/preact';
import { action } from '@storybook/addon-actions';

import MarkStickersetForm from '../src/components/MarkStickersetForm';
import MarkButton from '../src/components/MarkButton';
import NextBatchButton from '../src/components/NextBatchButton';


storiesOf('MarkStickersetForm', module)
  .add('basic', () => <MarkStickersetForm />);

storiesOf('MarkButton', module)
  .add('basic', () => <MarkButton />)
  .add('disabled', () => <MarkButton disabled />)
  .add('onClick', () => <MarkButton onClick={action('onClick')} />);

storiesOf('NextBatchButton', module)
  .add('basic', () => <NextBatchButton />);