export function getCookie(name) {
  const reg = new RegExp(`(^| )${name}=([^;]*)(;|$)`);
  const arr = document.cookie.match(reg);
  if (arr !== null) {
    return (arr[2]);
  }
  return null;
}

export function setCookie(cName, value, expiredays) {
  const exdate = new Date();
  exdate.setDate(exdate.getDate() + expiredays);
  const end = (expiredays === null ? '' : `;expires=${exdate.toGMTString()}`);
  document.cookie = `${cName}=${escape(value)}${end}`;
}

export function delCookie(name) {
  const exp = new Date();
  exp.setTime(exp.getTime() - 1);
  const cval = getCookie(name);
  if (cval !== null) {
    document.cookie = `${name}=${cval};expires=${exp.toGMTString()}`;
  }
}
