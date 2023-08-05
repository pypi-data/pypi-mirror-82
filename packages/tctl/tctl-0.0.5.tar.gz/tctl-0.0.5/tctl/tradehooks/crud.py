#!/usr/bin/env python

import click
from .. import utils
from .. import inputs
from .. import remote
import ujson as json
import yaml

from pathlib import Path

import pandas as pd
pd.options.display.float_format = '{:,}'.format


def tradehooks_list(options):
    data = remote.api.get("/tradehooks")

    if options.get("raw"):
        if not data:
            click.echo("\n[]")
        else:
            click.echo(utils.to_json(data))
        return

    if not data:
        click.echo("\nNo Tradehooks found.")
        return

    table_data = []
    for item in data:
        table_data.append({
            # "name": item["tradehook"],
            "tradehook_id": item["tradehook_id"],
            "comment": item["comment"],
            "strategies": len(item["strategies"]),
            # "assets": len(item["assets"]),
            "invocations": "{:,.0f}".format(item["invocations"]),
            "days": item["rule"]["schedule"]["on_days"],
            # "exchange": item["rule"]["schedule"]["exchange"],
            "session": item["rule"]["schedule"]["exchange"] + ": " +
                        item["rule"]["schedule"]["session"]["open"] +
                        " to " + item["rule"]["schedule"]["session"]["close"],
            "timing": item["rule"]["schedule"]["timing"],
        })
    click.echo(utils.to_table(table_data))


def tradehook_info(options):
    data = remote.api.get("/tradehook/{tradehook}".format(
        tradehook=options.first("tradehook")))

    if options.get("raw"):
        click.echo(utils.to_json(data))
        return

    data = {
        "name": data["tradehook"],
        "tradehook_id": data["tradehook_id"],
        "comment": data["comment"],
        "strategies": len(data["strategies"]),
        "assets": len(data["assets"]),
        "invocations": "{:,.0f}".format(data["invocations"]),
        "days": data["rule"]["schedule"]["on_days"],
        "exchange": data["rule"]["schedule"]["exchange"],
        "session": data["rule"]["schedule"]["session"]["open"] +
                    " to " + data["rule"]["schedule"]["session"]["close"],
        "timing": data["rule"]["schedule"]["timing"],
    }

    df = pd.DataFrame([data])
    df.columns = [col.replace("_", " ").title() for col in df.columns]
    click.echo(utils.to_table(df.T, showindex=True, showheaders=False))


def tradehook_create(options, from_update=False):
    strategies = {}
    supported_strategies = remote.api.get("/strategies")
    for strategy in supported_strategies:
        strategies[strategy['name']] = strategy["strategy_id"]

    click.echo("")
    name = ""
    if from_update:
        name = inputs.text("Tradehook name [{s}]".format(
            s=options.first("tradehook")))
    else:
        while name == "":
            name = inputs.text("Tradehook name")

    config_file = inputs.path(
        "Path to Tradehook configuration file", validator="file")

    selected_strategies = inputs.checkboxes(
        "Attach to strategy/ies (optional, can be done later)", list(strategies.keys()))

    # if not selected_strategies:
    #     click.echo(click.style("\nFAILED", fg="red"))
    #     click.echo("Tradehook *must* be associated with at least one strategy.")

    strategies = [s for n, s in strategies.items() if n in selected_strategies]

    payload = {}
    if ".json" in config_file:
        with open(Path(config_file)) as f:
            payload = json.load(f)
    else:
        with open(Path(config_file)) as f:
            payload = yaml.load(f, Loader=yaml.SafeLoader)

    if not payload:
        click.echo(click.style("\nFAILED", fg="red"))
        click.echo("Tradehook configuration file appears to be empty.")

    if strategies:
        payload["strategies"] = strategies
    payload["name"] = name
    payload["comment"] = inputs.text("Comment (optional)")

    if from_update:
        return payload
    data = remote.api.post("/tradehooks", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data))
        return

    utils.success_response(
        f"The Tradehook account `{name}` was added to your account.")
    if strategies:
        click.echo("The Tradehook was attached to:")
    click.echo("  - "+"\n  - ".join(strategies))


def tradehook_update(options):
    name = options.first("tradehook")

    payload = tradehook_create(options, from_update=True)
    if payload["name"] == "":
        tradehook = remote.api.get("/tradehook/{tradehook}".format(
            tradehook=options.first("tradehook")))
        payload["name"] = tradehook["tradehook"]

    data = remote.api.patch(
        f"/tradehook/{name}", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data))
        return

    utils.success_response(
        f"The tradehook `{name}` was updated successfully. It's now attached to:")
    click.echo("  - "+"\n  - ".join(payload["strategies"]))



def tradehook_attach(options):
    tradehook = options.first("tradehook")
    data = remote.api.get("/tradehook/{tradehook}".format(
        tradehook=tradehook))

    payload = {
        "name": data["tradehook"],
        "comment": data["comment"],
        "strategies": data["strategies"],
        "when": {
            "schedule": data["rule"]["schedule"]
        },
        "what": {
            "assets": data["assets"],
            "bar": data["lookback_resolution"],
            "history": data["lookback_history"]
        }
    }

    strategy = options.get("strategy")
    if strategy:
        strategy = strategy[0]
        payload["strategies"].append(strategy)
    else:
        strategies = {}
        supported_strategies = remote.api.get("/strategies")
        for strategy in supported_strategies:
            strategies[strategy['name']] = strategy["strategy_id"]

        selected_strategies = inputs.checkboxes(
            "Attach to strategy(ies)", list(strategies.keys()))

        for n, s in strategies.items():
            if n in selected_strategies:
                data["strategies"].append(s)

    payload["strategies"] = list(set(data["strategies"]))

    if not payload["strategies"]:
        click.echo(click.style("\nFAILED", fg="red"))
        click.echo("Select at least one strategy.")

    data = remote.api.patch(
        f"/tradehook/{tradehook}/strategies", json=payload)

    if options.get("raw"):
        click.echo(utils.to_json(data))
        return

    utils.success_response(
        f"The tradehook account `{tradehook}` was successfully attached to:")
    click.echo("  - "+"\n  - ".join(payload["strategies"]))



def tradehook_delete(options):
    tradehook = options.first("tradehook")
    remote.api.delete("/tradehook/{tradehook}".format(
        tradehook=options.first("tradehook")))

    utils.success_response(
        f"The tradehook `{tradehook}` was removed from your account")
