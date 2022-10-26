const json_to_download = [
  {
    id: "0109808d-475d-471b-802e-0e5226c7600b",
    imageurl:
      "https://machinelearningforkids.co.uk/api/scratch/eec04a70-5411-11ed-9dd6-7f589b4580fe964b0d2e-7f69-40b4-85e1-6038033bcf95/images/api/classes/88fee50f-be5a-4588-84f5-25efb452fc0e/students/auth0|6331b022531bcf87a4722a24/projects/2744bea0-5410-11ed-9d8f-67dfbf0392e9/images/0109808d-475d-471b-802e-0e5226c7600b",
    label: "divisao",
  }
];

const fs = require("fs");
const https = require("https");

json_to_download.map((item) => {
  https.get(item.imageurl, (res) => {
    const path = `./${item.id}`;
    const filePath = fs.createWriteStream(path);
    res.pipe(filePath);
    filePath.on("finish", () => {
      filePath.close();
    });
  });
});
