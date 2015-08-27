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

### CFDocs Tag and Function Documentation

<kbd>CTRL</kbd>+<kbd>F12</kbd> pressed when the cursor is within a built-in function or tag will load the http://cfdocs.org documentation for that function or tag in a pop up window within Sublime. For example, having the cursor anywhere within `dateFormat(myDate, "yyyy-mm-dd")` and pressing <kbd>CTRL</kbd>+<kbd>F12</kbd> will trigger a pop up displaying the documentation for `dateFormat`. Similarly, having the cursor anywhere within `<cfinclude template="myOtherTemplate.cfm">` and pressing <kbd>CTRL</kbd>+<kbd>F12</kbd> will trigger the display of the documention for `cfinclude`.

*Note:* If a tag has a script expression in it (e.g. `<cfset myVar=false>`, or anything between `#`'s), the pop up will not be triggered if the cursor is within that expression.

### Completions

Completions are included for tags and tag attributes, as well for built-in functions and member functions. There is also the ability on a per project basis, via the `.sublime-project` file, to index folders of components, and then completions will be offered after typing a `.` if the preceding text matches a component file, or component file and containing directory (as DI/1 has it). So, for example, if a `services/user.cfc` file is found, then when typing either `user.` or `userService.`, the functions from that cfc will be offered as completions. To set this up you add the following setting to your project file: `"model_completion_folders":    [ "/full/path/to/model", "/another/full/path/to/index" ]`.

### Custom Coloring for Lucee/CFML Tags

Unless you are using a specialized color scheme, Lucee/CFML tags and HTML tags will receive the same coloring. This can make it a bit harder to distinguish between the two types of tags when embedding Lucee/CFML tags in HTML. This package has a command you can run from the command palette that will inject custom colors for Lucee/CFML tags into your current color scheme (or remove them if they are already there). Press <kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd> to bring up the command palette (<kbd>CMD</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd> on a Mac) and run `Lucee: Toggle Color Scheme Styles`. You can edit the styles that will be injected via the user color scheme settings for this package. This can be found under the menu `Package Settings -> Lucee -> Color Scheme Styles - User` or via the command palette: `Lucee: User Color Scheme Styles`. See the default settings file for the settings to use (`Package Settings -> Lucee -> Color Scheme Styles - Default` or via the command palette: `Lucee: Default Color Scheme Styles`).

*Note:* Do not edit the default settings to change the color scheme styles, but rather place your custom settings in the user settings file, as this will not be overwritten when the package is upgraded.

*Caveat:* This feature works by either overriding or modifying your active color scheme file. Because of this, it may not work well with other packages that also modify the active color scheme in some way. Also, if the package containing your active color scheme is updated, it is likely that you will need to toggle the custom tag coloring off and then on again to pick up any changes.

### Installation

Locate your Sublime Text 3 packages directory. This can be easily done by opening the command palette in Sublime Text (<kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd> on Windows, <kbd>CMD</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd> on a Mac), and running `Preferences: Browse Packages`.

On Windows it will typically be something like this:
`C:\Users\Username\AppData\Roaming\Sublime Text 3\Packages`

On a Mac it will be something like this:
`/Users/Username/Library/Application Support/Sublime Text 3/Packages/`

#### Via Git

Open Terminal or Command Prompt and cd into your packages directory, then run:

    git clone https://github.com/jcberquist/sublimetext-lucee.git

You can optionally specify a subdirectory name to clone into by adding it to the `git clone` command. For example, to clone into a folder named `Lucee` run:

    git clone https://github.com/jcberquist/sublimetext-lucee.git ./Lucee

Or you can leave it as is, and it will clone into `sublimetext-lucee`.

That's it, restart Sublime Text 3 - if you want to update the code to match this repo, simply run the following inside the folder where you installed the package:

    git pull origin master

#### Manually

Use the `Download ZIP` option to download a zip of the repository to your computer. Unzip this, and copy the repository folder into your Sublime Text packages directory. You can leave the folder name as is, or rename it (e.g. to `Lucee`).
