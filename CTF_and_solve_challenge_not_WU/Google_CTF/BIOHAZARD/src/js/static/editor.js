(() => {
    var e = new goog.editor.Field("editMe");
    e.registerPlugin(new goog.editor.plugins.BasicTextFormatter), e.registerPlugin(new goog.editor.plugins.RemoveFormatting), e.registerPlugin(new goog.editor.plugins.UndoRedo), e.registerPlugin(new goog.editor.plugins.ListTabHandler), e.registerPlugin(new goog.editor.plugins.SpacesTabHandler), e.registerPlugin(new goog.editor.plugins.EnterHandler), e.registerPlugin(new goog.editor.plugins.HeaderFormatter), e.registerPlugin(new goog.editor.plugins.LoremIpsum("Click here to edit")), e.registerPlugin(new goog.editor.plugins.LinkDialogPlugin), e.registerPlugin(new goog.editor.plugins.LinkBubble);
    const o = [goog.editor.Command.LINK, goog.editor.Command.BOLD, goog.editor.Command.ITALIC, goog.editor.Command.UNORDERED_LIST, goog.editor.Command.FONT_COLOR, goog.editor.Command.FONT_FACE, goog.editor.Command.FONT_SIZE, goog.editor.Command.JUSTIFY_LEFT, goog.editor.Command.JUSTIFY_CENTER, goog.editor.Command.JUSTIFY_RIGHT];
    var g = goog.ui.editor.DefaultToolbar.makeToolbar(o, goog.dom.getElement("toolbar")); new goog.ui.editor.ToolbarController(e, g), e.makeEditable(), goog.events.listen(e, goog.editor.Field.EventType.DELAYEDCHANGE, (function () {
        let o = e.getCleanContents(), g = goog.dom.getElement("youtube").value;
        if (g.startsWith("https://www.youtube.com/watch")) { let e = new URL(g), t = new URLSearchParams(e.search), i = document.createElement("iframe"); i.src = `https://www.youtube.com/embed/${t.get("v")}`, i.width = "560", i.height = "315", o += "<br>" + i.outerHTML } let t = sanitizer.sanitize(o);
        setInnerHTML(goog.dom.getElement("preview"), t), goog.dom.getElement("introduction").value = t
    }))
})();
