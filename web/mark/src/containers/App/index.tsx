import * as React from 'react';
import StickersetFormsPanel from '../StickersetFormsPanel';
import MarkButton from '../MarkButton';
import NextBatchButton from '../NextBatchButton';

const App = () => {
    return (
        <div>
            <StickersetFormsPanel />
            <MarkButton />
            <NextBatchButton />
        </div>
    );
};

export default App;