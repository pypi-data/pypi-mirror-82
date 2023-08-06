.. _features:

========
Features
========

Overview
--------

We all know that doing data analysis day-to-day could easily turn into routine work and it is often hard to have fully reproducible code. Can you say for sure that you can redo your whole analysis only provided the raw data and your code?
wBuild is designed to reduce the
amount of time you spend to :ref:`publish the output of your script <publishing-the-output>`, :ref:`declare the needed input files <specify-input>`,
:ref:`run Py code as a part of work pipeline <execute-py-code>`, :ref:`use placeholders to structure your Snakemake job <use-placeholders>`,
:ref:`map your project's scripts together <script-mapping>` and many more.

Demo project
------------
It is highly recommended to see all of the `examples` of using the features :ref:`in the demo project <running-demo>`.
There you also have additional documentation that explains the features and working with them!

Command-line interface
----------------------
The command-line interface of wBuild is responsible `only` for preparing a project directory to be processed by snakemake and wBuild. There are three instructions, also shortly
documented under :bash:`wbuild -h`

:bash:`wbuild demo`
    Run :ref:`demo project <running-demo>`.

.. _wbuild-init:

:bash:`wbuild init`
    Initialize `wBuild` in an already existing project. This command prepares all important wrappers and files for Snakemake.

:bash:`wbuild update`
    To be called on an already initialized project. Updates :bash:`.wbuild` directory to the latest version using
    :ref:`installed <install-wbuild>` Python :code:`wbuild` package.

All these commands should be executed from the **root directory of the project**.

Snakemake CLI
~~~~~~~~~~~~~

Most of the job of building your project is done by Snakemake, :ref:`as explained here <overview-of-functionality>`. There
are also several special Snakemake rules that wBuild provides. The most important include:

snakemake mapScripts
    Do :ref:`script mapping <script-mapping>`

snakemake publish
    Publish your html output pages to your :ref:`projectWebDir <publishing-the-output>`

snakemake clean
    Deletes html output, generated dependencies file and Python cache.

.. _restore-mod-date:

snakemake restoreModDate
    Restore previous modification date of all the files. Comes handy for pulling changes from VCS, where all the mod.dates
    get changed.

:ref:`See more <snakemake-features>` about this down the page.

.. _yaml-headers:

Parsing YAML headers
--------------------
In following, we present a basic YAML header:

.. code-block:: R

    #'---
    #' title: Basic Input Demo
    #' author: Leonhard Wachutka
    #' wb:
    #'  input:
    #'  - iris: "Data/{wbP}/iris.RDS"
    #'  output:
    #'  - pca: " {wbPD_P}/pca.RDS"
    #' type: script
    #'---


wBuild requires users to define information of the scripts in RMarkdown YAML-format header.
wBuild scans it and outputs `rules for Snakemake`_. :code:`wb` block is a "wBuild-own" one.
Important tags here are input and output. These are used to :ref:`costruct the snakemake pipeline <overview-of-functionality>`,
and :ref:`render the script into an HTML format <publishing-the-output>`.

Tags that can be provided mainly follow the logic of Snakemake and partially that of wbuild.

**Please note**: YAML tags have a strict format that they should follow - e.g. there should be *no tabs*, **only spaces!**
You can `read more about the YAML syntax`_.

.. _read more about the YAML syntax: http://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html

If you want to access information from the header of a script from within the script (code self-reflection), need to **source** :code:`.wBuild\wBuildParser.R` and **call**
:code:`parseWBHeader()` with the path to your script as an argument.


Tags
~~~~

To make working with R projects even more comfortable, there are a few additional YAML tags that wBuild provides. They are:

.. _specify-input:

input
    Specify any input files you would like to use. You can later access them from the R code using :code:`snakemake@input[[<input_file_var>]]`.

output
    The same as input - accessed using :code:`snakemake@output`.

.. _execute-py-code:

py
    This tag allows you to run some Python code during parsing of the header - a good example of how this feature can be extremely helpful is
    in the :ref:`demo <running-demo>`. Don't forget the **YAML pipe operator** for the proper functionality!

type
    Tag describing the type of the file. Can be: :code:`script` for R Scripts, :code:`noindex` for Markdown and :code:`empty`
    for the rest.

The information stated under this tags is later synchronised with Snakemake.

.. _snakemake-tags:

One can also state Snakemake options in "wb" block of the YAML header and even `refer to them in this R script later` using
:code:`snakemake@`. Here, we mark that we will use 10 threads when executing this script:

.. code-block:: R

    #' wb:
    #'  input:
    #'  - iris: "Data/iris_downloaded.data"
    #'  threads: 10

The specified thread variable can then be refered to by name in our R script: :code:`snakemake@threads`

.. _snakemake-features:

Snakemake special features
--------------------------

Use following addenda to :code:`snakemake` CLI:

--dag
    Construct the directed acyclic graph of the current snakemake workflow and display as svg.

There are also some special rules that are not getting executed as a part of the usual workflow which can be run separately. Consult
:code:`.wBuild/wBuild.snakefile` in your project to find out more.

.. _rules for Snakemake: http://snakemake.readthedocs.io/en/stable/snakefiles/rules.html

.. _publishing-the-output:

Publishing the output
---------------------

Snakemake renders your project, including script text and their outputs, to a nice viewable *structure of HTML files*. You can
specify the output path by putting/changing the htmlOutputPath value inside the :ref:`configuration <configuration-file>` file found
in the root directory of your wBuild-initiated project. Your HTML gets output to :code:`Output/html` by default.

There is also a way to automatically **fetch your output to a webserver**: typing :code:`snakemake publish` copies the whole HTML output directory
to the directory specified in **projectWebDir** parameter in the :ref:`configuration file <configuration-file>`.

Markdown
--------

No need to create a separate Markdown file to describe the analysis - with wBuild you can do it right in your render
output using :code:`#'` at the beginning of the line, an then just usual MD syntax!

.. _configuration-file:

Configuration file
------------------

:code:`wbuild.yaml` file that is found in the root directory of the project stands for the configuration file of wBuild.
In this file you can adjust various properties of wBuild workflow:

.. _html-output-path:

htmlOutputPath
    This value specifies the `relative` path where your HTML output will land. *More precisely*, it is a `prefix to output file`
    of any Snakemake rule that is generated by wBuild. Default is :code:`Output/html`.

processedDataPath
    `Relative` path to the data output directory. Default is :code:`Output/ProcessedData`

scriptsPath
    `Relative` path to the root Scripts directory.

projectWebDir
    Path to the output directory for :code:`snakemake publish`.

**IMPORTANT**: Please, do not remove any key-value pairs from it or move this file *unless you know what you are doing*.

.. _use-placeholders:

Placeholders
------------

Placeholders provide the ability to refer to your current position in your system's filepath with a pair of letters instead
of absolute, relative paths. It's best shown in an example:

.. code-block:: md

    #' wb:
    #'  input:
    #'  - iris: "Data/{wbP}/iris.RDS"
    #'  output:
    #'  - pca: " {wbPD_P}/pca.RDS"

Here, we use :code:`wbP` for the name of the current project (say, Analysis01) and :code:`wbPD_P` for the name of the
output directory for processed data slash project name, say :code:`Output/ProcessedData/Analysis01`.

Here is the conscise list of the placeholders:

wbPD
    <output directory for processed data>, e.g. :code:`Output/ProcessedData`

wbP
    <current project>, e.g.  :code:`Analysis1`

wbPP
    <subfolder name>, e.g. :code:`020_InputOutput`

wbPD_P
    <output directory for processed data>/<current project>, e.g. :code:`Output/ProcessedData/Analysis1`

wbPD_PP
    <output directory for processed data>/<current project>/<subfolder name>, e.g. :code:`Output/ProcessedData/Analysis1/020_InputOutput`


.. _script-mapping:

Script mapping
--------------

This advanced feature allows you to use the same script to analyse the similarly structured data as a part of various
subprojects.

It all begins with a configure file :code:`scriptsMapping.wb` in the root directory of your project. There, you put a YAML *list of* YAML formatted **dictionaries** with two keys:

src
    A **YAML list** of *file* paths to create links from.
dst
    A **YAML list** of **directories** paths to put file links *into*.

Running :code:`snakemake mapScripts` then creates symbolic links for *all the 'src' files* in any of *'dst' directories*.

.. note:

    Give only paths *without* Scripts directory name - Scripts path will automatically be taken from
    :ref:`configuration file <configuration-file>` under key :code:`scriptsPath`.

Below is an example of a proper :code:`scriptsMapping.wb` file:

.. code-block:: yaml

  - src:
    - _Template/preprocessData.R
    - _Template/PCAoutliers.R
    dst:
    - Principal_Analysis/allIntensities
    - Principal_Analysis/withoutFamilies
    - Principal_Analysis/withoutReplicates
    - Principal_Analysis/withoutReplicatesAndFamilies

Here, we map two scripts, :code:`preprocessData.R` and :code:`PCAoutliers.R`, to be in each of the four projects of :code:`Principal_Analysis`. :ref:`Placeholders <use-placeholders>` then do their thing to speak to the right :code:`ProcessedData` sub-directories, based on the current subproject.


.. _subindex:

HTML Subindex
-------------

For subdirectories under the :code:`Scripts/` directory you can also create a separate HTML index file.
This is particularly useful when you have a larger, more modular workflow and you want to view the results of one module
as soon as they have successfully finished.

In order to create a subindex, you need to create a new rule in your :code:`Snakefile`.

.. note::

    The subdirectory path has to be within the script directory so that all HTML pages get rendered correctly.


Here is an example from the Demo project.

.. code-block:: python


    from wbuild.createIndex import createIndexRule, ci

    subdir = "Scripts/Analysis1/010_BasicInput/"
    index_name = "Analysis1_BasicInput"
    input, index_file, graph_file, _ = createIndexRule(scriptsPath=subdir, index_name=index_name)

    rule subIndex:
        input: input
        output:
            index = index_file,
            graph = graph_file
        run:
            # 1. create the index file
            ci(subdir, index_name)
            # 2. create the dependency graph
            shell("snakemake --rulegraph {output.index} | dot -Tsvg -Grankdir=LR > {output.graph}")

The :code:`wbuild.createIndex.createIndexRule()` function takes in the relative subdirectory path and an index name,
which is prepended to the index HTML file.
In this example, the HTML index file is called :code:`Analysis1_BasicInput_index.html` under the :code:`htmlOutputPath`.
The function returns a list of all HTML output files, the index file name, the dependency graph file name and the
readme HTML file name.

Using this information, you can assemble your rule, where the HTML file list is the input and the output is the index
file name.
You need to call the :code:`wbuild.createIndex.ci()` function to write the index HTML file.
You should also include the instructions to generate your dependency graph file.
The standard way is to use the snakemake option :code:`--rulegraph` to create a graph of all dependencies of the index file.
This gives you a :code:`graphviz` output that you can pipe into an the dependency graph file that you obtained from
:code:`wbuild.createIndex.createIndexRule()`.
Optionally, you can also use the :code:`--dag` option, which gives you the complete job graph.
