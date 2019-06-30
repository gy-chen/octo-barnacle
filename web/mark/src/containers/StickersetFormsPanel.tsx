import * as React from 'react';
import { connect } from 'react-redux';
import { AppState } from '../store';
import StickersetFormsPanel from '../components/StickersetFormsPanel';
import { Stickerset } from '../store/batch/types';
import MarkStickersetForm from '../components/MarkStickersetForm';
import { updateMarkFormAction } from '../store/mark/actions';

interface Props {
    state: AppState;
    updateMarkForm: typeof updateMarkFormAction;
}

const StickersetFormsPanelContainer = (props: Props) => {
    const { state, updateMarkForm } = props;

    const toStickersetForm = (stickerset: Stickerset) => {
        return <MarkStickersetForm
            key={stickerset.name}
            stickerset={stickerset}
            stickers={state.batch.stickers[stickerset.name]}
            selectedMarkType={state.mark.markForms[stickerset.name]}
            markResult={state.mark.markResults[stickerset.name]}
            onMarkTypeChange={updateMarkForm}
        />;
    };

    return (
        <StickersetFormsPanel>
            {state.batch.stickersets.map(toStickersetForm)}
        </StickersetFormsPanel>
    );
};

const mapStateToProps = (state: AppState) => ({
    state
});

const mapDispatchToProps = {
    updateMarkForm: updateMarkFormAction
};

export default connect(mapStateToProps, mapDispatchToProps)(StickersetFormsPanelContainer);