goog.require('goog.dom');
goog.require('goog.dom.safe');
goog.require('goog.html.sanitizer.unsafe');
goog.require('goog.html.sanitizer.HtmlSanitizer.Builder');
goog.require('goog.string.Const');

window.addEventListener('DOMContentLoaded', () => {
  var Const = goog.string.Const;
  var unsafe = goog.html.sanitizer.unsafe;
  var builder = new goog.html.sanitizer.HtmlSanitizer.Builder();
  builder = unsafe.alsoAllowTags(
    Const.from('IFRAME is required for Youtube embed'), builder, ['IFRAME']);
  sanitizer = unsafe.alsoAllowAttributes(
    Const.from('iframe#src is required for Youtube embed'), builder,
    [
      {
        tagName: 'iframe',
        attributeName: 'src',
        policy: (s) => s.startsWith('https://') ? s : '',
      }
    ]).build();
});

setInnerHTML = function (elem, html) {
  goog.dom.safe.setInnerHtml(elem, html);
}



