const teste = 0 //colar o json aqui

const fs = require("fs");
const https = require("https");

teste.map((item) => {
  https.get(item.imageurl, (res) => {
    // Image will be stored at this path
    const path = `./${item.id}`;
    const filePath = fs.createWriteStream(path);
    res.pipe(filePath);
    filePath.on("finish", () => {
      filePath.close();
    });
  });
});
