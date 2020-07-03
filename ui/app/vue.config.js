module.exports = {
  transpileDependencies: ["vuetify"],
  devServer: {
    disableHostCheck: true,
    host: "0.0.0.0",
    proxy: "http://localhost:8000",
  },
};
