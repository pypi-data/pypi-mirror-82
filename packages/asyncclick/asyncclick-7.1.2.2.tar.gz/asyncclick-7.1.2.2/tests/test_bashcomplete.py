# -*- coding: utf-8 -*-
import pytest

import asyncclick as click
from asyncclick._bashcomplete import get_choices
import pytest


async def choices_without_help(cli, args, incomplete):
    completions = await get_choices(cli, "dummy", args, incomplete)
    return [c[0] for c in completions]


async def choices_with_help(cli, args, incomplete):
    return list(await get_choices(cli, "dummy", args, incomplete))


@pytest.mark.anyio
async def test_single_command():
    @click.command()
    @click.option("--local-opt")
    def cli(local_opt):
        pass

    assert await choices_without_help(cli, [], "-") == ["--local-opt"]
    assert await choices_without_help(cli, [], "") == []


@pytest.mark.anyio
async def test_boolean_flag():
    @click.command()
    @click.option("--shout/--no-shout", default=False)
    def cli(local_opt):
        pass

    assert await choices_without_help(cli, [], "-") == ["--shout", "--no-shout"]


@pytest.mark.anyio
async def test_multi_value_option():
    @click.group()
    @click.option("--pos", nargs=2, type=float)
    def cli(local_opt):
        pass

    @cli.command()
    @click.option("--local-opt")
    def sub(local_opt):
        pass

    assert await choices_without_help(cli, [], "-") == ["--pos"]
    assert await choices_without_help(cli, ["--pos"], "") == []
    assert await choices_without_help(cli, ["--pos", "1.0"], "") == []
    assert await choices_without_help(cli, ["--pos", "1.0", "1.0"], "") == ["sub"]


@pytest.mark.anyio
async def test_multi_option():
    @click.command()
    @click.option("--message", "-m", multiple=True)
    def cli(local_opt):
        pass

    assert await choices_without_help(cli, [], "-") == ["--message", "-m"]
    assert await choices_without_help(cli, ["-m"], "") == []


@pytest.mark.anyio
async def test_small_chain():
    @click.group()
    @click.option("--global-opt")
    def cli(global_opt):
        pass

    @cli.command()
    @click.option("--local-opt")
    def sub(local_opt):
        pass

    assert await choices_without_help(cli, [], "") == ["sub"]
    assert await choices_without_help(cli, [], "-") == ["--global-opt"]
    assert await choices_without_help(cli, ["sub"], "") == []
    assert await choices_without_help(cli, ["sub"], "-") == ["--local-opt"]


@pytest.mark.anyio
async def test_long_chain():
    @click.group("cli")
    @click.option("--cli-opt")
    def cli(cli_opt):
        pass

    @cli.group("asub")
    @click.option("--asub-opt")
    def asub(asub_opt):
        pass

    @asub.group("bsub")
    @click.option("--bsub-opt")
    def bsub(bsub_opt):
        pass

    COLORS = ["red", "green", "blue"]

    def get_colors(ctx, args, incomplete):
        for c in COLORS:
            if c.startswith(incomplete):
                yield c

    def search_colors(ctx, args, incomplete):
        for c in COLORS:
            if incomplete in c:
                yield c

    CSUB_OPT_CHOICES = ["foo", "bar"]
    CSUB_CHOICES = ["bar", "baz"]

    @bsub.command("csub")
    @click.option("--csub-opt", type=click.Choice(CSUB_OPT_CHOICES))
    @click.option("--csub", type=click.Choice(CSUB_CHOICES))
    @click.option("--search-color", autocompletion=search_colors)
    @click.argument("color", autocompletion=get_colors)
    def csub(csub_opt, color):
        pass

    assert await choices_without_help(cli, [], "-") == ["--cli-opt"]
    assert await choices_without_help(cli, [], "") == ["asub"]
    assert await choices_without_help(cli, ["asub"], "-") == ["--asub-opt"]
    assert await choices_without_help(cli, ["asub"], "") == ["bsub"]
    assert await choices_without_help(cli, ["asub", "bsub"], "-") == ["--bsub-opt"]
    assert await choices_without_help(cli, ["asub", "bsub"], "") == ["csub"]
    assert await choices_without_help(cli, ["asub", "bsub", "csub"], "-") == [
        "--csub-opt",
        "--csub",
        "--search-color",
    ]
    assert (
        await choices_without_help(cli, ["asub", "bsub", "csub", "--csub-opt"], "")
        == CSUB_OPT_CHOICES
    )
    assert await choices_without_help(cli, ["asub", "bsub", "csub"], "--csub") == [
        "--csub-opt",
        "--csub",
    ]
    assert (
        await choices_without_help(cli, ["asub", "bsub", "csub", "--csub"], "")
        == CSUB_CHOICES
    )
    assert await choices_without_help(cli, ["asub", "bsub", "csub", "--csub-opt"], "f") == [
        "foo"
    ]
    assert await choices_without_help(cli, ["asub", "bsub", "csub"], "") == COLORS
    assert await choices_without_help(cli, ["asub", "bsub", "csub"], "b") == ["blue"]
    assert await choices_without_help(
        cli, ["asub", "bsub", "csub", "--search-color"], "een"
    ) == ["green"]


@pytest.mark.anyio
async def test_chaining():
    @click.group("cli", chain=True)
    @click.option("--cli-opt")
    @click.argument("arg", type=click.Choice(["cliarg1", "cliarg2"]))
    def cli(cli_opt, arg):
        pass

    @cli.command()
    @click.option("--asub-opt")
    def asub(asub_opt):
        pass

    @cli.command(help="bsub help")
    @click.option("--bsub-opt")
    @click.argument("arg", type=click.Choice(["arg1", "arg2"]))
    def bsub(bsub_opt, arg):
        pass

    @cli.command()
    @click.option("--csub-opt")
    @click.argument("arg", type=click.Choice(["carg1", "carg2"]), default="carg1")
    def csub(csub_opt, arg):
        pass

    assert await choices_without_help(cli, [], "-") == ["--cli-opt"]
    assert await choices_without_help(cli, [], "") == ["cliarg1", "cliarg2"]
    assert await choices_without_help(cli, ["cliarg1", "asub"], "-") == ["--asub-opt"]
    assert await choices_without_help(cli, ["cliarg1", "asub"], "") == ["bsub", "csub"]
    assert await choices_without_help(cli, ["cliarg1", "bsub"], "") == ["arg1", "arg2"]
    assert await choices_without_help(cli, ["cliarg1", "asub", "--asub-opt"], "") == []
    assert await choices_without_help(
        cli, ["cliarg1", "asub", "--asub-opt", "5", "bsub"], "-"
    ) == ["--bsub-opt"]
    assert await choices_without_help(cli, ["cliarg1", "asub", "bsub"], "-") == ["--bsub-opt"]
    assert await choices_without_help(cli, ["cliarg1", "asub", "csub"], "") == [
        "carg1",
        "carg2",
    ]
    assert await choices_without_help(cli, ["cliarg1", "bsub", "arg1", "csub"], "") == [
        "carg1",
        "carg2",
    ]
    assert await choices_without_help(cli, ["cliarg1", "asub", "csub"], "-") == ["--csub-opt"]
    assert await choices_with_help(cli, ["cliarg1", "asub"], "b") == [("bsub", "bsub help")]


@pytest.mark.anyio
async def test_argument_choice():
    @click.command()
    @click.argument("arg1", required=True, type=click.Choice(["arg11", "arg12"]))
    @click.argument("arg2", type=click.Choice(["arg21", "arg22"]), default="arg21")
    @click.argument("arg3", type=click.Choice(["arg", "argument"]), default="arg")
    def cli():
        pass

    assert await choices_without_help(cli, [], "") == ["arg11", "arg12"]
    assert await choices_without_help(cli, [], "arg") == ["arg11", "arg12"]
    assert await choices_without_help(cli, ["arg11"], "") == ["arg21", "arg22"]
    assert await choices_without_help(cli, ["arg12", "arg21"], "") == ["arg", "argument"]
    assert await choices_without_help(cli, ["arg12", "arg21"], "argu") == ["argument"]


@pytest.mark.anyio
async def test_option_choice():
    @click.command()
    @click.option("--opt1", type=click.Choice(["opt11", "opt12"]), help="opt1 help")
    @click.option("--opt2", type=click.Choice(["opt21", "opt22"]), default="opt21")
    @click.option("--opt3", type=click.Choice(["opt", "option"]))
    def cli():
        pass

    assert await choices_with_help(cli, [], "-") == [
        ("--opt1", "opt1 help"),
        ("--opt2", None),
        ("--opt3", None),
    ]
    assert await choices_without_help(cli, [], "--opt") == ["--opt1", "--opt2", "--opt3"]
    assert await choices_without_help(cli, [], "--opt1=") == ["opt11", "opt12"]
    assert await choices_without_help(cli, [], "--opt2=") == ["opt21", "opt22"]
    assert await choices_without_help(cli, ["--opt2"], "=") == ["opt21", "opt22"]
    assert await choices_without_help(cli, ["--opt2", "="], "opt") == ["opt21", "opt22"]
    assert await choices_without_help(cli, ["--opt1"], "") == ["opt11", "opt12"]
    assert await choices_without_help(cli, ["--opt2"], "") == ["opt21", "opt22"]
    assert await choices_without_help(cli, ["--opt1", "opt11", "--opt2"], "") == [
        "opt21",
        "opt22",
    ]
    assert await choices_without_help(cli, ["--opt2", "opt21"], "-") == ["--opt1", "--opt3"]
    assert await choices_without_help(cli, ["--opt1", "opt11"], "-") == ["--opt2", "--opt3"]
    assert await choices_without_help(cli, ["--opt1"], "opt") == ["opt11", "opt12"]
    assert await choices_without_help(cli, ["--opt3"], "opti") == ["option"]

    assert await choices_without_help(cli, ["--opt1", "invalid_opt"], "-") == [
        "--opt2",
        "--opt3",
    ]


@pytest.mark.anyio
async def test_option_and_arg_choice():
    @click.command()
    @click.option("--opt1", type=click.Choice(["opt11", "opt12"]))
    @click.argument("arg1", required=False, type=click.Choice(["arg11", "arg12"]))
    @click.option("--opt2", type=click.Choice(["opt21", "opt22"]))
    def cli():
        pass

    assert await choices_without_help(cli, ["--opt1"], "") == ["opt11", "opt12"]
    assert await choices_without_help(cli, [""], "--opt1=") == ["opt11", "opt12"]
    assert await choices_without_help(cli, [], "") == ["arg11", "arg12"]
    assert await choices_without_help(cli, ["--opt2"], "") == ["opt21", "opt22"]
    assert await choices_without_help(cli, ["arg11"], "--opt") == ["--opt1", "--opt2"]
    assert await choices_without_help(cli, [], "--opt") == ["--opt1", "--opt2"]


@pytest.mark.anyio
async def test_boolean_flag_choice():
    @click.command()
    @click.option("--shout/--no-shout", default=False)
    @click.argument("arg", required=False, type=click.Choice(["arg1", "arg2"]))
    def cli(local_opt):
        pass

    assert await choices_without_help(cli, [], "-") == ["--shout", "--no-shout"]
    assert await choices_without_help(cli, ["--shout"], "") == ["arg1", "arg2"]


@pytest.mark.anyio
async def test_multi_value_option_choice():
    @click.command()
    @click.option("--pos", nargs=2, type=click.Choice(["pos1", "pos2"]))
    @click.argument("arg", required=False, type=click.Choice(["arg1", "arg2"]))
    def cli(local_opt):
        pass

    assert await choices_without_help(cli, ["--pos"], "") == ["pos1", "pos2"]
    assert await choices_without_help(cli, ["--pos", "pos1"], "") == ["pos1", "pos2"]
    assert await choices_without_help(cli, ["--pos", "pos1", "pos2"], "") == ["arg1", "arg2"]
    assert await choices_without_help(cli, ["--pos", "pos1", "pos2", "arg1"], "") == []


@pytest.mark.anyio
async def test_multi_option_choice():
    @click.command()
    @click.option("--message", "-m", multiple=True, type=click.Choice(["m1", "m2"]))
    @click.argument("arg", required=False, type=click.Choice(["arg1", "arg2"]))
    def cli(local_opt):
        pass

    assert await choices_without_help(cli, ["-m"], "") == ["m1", "m2"]
    assert await choices_without_help(cli, ["-m", "m1", "-m"], "") == ["m1", "m2"]
    assert await choices_without_help(cli, ["-m", "m1"], "") == ["arg1", "arg2"]


@pytest.mark.anyio
async def test_variadic_argument_choice():
    @click.command()
    @click.option("--opt", type=click.Choice(["opt1", "opt2"]))
    @click.argument("src", nargs=-1, type=click.Choice(["src1", "src2"]))
    def cli(local_opt):
        pass

    assert await choices_without_help(cli, ["src1", "src2"], "") == ["src1", "src2"]
    assert await choices_without_help(cli, ["src1", "src2"], "--o") == ["--opt"]
    assert await choices_without_help(cli, ["src1", "src2", "--opt"], "") == ["opt1", "opt2"]
    assert await choices_without_help(cli, ["src1", "src2"], "") == ["src1", "src2"]


@pytest.mark.anyio
async def test_variadic_argument_complete():
    def _complete(ctx, args, incomplete):
        return ["abc", "def", "ghi", "jkl", "mno", "pqr", "stu", "vwx", "yz"]

    @click.group()
    def entrypoint():
        pass

    @click.command()
    @click.option("--opt", autocompletion=_complete)
    @click.argument("arg", nargs=-1)
    def subcommand(opt, arg):
        pass

    entrypoint.add_command(subcommand)

    assert await choices_without_help(entrypoint, ["subcommand", "--opt"], "") == _complete(
        0, 0, 0
    )
    assert await choices_without_help(
        entrypoint, ["subcommand", "whatever", "--opt"], ""
    ) == _complete(0, 0, 0)
    assert (
        await choices_without_help(entrypoint, ["subcommand", "whatever", "--opt", "abc"], "")
        == []
    )


@pytest.mark.anyio
async def test_long_chain_choice():
    @click.group()
    def cli():
        pass

    @cli.group()
    @click.option("--sub-opt", type=click.Choice(["subopt1", "subopt2"]))
    @click.argument(
        "sub-arg", required=False, type=click.Choice(["subarg1", "subarg2"])
    )
    def sub(sub_opt, sub_arg):
        pass

    @sub.command(short_help="bsub help")
    @click.option("--bsub-opt", type=click.Choice(["bsubopt1", "bsubopt2"]))
    @click.argument(
        "bsub-arg1", required=False, type=click.Choice(["bsubarg1", "bsubarg2"])
    )
    @click.argument(
        "bbsub-arg2", required=False, type=click.Choice(["bbsubarg1", "bbsubarg2"])
    )
    def bsub(bsub_opt):
        pass

    @sub.group("csub")
    def csub():
        pass

    @csub.command()
    def dsub():
        pass

    assert await choices_with_help(cli, ["sub", "subarg1"], "") == [
        ("bsub", "bsub help"),
        ("csub", ""),
    ]
    assert await choices_without_help(cli, ["sub"], "") == ["subarg1", "subarg2"]
    assert await choices_without_help(cli, ["sub", "--sub-opt"], "") == ["subopt1", "subopt2"]
    assert await choices_without_help(cli, ["sub", "--sub-opt", "subopt1"], "") == [
        "subarg1",
        "subarg2",
    ]
    assert await choices_without_help(
        cli, ["sub", "--sub-opt", "subopt1", "subarg1", "bsub"], "-"
    ) == ["--bsub-opt"]
    assert await choices_without_help(
        cli, ["sub", "--sub-opt", "subopt1", "subarg1", "bsub"], ""
    ) == ["bsubarg1", "bsubarg2"]
    assert await choices_without_help(
        cli, ["sub", "--sub-opt", "subopt1", "subarg1", "bsub", "--bsub-opt"], ""
    ) == ["bsubopt1", "bsubopt2"]
    assert await choices_without_help(
        cli,
        [
            "sub",
            "--sub-opt",
            "subopt1",
            "subarg1",
            "bsub",
            "--bsub-opt",
            "bsubopt1",
            "bsubarg1",
        ],
        "",
    ) == ["bbsubarg1", "bbsubarg2"]
    assert await choices_without_help(
        cli, ["sub", "--sub-opt", "subopt1", "subarg1", "csub"], ""
    ) == ["dsub"]


@pytest.mark.anyio
async def test_chained_multi():
    @click.group()
    def cli():
        pass

    @cli.group()
    def sub():
        pass

    @sub.group()
    def bsub():
        pass

    @sub.group(chain=True)
    def csub():
        pass

    @csub.command()
    def dsub():
        pass

    @csub.command()
    def esub():
        pass

    assert await choices_without_help(cli, ["sub"], "") == ["bsub", "csub"]
    assert await choices_without_help(cli, ["sub"], "c") == ["csub"]
    assert await choices_without_help(cli, ["sub", "csub"], "") == ["dsub", "esub"]
    assert await choices_without_help(cli, ["sub", "csub", "dsub"], "") == ["esub"]


@pytest.mark.anyio
async def test_hidden():
    @click.group()
    @click.option("--name", hidden=True)
    @click.option("--choices", type=click.Choice([1, 2]), hidden=True)
    def cli(name):
        pass

    @cli.group(hidden=True)
    def hgroup():
        pass

    @hgroup.group()
    def hgroupsub():
        pass

    @cli.command()
    def asub():
        pass

    @cli.command(hidden=True)
    @click.option("--hname")
    def hsub():
        pass

    assert await choices_without_help(cli, [], "--n") == []
    assert await choices_without_help(cli, [], "--c") == []
    # If the user exactly types out the hidden param, complete its options.
    assert await choices_without_help(cli, ["--choices"], "") == [1, 2]
    assert await choices_without_help(cli, [], "") == ["asub"]
    assert await choices_without_help(cli, [], "") == ["asub"]
    assert await choices_without_help(cli, [], "h") == []
    # If the user exactly types out the hidden command, complete its subcommands.
    assert await choices_without_help(cli, ["hgroup"], "") == ["hgroupsub"]
    assert await choices_without_help(cli, ["hsub"], "--h") == ["--hname"]


@pytest.mark.parametrize(
    ("args", "part", "expect"),
    [
        ([], "-", ["--opt"]),
        (["value"], "--", ["--opt"]),
        ([], "-o", []),
        (["--opt"], "-o", []),
        (["--"], "", ["name", "-o", "--opt", "--"]),
        (["--"], "--o", ["--opt"]),
    ],
)
@pytest.mark.anyio
async def test_args_with_double_dash_complete(args, part, expect):
    def _complete(ctx, args, incomplete):
        values = ["name", "-o", "--opt", "--"]
        return [x for x in values if x.startswith(incomplete)]

    @click.command()
    @click.option("--opt")
    @click.argument("args", nargs=-1, autocompletion=_complete)
    def cli(opt, args):
        pass

    assert await choices_without_help(cli, args, part) == expect
