const path = require('path');

module.exports = {
  mode: 'development', // or 'production'
  entry: './application/static/js/index.js',
  output: {
    path: path.resolve(__dirname, 'application/static/js'),
    filename: 'bundle.js',
  },
//   resolve: {
//     modules: [path.resolve(__dirname, 'application/static/js'), 'node_modules'],
//   },
};