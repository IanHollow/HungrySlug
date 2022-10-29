import * as https from 'https';
import * as cheerio from "cheerio";

const getHtml = async (hostname: string, path: string): Promise<string> =>
  new Promise((resolve, reject) => {
    https
      .get(
        {
          hostname,
          path,
          method: "GET",
        },
        (res) => {
          let html = "";
          res.on("data", function (chunk) {
            html += chunk;
          });
          res.on("end", function () {
            resolve(html);
          });
        }
      )
      .on("error", (error) => {
        console.error(error);
        reject(error);
      });
  });

const getDHUrls = (html: string) => {
  const $start_html = cheerio.load(html);
  // Create websites array to store dining hall websites
  const dh_websites: any[] = [];
  // Find all elements with locations class, find their url and add them to the dh_websites array
  $start_html("li.locations").each((i, el) => {
    const link = $start_html(el).find("a").attr("href");
    if (dh_websites.length < 4) {
      dh_websites.push(link);
    }
  });
  // add orginal url to start of new urls
  for (let i = 0; i < dh_websites.length; i++) {
    dh_websites[i] = `https://nutrition.sa.ucsc.edu/${dh_websites[i]}`;
  }
  return dh_websites;
};

getHtml("nutrition.sa.ucsc.edu", "")
.then(getDHUrls)
.then((data) => console.log(data))
.catch((error) => console.log(error));