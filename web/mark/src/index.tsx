import { h, render } from 'preact';
import * as styles from './index.css';

const Hello = () => {
    return <div className={styles.hello}>Hello</div>;
};

render(<Hello />, document.body);