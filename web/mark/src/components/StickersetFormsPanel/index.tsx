import * as React from 'react';
import * as styles from './stickersetFormsPanel.css';

interface Props {
    children?: JSX.Element[] | JSX.Element
}

const StickersetFormsPanel = (props: Props) => {
    const { children } = props;

    return (
        <div className={styles.container}>
            {children}
        </div>
    );
};

export default StickersetFormsPanel;