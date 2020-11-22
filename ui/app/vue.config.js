module.exports = {
  transpileDependencies: ['vuetify'],
  devServer: {
    // disableHostCheck: true,
    // host: '0.0.0.0',
    proxy: {
      '/api': {
        target: "http://127.0.0.1:8000",
        secure: false
      }
    }
  },
}
