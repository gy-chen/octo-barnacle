const path = require('path');
const addCssTypes = require('../config/addCssTypes');

module.exports = async ({ config }) => {
    await addCssTypes(path.join(__dirname, '../src'), { watch: true });

    config.module.rules = [
        {
            test: /\.(ts|tsx)$/,
            use: [
                {
                    loader: 'ts-loader',
                },
            ],
        },
        {
            test: /\.css?$/,
            use: [
                'style-loader',
                {
                    loader: 'css-loader',
                    options: {
                        modules: true
                    }
                }
            ]
        }
    ];
    config.resolve.extensions.push('.ts', '.tsx');
    return config;
};