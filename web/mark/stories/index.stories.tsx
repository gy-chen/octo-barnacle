import { h } from 'preact';

import { storiesOf } from '@storybook/preact';

import MarkStickersetForm from '../src/MarkStickersetForm';

storiesOf('MarkStickersetForm', module)
  .add('basic', () => <MarkStickersetForm />);

