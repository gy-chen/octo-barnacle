import { connect } from 'react-redux';
import NextBatchButton from '../components/NextBatchButton';
import { startBatchRequestAction } from '../store/batch/actions';
import { nextBatch } from '../api';
import { AppState } from '../store';

const mapStateToProps = (state: AppState) => ({
    disabled: state.batch.isBatchRequesting || state.mark.isMarkRequesting
});

const mapDispatchToProps = {
    onClick: () => startBatchRequestAction(nextBatch)
};

export default connect(mapStateToProps, mapDispatchToProps)(NextBatchButton);