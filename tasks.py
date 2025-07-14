from invoke import task
import os

@task
def git(ctx, message):
    ctx.run(f"git add .")
    ctx.run(f"git commit -m '{message}'")
    ctx.run(f"git push")

@task
def conda(ctx, name: str = "health-care"):
    ctx.run(f"conda env create -f environment.yml", echo=True)
    
    ctx.run(f"source ~/.bashrc", echo=True)
    ctx.run(f"conda init", echo=True)
    ctx.run(f"conda activate {name}", echo=True)
    ctx.run(f"pip install -e .", echo=True)

@task
def train(ctx):
    ctx.run("train")