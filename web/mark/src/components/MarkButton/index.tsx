import * as React from 'react';
import * as styles from './markButton.css';

interface Props {
    onClick?: () => void,
    disabled?: boolean
}

const MarkButton = (props: Props): any => {
    const { disabled = false, onClick } = props;
    return (
        <button className={styles.markButton} disabled={disabled} onClick={onClick}>
            <div className={styles.markIcon}></div>
        </button>
    );
};

export default MarkButton;