# EEK_lab
This is the repository where you can find all of the resources I used regarding the USN course TSE2370-1 Elektroniske enheter og kretsert (Electronic components and circuits)

## Licence
All files within this repository are licensed under the [MIT License](LICENSE), allowing you to freely use, modify, and distribute the code for any purpose, provided you include the original license notice.

## Use
Do you want to use some of this material for your own course completion, feel free. Keep in mind that copy pasting from the documents will not teach you anything about components and circuits and it will be flagged as plagiarism and then you don't pass the course. That said, using this as an example solution or comparing to see why/how something works like it does is a good idea. If you just want a LaTeX sample document to use my styles you can use the template.tex file as a template on how to make IEEE documents. Also feel free to reach out if you have any questions about the customization or use.

## LaTeX file
To use the LaTeX files (from Lab 03 and onwards) you need to render it with PdfLaTeX, for all the IEEEtran class to work as intended. Note that Lab 01 and Lab 02 uses some custom styling that will only compile with LuaLaTeX and have their own .sty file to do this. I personally use VScode with LaTeX workshop extension to write LaTeX and render it side by side. You have to install some LaTeX commands, these are operating system specific. I and have installed MacTeX, as I primary use a mac, this works great, I cannot comment on what to use for Windows or Linux.

## Structure
Each lab task has it's own folder where the LaTeX report and its relevant files are. usually these will be within their own folders like this:
- Data     - for all raw data, like my notes/measurements/calculations in an Excel file, raw unedited photos, python code for graphing ect. 
- Figures  - for all pictures, screenshots and similar graphics to be used in the document.
- Affinity - for all affinity photo project files, before final edit is exported to figures, useful if for example you need to crop a photo different, this contains the whole photo and current configuration and can therefore also un-crop parts.
- LaTeX    - for all compiling files of the LaTeX document will be put here, including the rendered pdf (the pdf is also copied out of this folder when a report is finalized)
