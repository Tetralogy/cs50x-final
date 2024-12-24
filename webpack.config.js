const path = require('path');
const webpack = require('webpack');

module.exports = {
  mode: 'development', // or 'production'
  entry: './application/static/js/index.js',
  output: {
    path: path.resolve(__dirname, 'application/static/js'),
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  // This ensures proper source maps for debugging
  devtool: 'source-map',
  resolve: {
    alias: {
      bootstrap: path.resolve(__dirname, 'node_modules/bootstrap'),
    },
  },
};