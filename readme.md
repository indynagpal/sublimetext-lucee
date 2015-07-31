# Lucee Package for Sublime Text
## Sublime Text 3 dev build 3092+ only

This package was developed from the following packages:

* https://github.com/SublimeText/ColdFusion
* https://github.com/sublimehq/Packages (especially the HTML and JavaScript syntaxes)
* https://github.com/Benvie/JavaScriptNext.tmLanguage (from which the current Sublime JavaScript syntax is derived)

It includes syntax highlighting for both the new Lucee 5 dialect and the current CFML dialect. It recognizes the following file extensions: `lucee,lc,cfm,cfml,cfc`. It also has function and tag completions.

Installation must currently be done manually by downloading the repository and placing it in a folder within your Sublime packages folder.

### Key Bindings

In tag attributes, script strings, and between `cfoutput` tags, pressing `#` will automatically be escaped `##` if there is no cursor selection, or it will wrap the currently selected text `#selected#`.

<kbd>CTRL</kbd>+<kbd>ALT</kbd>+<kbd>D</kbd> will output a `dump` tag or `writeDump()/dump()` function, wrapping any currently selected text.

<kbd>CTRL</kbd>+<kbd>ALT</kbd>+<kbd>A</kbd> will output an `abort` tag.

If SublimeText's `auto_close_tags` setting is true, when a closing tag's `/` has been pressed, the closing tag will be completed. (Hopefully not closing `cfset` tags and the like.)

<kbd>CTRL</kbd>+<kbd>F12</kbd> pressed when the cursor is on a built-in function (e.g. `arrayMap()`) or a tag (e.g. `<cfset>`, will load the http://docs.lucee.org page for that function in the default browser.

### Completions

Completions are included for tags and tag attributes, as well for built-in functions and member functions. There is also the ability on a per project basis, via the `.sublime-project` file, to index folders of components, and then completions will be offered after typing a `.` if the preceding text matches a component file, or component file and containing directory (as DI/1 has it). So, for example, if a `services/user.cfc` file is found, then when typing either `user.` or `userService.`, the functions from that cfc will be offered as completions. To set this up you add the following setting to your project file: `"model_completion_folders":    [ "/full/path/to/model", "/another/full/path/to/index" ]`.