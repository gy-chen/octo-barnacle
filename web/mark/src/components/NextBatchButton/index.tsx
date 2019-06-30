import * as React from 'react';
import * as styles from './nextBatchButton.css';

interface Props {
    onClick?: () => void;
    disabled?: boolean;
}

const NextBatchButton = (props: Props) => {
    const { disabled = false, onClick } = props;

    return (
        <button className={styles.nextBatchButton} disabled={disabled} onClick={onClick}>
            <div className={styles.nextBatchIcon}></div>
        </button>
    );
}

export default NextBatchButton;