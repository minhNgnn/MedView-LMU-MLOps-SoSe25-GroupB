import os

from invoke import task


@task
def conda(ctx, name: str = "health-care"):
    ctx.run(f"conda env create -f environment.yml", echo=True)
    ctx.run(f"source ~/.bashrc", echo=True)
    ctx.run(f"conda init", echo=True)


@task
def train(ctx):
    ctx.run("train")
