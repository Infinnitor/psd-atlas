from argparse import ArgumentParser
import operations
from psd_tools import PSDImage
from pathlib import Path


def extract_cli(args: ArgumentParser):
    path = Path(args.target)
    assert path.exists(), f"target path '{path}' does not exist"

    dest = Path(args.dest or ".")
    assert dest.exists(), f"destination path '{path}' does not exist"

    psd = PSDImage.open(path)
    output = ""

    for name, layer in operations.extract(
        psd, ignore_background_layer=args.dispose_background
    ):
        lpath = dest.absolute().joinpath(Path(name + ".png"))
        layer.save(lpath)
        output += f"Saved as {lpath}\n"

    return output[:-1] if not args.quiet else None


def atlas_cli(args: ArgumentParser):
    path = Path(args.target)
    assert path.exists(), f"target path '{path}' does not exist"

    dest = Path(args.dest or ".")
    assert dest.exists(), f"destination path '{path}' does not exist"

    psd = PSDImage.open(path)
    num_layers = len(psd)
    image = operations.atlas(psd, ignore_background_layer=args.dispose_background)

    opath = (
        dest.absolute().joinpath(Path(path.name + ".png"))
        if dest.is_dir()
        else dest.absolute()
    )
    image.save(opath)

    return (
        f"Saved completed tilemap as {opath}, {num_layers} layers"
        if not args.quiet
        else None
    )


def parser_setup() -> ArgumentParser:
    parser = ArgumentParser(
        prog="psd-atlas",
        description="Apply operations on PSD files to transform them into sprite atlases and tilemaps",
    )

    parser.add_argument("-q", "--quiet", action="store_true", help="Less output")

    subparsers = parser.add_subparsers(title="subcommand", dest="subparser")

    extract = subparsers.add_parser("extract", help="Extract a PSD file's layers")
    extract.add_argument("target", help="The PSD file to extract from")
    extract.add_argument(
        "-C", "--dest", default=None, help="Path to output the extracted files to"
    )
    extract.add_argument(
        "-bg",
        "--dispose-background",
        action="store_true",
        help="Dispose of layers named Background (for use with Procreate PSD files)",
    )
    extract.add_argument("-q", "--quiet", action="store_true", help="Less output")
    extract.set_defaults(func=extract_cli)

    atlas = subparsers.add_parser(
        "atlas", help="Transforms PSD layers into a sprite atlas"
    )
    atlas.add_argument("target", help="The PSD file to transform from")
    atlas.add_argument(
        "-C", "--dest", default=None, help="Path to output the sprite atlas to"
    )
    atlas.add_argument(
        "-bg",
        "--dispose-background",
        action="store_true",
        help="Dispose of layers named Background (for use with Procreate PSD files)",
    )
    atlas.add_argument("-q", "--quiet", action="store_true", help="Less output")
    atlas.set_defaults(func=atlas_cli)

    return parser
