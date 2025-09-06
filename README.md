# EEK_lab
This is the repository where you can find all of the resources I used regarding the USN course TSE2370-1 Elektroniske enheter og kretsert (Electronic components and circuits)

## Licence
All files within this repository are licensed under the [MIT License](LICENSE), allowing you to freely use, modify, and distribute the code for any purpose, provided you include the original license notice.

## Use
Do you want to use some of this material for your own course completion, feel free. Keep in mind that copy pasting from the documents will not teach you anything about components and circuits and it will be flagged as plagiarism and then you don't pass the course. That said, using this as an example solution or comparing to see why/how something works like it does is a good idea. If you just want a LaTeX sample document to use my styles you can use any main.tex file as a template on how to make such documents, and the styling/LaTeX preamble is  stored within KjelsethReportStyle.sty, found in this root folder to the repository. Also feel free to reach out if you have any questions about the customization or use.

# LaTeX file
To use the LaTeX file you need to render it with LuaLaTeX, for all of the preable to work. I use VScode with LaTeX workshop extension and have installed MacTeX, but this last one will depend on what system you use.

## Structure
Each lab task has it's own folder where the LaTeX report and its relevant files are. usually these will be within their own folders like this:
- Figures  - for all pictures, screenshots and similar
- Affinity - for all affinity photo project files, before final edit is exported to figures
- LaTeX    - for all compiling files of the LaTeX document
