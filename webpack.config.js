const MiniCssExtractPlugin = require('mini-css-extract-plugin');
   const path = require('path');

   module.exports = {
     entry: './src/index.js',
     output: {
       filename: 'bundle.js',
       path: path.resolve(__dirname, 'static'),
     },
     module: {
       rules: [
         {
           test: /\.(scss|css)$/,
           use: [
             MiniCssExtractPlugin.loader,
             'css-loader',
             'sass-loader',
           ],
         },
       ],
     },
     plugins: [new MiniCssExtractPlugin({
       filename: 'main.css',
     })],
   };