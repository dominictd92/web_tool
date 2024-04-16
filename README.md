# Web Tool

Web Tool is a general purpose tool that is meant to assist web developers and maintainers with their daily efforts. The 
need for this tool came from doing maintenance on a site that didn't have an adequate CMS (content management system) 
and I had time and a desire to learn Python. Overtime, there were other considerations and additions that, even though 
not needed for personal use, could be useful somewhere. 

# Usage

Within the Web Tool, there are different tools/apps that can be used. Each of these have different functionality. Even 
so, currently, the Webscrapper and the Webmapper are pretty straight-forward and self-explanatory with notes in the 
application to assist with functionality. 

# Installation

Below are examples of installing the application as a standalone app, running the commands in the directory of the 
ReadMe.md file. Although these commands work for both macOS and Windows, you cannot create the installer for a system 
that you are not currently on. Refer to [Pyinstaller](https://pyinstaller.org/en/stable/) for more information and other options.

```bash
pyinstaller --windowed --onedir --clean --icon icons/webtool_icon.icns --noconfirm --name WebTool webtool/main.py
```

To open a terminal when opening the app, use the following:

```bash
pyinstaller --nowindowed --onedir --clean --icon icons/webtool_icon.icns --noconfirm --name WebTool webtool/main.py
```

On windows, the above command will create an executable file that will open command prompt simultaneously. For macOS,
both commands will generate a UNIX executable file that can be run from Terminal with the below command: 

```bash
open -n WebTool
```

The icon is added when using "--icon", but you may have to use the .ico version depending on the system you're working on. 

Pyinstaller mentions that using '--onefile' and '--windowed' is not recommended. According to Pyinstaller "because they 
require unpacking on each run (and the unpacked content might be scanned by the OS each time). Furthermore, onefile 
executables will not work when signed/notarized with sandbox enabled." Be weary of this as you configure things. 
Changing this will automatically break logging for sure... after hours of trying to figure out different configurations 
for it.

# Support

If there are major issues or concerns, email [dominic.t.dangerfield@gmail.com](mailto:dominic.t.dangerfield@gmail.com), 
with the subject "Web Tool Support".

# Roadmap

There are a number of changes that need to happen for this project, from testing to functionality to looks, and making
it production level will take time. For what's to come, review the [Roadmap](https://github.com/dominictd92/web_tool/wiki/Roadmap). 

### Web Tool 

Here is a list of a few things that are still to come for the entire project:

- Create an icon.
- Set up logging for the application.
- Fill test website. 
- Set up Python tests for all functions. 
- New tool for getting all links, images, etc. from the website.
- Style (continuous goal)

### Tool Options
The Webmapper will have the following options: 
- Seconds before timeout
- Retries before skipping URL 
- Allow a home url 
- Starting url
- Rerun URLs that timeout after/immediately 
- Ignoring file extensions. 

The Webscrapper will have the following options: 

- Case sensitivity toggle
- Restrictions on terms within URLs to search.
- Sorting the results. 
- Searching the results. 

# Authors

- [Dominic Dangerfield](https://github.com/dominictd92)

# License

MIT
