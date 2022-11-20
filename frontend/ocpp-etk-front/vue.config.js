const fs = require('fs');
const webpack = require('webpack');
const {defineConfig} = require('@vue/cli-service');
const {getAllMessages} = require("./src/Scripts/OCPPMessages.js");
const messages = getAllMessages()


module.exports = defineConfig({
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:4567',
        changeOrigin: true
      }
    }
  },
  transpileDependencies: true,
  configureWebpack: config => {
    return {
      plugins: [
        new webpack.DefinePlugin({
          OCPP_MESSAGES: messages,
        })
      ]
    }
  },
})



