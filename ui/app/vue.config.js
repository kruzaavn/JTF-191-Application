module.exports = {
  transpileDependencies: ['vuetify'],
  devServer: {
    // disableHostCheck: true,
    // host: '0.0.0.0',
    proxy: {
      '^/api': {
        target: `http://${process.env.DEV_PROXY ?? 'localhost'}:8000`,
        secure: false,
        logLevel: 'debug',
      },
    },
  },
}
