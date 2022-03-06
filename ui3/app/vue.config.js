const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "^/api": {
        target: `http://${process.env.DEV_PROXY ?? "localhost"}:8000`,
        secure: false,
        logLevel: "debug",
      },
    },
  }
});
