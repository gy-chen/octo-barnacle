const path = require('path');
const DtsCreator = require('typed-css-modules');
const chokidar = require('chokidar');

const addCssTypes = (rootPath, opts = {}) => {
    return new Promise(resolve => {
        const { watch = false } = opts;

        const watchPaths = [path.join(rootPath, '**/*.css')];
        const watcher = chokidar.watch(watchPaths, {
            ignored: '*.d.*',
            persistent: watch,
        })

        const preReadyPromises = [];
        let isReady = false;

        const onChange = async path => {
            const promise = (async () => {
                const creator = new DtsCreator({
                    camelCase: true
                });
                const result = await creator.create(path);
                await result.writeFile();
            })();

            if (!isReady) {
                preReadyPromises.push(promise);
            }
        };

        watcher.on('change', onChange);
        watcher.on('add', onChange);

        watcher.on('ready', () => {
            isReady = true;
            Promise.all(preReadyPromises).then(resolve);
            if (!watch) {
                watcher.close();
            }
        });
    });
};

module.exports = addCssTypes;