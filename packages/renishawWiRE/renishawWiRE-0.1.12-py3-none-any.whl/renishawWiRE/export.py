#!/usr/bin/env python
"""Export the renishaw file as plain text files
   usage:
   renishaw-export
"""

from renishawWiRE.wdfReader import WDFReader
from argparse import ArgumentParser
from pathlib import Path
import os
import sys
import numpy as np

def test_version():
    ver = sys.version_info
    if (ver.major >= 2) and (ver.minor >= 6):
        return True
    else:
        return False


def main():
    """Main program
    """

    if test_version() is False:
        print("Need at least python>=3.6. Abort!",
              file=sys.stderr)
        return 1

    parser = ArgumentParser(description=("Simple script to convert Renishaw wdf spectroscopy"
                                         " files into plain text files"))
    parser.add_argument("wdf_file",
                        help="Renishaw wdf for input")
    parser.add_argument("-o",
                        "--output",
                        default=None,
                        help=("name of the exported plain text file.\n"
                              "If not specified, use the base name of the "
                              ".wdf file"))
    parser.add_argument("-f",
                        "--format",
                        default=".csv",
                        help=("format of exported, valid values\n"
                              "\t.csv (comma-separated) \n"
                              "\t.txt (space-separated) \n"
                              "If not specified, guess from the "
                              "output file name.\n"
                              "Note: -f option is ignored when "
                              "the output file name already have an extension."))
    parser.add_argument("-p",
                        "--precision",
                        default="%.4f",
                        help=("precision of exported data."
                              " Use printf-compatible format such as %%2.4f."))

    args = parser.parse_args()
    wdf_file = Path(args.wdf_file).expanduser().resolve()
    if not wdf_file.is_file():
        print("The file {0} does not exist. Abort!".format(wdf_file.as_posix()),
              file=sys.stderr)
        return 1

    reader = WDFReader(wdf_file)
    # Output test information
    print("Your Renishaw file looks like:")
    reader.print_info()
    # handle the spectra data

    form = args.format
    # Try to guess the format from output output_filename
    if args.output is not None:
        f_ = Path(args.output).suffix
        if len(f_) > 0:
            form = f_
            print("Using format {0} from output file name".format(form))

    if form not in (".csv", ".txt"):
        print("Only .csv and .txt formats are allowed! Abort.",
              file=sys.stderr)
        return 1

    # Try to guess the
    if form == ".csv":
        delimiter = ","
    else:
        delimiter = " "
    X, header = handle_spectra(reader, delimiter=delimiter)

    # root = wdf_file.parent
    # print(root, name)
    if args.output is not None:
        output_filename = Path(args.output).with_suffix(form)
    else:
        output_filename = wdf_file.with_suffix(form)

    # output_filename = root / name
    if not output_filename.parent.is_dir():
        os.makedirs(output_filename.parent, exist_ok=True)

    print("Extracting spectra data......")
    try:
        np.savetxt(output_filename, X, fmt=args.precision,
                   delimiter=delimiter, header=header)
    except (OSError, FileExistsError):
        print("Output file {0} cannot be written. Abort!".
              format(output_filename.as_posix()),
              file=sys.stderr)
        return 1

    # There is an image associated?
    if hasattr(reader, "img"):
        print("Extracting mapping image......")
        try:
            extract_img(
                reader, output_filename=output_filename.with_suffix(".mapping.svg"))
        except (OSError, FileExistsError):
            print("Image file {0} cannot be written. Abort!".
                  format(output_filename.with_suffix(
                      ".mapping.svg").as_posix()),
                  file=sys.stderr)
            return 1

    return 0


def handle_spectra(reader, delimiter=","):
    """Function to treat single point spectrum
       return the X matrix using numpy, and header
    """
    # Wavenumber is alwa
    wn = reader.xdata
    spectra = reader.spectra
    try:
        if len(spectra.shape) == 1:
            # single point
            l_w, = spectra.shape
            assert l_w == len(wn)
            X = np.vstack([wn, spectra]).T
            header = delimiter.join(["Wavenumber", "point 1"])
        elif len(spectra.shape) == 2:
            # line or depth scan
            n_p, l_w = spectra.shape
            X = np.vstack([wn, spectra]).T
            header = delimiter.join(["Wavenumber", ] +
                                    ["point {:d}".format(i + 1)
                                     for i in range(n_p)])
        elif len(spectra.shape) == 3:
            # mapping
            r, c, l_w = spectra.shape
            assert l_w == len(wn)
            X = np.vstack([wn, spectra.reshape(r * c, l_w)]).T
            header = delimiter.join(["Wavenumber", ] +
                                    ["row {:d} column {:d}"
                                     .format(i + 1,
                                             j + 1)
                                     for i in range(r)
                                     for j in range(c)])
        else:
            print(("There seems to be something wrong "
                   "with the spectral file. Abort!"),
                  file=sys.stderr)
            return 1
    except AssertionError:
        print(("The length of wavenumber points do not "
               "match that in the spectral data. Abort!"), file=sys.stderr)

    # Sort the ndarray according to 0st
    X = X[X[:, 0].argsort()]
    return X, header


def extract_img(reader, output_filename):
    """Handle image file
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
    except ImportError as e:
        print("Error when importing matplotlib.\n{0}"
              .format(e),
              file=sys.stderr)
        return 1
    img = mpimg.imread(reader.img, format="jpg")
    img_x0, img_y0 = reader.img_origins
    img_w, img_h = reader.img_dimensions
    map_x = reader.xpos
    map_y = reader.ypos
    map_w = reader.map_info["x_span"]
    map_h = reader.map_info["y_span"]
    plt.cla()
    plt.figure(figsize=(10, 10))
    plt.imshow(img, extent=(img_x0, img_x0 + img_w,
                            img_y0 + img_h, img_y0))
    # Add rectangle for marking
    r = plt.Rectangle(xy=(map_x.min(), map_y.min()),
                      width=map_w,
                      height=map_h,
                      fill=False)
    plt.gca().add_patch(r)
    plt.xlabel("Stage X [μm]")
    plt.ylabel("Stage Y [μm]")
    plt.savefig(output_filename)


if __name__ == '__main__':
    main()
