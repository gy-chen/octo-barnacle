const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const addCssTypes = require('./config/addCssTypes');
const getClientEnvironment = require('./config/env');

require('dotenv').config()


module.exports = async () => {

    await addCssTypes(path.join(__dirname, 'src'));

    return {
        mode: 'development',
        entry: './src/index.tsx',
        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    use: 'ts-loader',
                    exclude: /node_modules/
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
            ]
        },
        resolve: {
            extensions: ['.tsx', '.ts', '.js']
        },
        output: {
            filename: 'bundle.js',
            path: path.resolve(__dirname, 'dist')
        },
        plugins: [
            new CleanWebpackPlugin(),
            new HtmlWebpackPlugin(),
            new webpack.DefinePlugin({ 'process.env': getClientEnvironment() })
        ],
        devtool: 'inline-source-map',
        devServer: {
            contentBase: './dist'
        },
    };
};
