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

### Completions

Completions are included for tags and tag attributes, as well for built-in functions and member functions. Completions are also available for `Application.cfc` settings and methods.

In addition, there is the ability on a per project basis, via the `.sublime-project` file, to index folders of components, and then completions will be offered after typing a `.` if the preceding text matches a component file, or component file and containing directory (as DI/1 has it). So, for example, if a `services/user.cfc` file is found, then when typing either `user.` or `userService.`, the functions from that cfc will be offered as completions. To set this up you add the following setting to your project file: `"model_completion_folders":    [ "/full/path/to/model", "/another/full/path/to/index" ]`.

### Inline Documentation

<kbd>F1</kbd> is mapped to an inline documentation command that provides an inline documentation popup based on the cursor position.

**Note: The default key binding for inline documentation has been changed from <kbd>CTRL</kbd>+<kbd>F12</kbd> to <kbd>F1</kbd>. You can always override the default key binding in your user key bindings file.**

If the documentation command is run when the cursor is within a built-in function or tag it will load the http://cfdocs.org documentation for that function or tag. Thus, having the cursor anywhere within `dateFormat(myDate, "yyyy-mm-dd")` and pressing <kbd>F1</kbd> (by default) will trigger a popup displaying the documentation for `dateFormat`. Similarly, having the cursor anywhere within `<cfinclude template="myOtherTemplate.cfm">` and pressing <kbd>F1</kbd> will trigger the display of the documention for `cfinclude`.

*Note:* If a tag has a script expression in it (e.g. `<cfset myVar=false>`, or anything between `#`'s), the pop up will not be triggered if the cursor is within that expression.

Inline documentation is also available for `Application.cfc` settings and methods as well as method calls that have been indexed via the model completions functionality (see above). In the latter case documentation of the function signature, file location, and argument list is provided.

### Controller/View Toggle

Lucee/CFML MVC frameworks typically have the convention that a `controllers` and a `views` folder are contained in the same parent directory, and that controller names and methods correspond to view folder and file names. <kbd>CTRL</kbd>+<kbd>F1</kbd> (<kbd>command</kbd>+<kbd>F1</kbd> on a Mac) is mapped to a toggle command that will jump the editor back and forth between a view file and the controller method that corresponds to it. The settings which determine which folder names are regarded as controller and view folders are contained in the package settings file. By default, `controllers` and `handlers` are treated as controller folders, and `views` as the views folder. Alternate folder names can be specifed in the user package settings file.

### Custom Coloring for Lucee/CFML Tags

Unless you are using a specialized color scheme, Lucee/CFML tags and HTML tags will receive the same coloring. This can make it a bit harder to distinguish between the two types of tags when embedding Lucee/CFML tags in HTML. This package has a command you can run from the command palette that will inject custom colors for Lucee/CFML tags into your current color scheme (or remove them if they are already there). Press <kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd> to bring up the command palette (<kbd>CMD</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd> on a Mac) and run `Lucee: Toggle Color Scheme Styles`. You can edit the styles that will be injected via the user settings for this package. This can be found under the menu `Package Settings -> Lucee -> Package Settings - User` or via the command palette: `Lucee: User Package Settings`. See the default settings file for the settings to use (`Package Settings -> Lucee -> Package Settings - Default` or via the command palette: `Lucee: Default Color Scheme Styles`).

*Note:* Do not edit the default settings to change the color scheme styles, but rather place your custom settings in the user settings file, as this will not be overwritten when the package is upgraded.

*Caveat:* This feature works by either overriding or modifying your active color scheme file. Because of this, it may not work well with other packages that also modify the active color scheme in some way. Also, if the package containing your active color scheme is updated, it is likely that you will need to toggle the custom tag coloring off and then on again to pick up any changes.

### CommandBox

CommandBox (https://www.ortussolutions.com/products/commandbox) has been added as the default CFML build system. This simply means that running the build command (<kbd>F7</kbd> on Windows) on a CFML file will run `box ${filename}` as a shell command in the directory of the file and output the result in a pane within Sublime Text (it can also be selected from the build system menu available via <kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>B</kbd>). For this to work, CommandBox needs to be installed, and the CommandBox `box` binary needs to be available system wide, so that `box` can be run in any directory (see https://ortus.gitbooks.io/commandbox-documentation/content/setup/installation.html).

### TestBox

TestBox (https://www.ortussolutions.com/products/testbox) completions and inline documentation are available for `BaseSpec` components. They are enabled by default, but can be disabled globally by adding `"testbox_enabled": false` to your Lucee user package settings, or on a per project basis by adding the same setting to a project settings file. The completions and documentation are offered in any cfc that is contained under a folder named `tests` (alternate folders can be specified in the settings), as well as in any cfc that extends `testbox.system.BaseSpec`.

There are three build system variants for running TestBox tests from within Sublime Text. The first is for running all of a project's tests, which can be used no matter what project files are open, so long as the active file is a CFML one. The next variant is for running all of the tests in the directory of the currently active file, while the last variant runs the tests in the currently active test cfc only. <kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>B</kbd> calls up the build system menu, from which these options can be selected. Once one of the variants has been run, <kbd>CTRL</kbd>+<kbd>B</kbd> can used to run the last selected option again, without having to go through the menu.

Several settings need to be set in a project in order for these build systems to function. The first setting is `testbox_runner_url`, which should be the URL to a TestBox runner which runs tests and returns results in JSON. This needs to be setup so that a dot delimited directory of tests to run can be appended to it. An example URL that does this might be the following: `http://localhost:8888/testbox/system/Testbox.cfc?method=runremote&reporter=json&directory=`. The second setting is `testbox_default_directory`, which is the dot delimited directory that will be appended to the `testbox_runner_url` when the build variant for running all of a project's tests is selected. The last setting is `testbox_tests_root`, which is the root directory path that is used to determine the dot delimited path to a test directory when running the tests in a particular folder or file. (This could be the path to your project's webroot if your tests are contained under the webroot, but might not be if mappings are used.)

Results are displayed in a results pane. If there are errors or failures you can step backwards and forwards through the file stack traces via <kbd>F4</kbd> and <kbd>SHIFT</kbd>+<kbd>F4</kbd>. As each file is selected, Sublime Text opens that file and jumps to the line indicated. You can also double click on any file, and Sublime Text will open it for you.  Since the path to your files might look different to Sublime Text and the Lucee application server (for example, if Lucee is running in a virtual machine), there is one more setting that maps the path as it appears to the server to the path as it appears to Sublime Text. Use `testbox_results.server_root` and `testbox_results.sublime_root` to specify the respective root paths to your project, so that Sublime Text can accurately open the files in stack traces.

All of the settings for TestBox can be seen in the default package settings.

### Framework One

Framework One (https://github.com/framework-one/fw1) function completions and `variables.framework` setting completions are available. They are disabled by default, but can be enabled globally by adding `"fw1_enabled": true` to your Lucee user package settings, or on a per project basis by adding the same setting to a project settings file. (Project based settings will override global settings. The default package settings for Framework One can be viewed in the Lucee default package settings file.) The completions are offered in `Application.cfc` as well as in Framework One controller, view and layout files. (The folder names can be specified in the settings.) In controllers, Framework One method completions are offered after typing `framework.` and `fw.`.

### Installation

Locate your Sublime Text 3 packages directory. This can be easily done by opening the command palette in Sublime Text (<kbd>CTRL</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd> on Windows, <kbd>CMD</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd> on a Mac), and running `Preferences: Browse Packages`.

On Windows it will typically be something like this:
`C:\Users\Username\AppData\Roaming\Sublime Text 3\Packages\`

On a Mac it will be something like this:
`/Users/Username/Library/Application Support/Sublime Text 3/Packages/`

#### Via Git

Open Terminal or Command Prompt and cd into your packages directory, then run:

    git clone https://github.com/jcberquist/sublimetext-lucee.git ./Lucee

The specified `./Lucee` subdirectory is optional and if it is not included the package will be cloned into `sublimetext-lucee`.

That's it, restart Sublime Text 3 - if you want to update the code to match this repo, simply run the following inside the folder where you installed the package:

    git pull origin master

#### Manually

Use the `Download ZIP` option to download a zip of the repository to your computer. Unzip this, and copy the repository folder into your Sublime Text packages directory. You can leave the folder name as is, or rename it (e.g. to `Lucee`).