<img width="2666" height="1332" alt="light back groundtext 1" src="https://github.com/user-attachments/assets/35280f8f-70f6-485e-a674-84fadffd8a86" />
Hi every one,
this repository archive the codes and tools that developed for FIRIA Signal modelling and analysis. note that this repository is under development right now.

# FIRIA-SMSA

**FIRIA Signal Modeling and Statistical Analysis Software**

FIRIA-SMSA is a Python-based research software package for generating FIRIA
signals, producing mixed signals, calculating RMSD matrices, summarizing RMSD
results, and performing supporting file-processing tasks. It includes a Tkinter
graphical user interface (GUI) and a collection of scripts that can also be run
individually.

## Development status

This repository contains an **alpha research release**. It is being made
available to support transparency, testing, and reproducibility while active
development continues.

The software has not yet undergone comprehensive software testing or independent
scientific validation. Review the [Known limitations](#known-limitations) section
before interpreting results. Use copies of valuable input files when running
tasks that rename, overwrite, or delete files.

## Main capabilities

- Generate FIRIA signals from frequency and IR-intensity data using Gaussian
  broadening.
- Combine multiple weighted FIRIA signals.
- Calculate RMSD matrices using original or normalized intensities.
- Summarize RMSD matrices for groups identified by `W` and `M` filename
  prefixes.
- Compare results calculated with different thresholds.
- Convert selected columns of whitespace-delimited text files to CSV.
- Extract, rename, edit, and copy batches of research files.
- Run individual tasks from a graphical interface.

## Repository layout

```text
FIRIA-SMSA/
├── Codes/
│   ├── GUI.py
│   ├── Parameters.config
│   ├── Automatic Processes/
│   ├── Single Tasks/
│   ├── Background/
│   ├── Documents/
│   └── Settings/
├── Files/
├── CHANGELOG.md
├── CITATION.cff
├── codemeta.json
└── README.md
```

## Requirements

- Python 3.10
- NumPy
- pandas
- Matplotlib
- Pillow
- Tkinter

Tkinter is normally included with standard Python installations on Windows and
macOS. On some Linux distributions it must be installed separately, for example
through the distribution's `python3-tk` package.

## Installation

1. Download or clone the repository.
2. Keep the directory layout shown above unchanged.
3. Open a terminal in the `FIRIA-SMSA` directory.
4. Create and activate a virtual environment.

Windows PowerShell:

```powershell
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install numpy pandas matplotlib pillow
```

Linux or macOS:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install numpy pandas matplotlib pillow
```

## Running the software

Start the GUI from the repository root:

```bash
python Codes/GUI.py
```

In the GUI:

1. Select `Automatic Processes` or `Single Tasks`.
2. Select the required task.
3. Review its parameters and select input and output folders where necessary.
4. Select `Save Parameters` to retain the settings or `Run` to save and execute
   the task.

An individual script may also be run directly. Quote paths that contain spaces.
For example:

```bash
python "Codes/Single Tasks/Mixed_Signal_Generator.py"
```

## Portable path handling

The location of the `Codes` directory is determined automatically from the
location of each Python file. The source code therefore does not need to be
edited when the repository is copied to another folder or computer.

Default data paths in `Codes/Parameters.config` are relative to the `Codes`
directory. For example:

```ini
input_folder = ../Files/Mixed Signal Input
output_folder = ../Files/Mixed Signal Output
```

You may replace a relative value with an absolute path by using the GUI's
`Browse` button or by editing `Parameters.config`. Both forward-slash paths and
native operating-system paths can be used on the operating system that owns the
path.

Git does not retain empty directories. If the empty directories under `Files`
are absent after cloning the repository, create the required input/output
directories or select existing directories through the GUI before running a
task.

## Configuration

Task parameters are stored in `Codes/Parameters.config`. Each section has the
same name as its corresponding Python script. The automatic threshold workflow
updates some of these values while it runs, so retain a copy of the original
configuration when exact parameter provenance is required.

### Common input formats

The current alpha scripts expect the following column names and conventions:

- `FIRIA_Signal_Generator_(Probability)`: CSV files containing
  `FREQ(CM**-1)` and `IR INTENS.` columns.
- `Mixed_Signal_Generator`: CSV files containing `x` and `y` columns. Each
  filename must contain a decimal weighting factor such as `0.8` or `5.0`.
- Original and normalized RMSD generators: CSV files containing `x` and `y`
  columns.
- `RMSD_Matrix_Average_Calculator`: matrix row and column labels beginning with
  `W` or `M` are used to define the groups.
- `TXT_to_CSV_Convertor`: whitespace-delimited text input; the current script
  extracts the second and fifth columns and names them `FREQ(CM**-1)` and
  `IR INTENS.`.
- `Matrix_Image_Generator`: CSV matrices whose first column contains the row
  labels; the current filtering expects labels beginning with `W` or `M`.

Always inspect a small test output before applying a task to a complete dataset.

## Output locations

Most tasks create a named subdirectory inside the configured output directory.
The supplied defaults use the directories under `Files`, including:

- `General Output`
- `Mixed Signal Output`
- `RMSD Matrix Output`
- `Avarage RMSD`
- `Final Result`

The spelling of existing directory and script names is retained in this alpha
release for compatibility with the current code.

## Data-safety warning

The following tasks modify the filesystem and should initially be used only on
test data or backups:

- `Delete_Contents.py` deletes all files and subdirectories inside the selected
  directory.
- `Lines_Replacement.py` overwrites matching files in place.
- The two file-renaming scripts rename files in place.
- `File_Extraction.py` copies files into one output directory and may replace an
  existing file with the same name.

Verify every configured path before selecting `Run`.

## Known limitations

- The original-intensity RMSD implementation currently assumes that compared
  files have the same row order and length. It does not align or interpolate
  values using the `x` column.
- Normalized RMSD and mixed-signal calculations rely on exact `x` values. Input
  signals should use the same sampling grid.
- Constant signals can cause division by zero during normalization.
- The Gaussian signal generator changes the number of sampled points with the
  selected Gaussian width.
- The matrix-image spacing operation is experimental in this alpha release.
- The automatic process changes `Parameters.config` and does not restore its
  previous values automatically.
- Some tasks do not yet provide comprehensive validation, rollback, progress
  reporting, or automated tests.
- GUI calculations run synchronously and the interface may appear unresponsive
  during long operations.

These limitations are planned to be addressed incrementally in later releases.

## Reproducibility recommendations

For every analysis, record:

- the software release or Git commit;
- the Python and dependency versions;
- a copy of `Parameters.config` used for the run;
- input-file checksums;
- the operating system;
- any manual preprocessing steps.

Do not use a working `Parameters.config` as the only record of a completed run,
because automatic workflows may update it.

## AI-assisted development disclosure

Generative AI tools, including OpenAI ChatGPT, were used
during the development of FIRIA-SMSA to assist with initial code layout,
debugging, portable path implementation, and documentation drafting.

All AI-assisted suggestions and generated content were reviewed and,
where necessary, revised by the human developer(s). The human author(s)
retain full responsibility for the scientific design, implementation,
testing, interpretation, and released source code. AI tools are not
considered authors or contributors to this software.


## Citation

Citation metadata is provided in `CITATION.cff` and `codemeta.json`. Replace all
placeholder author, ORCID, repository, and DOI values with the final metadata
before creating an archived release or DOI.

## Changelog

Release notes are maintained in `CHANGELOG.md`.

## License

This software published under "UP" terms. Please contact author by email (keyvanjahanfar@outlook.com) for more information.
