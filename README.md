# SVG file to beamer slides

## Description

This repo contains a Python 3 script which takes a multilayer SVG file as input and creates new files (SVG, PDF, and LaTeX) from which you can create
a slide show consisting of the layers of the original file being stacked on top of each other. This is especially useful for LaTeX [beamer](https://ctan.org/pkg/beamer) presentations.

## Dependencies

* Python 3.6 or later
* Inkscape 1.2 or later

## Beamer instructions

The process for creating beamer slides from an SVG file is as follows:
1. Open the SVG file in [Inkscape](https://inkscape.org/) and split it into layers such that 'later' objects are placed on higher layers. Save the edited file as e.g. `myfile.svg`.
2. Run `svgtoslides myfile.svg`. If there were 3 layers in the original file, this creates the files
    * `myfile1.pdf`, `myfile1.pdf_tex`, `myfile1.svg`, 
    * `myfile2.pdf`, `myfile2.pdf_tex`, `myfile2.svg`, 
    * `myfile3.pdf`, `myfile3.pdf_tex`.
    
    There is no file `myfile3.svg` as that would just be equal to the original `myfile.svg`.

3. In your beamer document, you can include the generated slides as follows:
    ```latex
    \usepackage{import}
    ...
    \begin{frame}
        \scalebox{0.5}{ % Change the scale to suit you
            \only<1>{\import{path/to/files/}{myfile1.pdf_tex}}
            \only<2>{\import{path/to/files/}{myfile2.pdf_tex}}
            \only<3>{\import{path/to/files/}{myfile3.pdf_tex}}
        }
    \end{frame}
    ```
    That's it!

## More info

For more info and options, run `svgtoslides --help`
