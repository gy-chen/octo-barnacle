import { connect } from 'react-redux';
import MarkButton from '../components/MarkButton';
import { startMarkRequestAction } from '../store/mark/actions';
import { mark } from '../api';
import { AppState } from '../store';

const mapStateToProps = (state: AppState) => ({
    disabled: state.batch.stickersets.length == 0 || state.batch.isBatchRequesting || state.mark.isMarkRequesting
});

const mapDispatchToProps = {
    onClick: () => startMarkRequestAction(mark)
};

export default connect(mapStateToProps, mapDispatchToProps)(MarkButton);