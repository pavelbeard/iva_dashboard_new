module.exports = {
  resolve: {
    fallback: {
      // "https": require.resolve('https-browserify'),
      // "url": require.resolve('url/'),
      // "http": require.resolve('stream-http'),
      // "buffer": false,
    }
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.css$/,
        use: [
          {
            loader: 'style-loader',
          },
          {
            loader: 'css-loader',
          },
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                plugins: () => {
                  require('autoprefixer')
                }
              }
            }
          },
          {
            loader: 'sass-loader',
          }
        ]
      }
    ]
  }
};