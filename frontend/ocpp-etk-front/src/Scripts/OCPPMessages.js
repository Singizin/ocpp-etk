const fs = require('fs');
const path = require('path')
console.log(__filename)
const directory = 'D:\\ETK\\Programming\\Python\\ocpp-etk\\frontend\\ocpp-etk-front\\src\\assets\\schemas\\json'
const jsonsInDir = fs.readdirSync(directory).filter(file => path.extname(file) === '.json');

module.exports = {
  getAllMessages: () => {
    return Object.fromEntries(
      jsonsInDir.map(file => {
        const fileData = fs.readFileSync(path.join(directory, file));
        const json = fileData.toString();
        return [file.replace('.json',''), json]
      })
    )
  }
}