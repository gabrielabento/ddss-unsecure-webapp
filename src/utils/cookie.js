function parse(cookies = "") {
  let cookieObj = {};
  const cookiesList = cookies.split(";");

  cookiesList.forEach(function parseCookie(cookie) {
    const [cookieName, cookieValue] = cookie.trim().split("=");
    cookieObj[cookieName] = cookieValue;
  });

  return cookieObj;
}

exports.parse = parse;
