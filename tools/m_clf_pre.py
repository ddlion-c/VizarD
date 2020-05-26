import click
import argparse
import sys
import os
import pickle
import numpy as np
import pandas as pd
import glob
import click

pd.set_option('mode.chained_assignment', None)

DATA_DIR = ''
CC_FILE_NAME = 'actual.csv'
RN_FILE_NAME = 'training.csv'
PRD_FILE_NAME = 'prepared.csv'
LB_COL = 'label'
RN_DIC = {'user_accepted': LB_COL}


@click.group()
def cli():
    pass

@cli.command(name='concat')
@click.argument('path', type=click.Path(exists=True))
def csv_concat(path):
    li = []
    all_files = glob.glob(path + "/*.csv")
    print(all_files)
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)
    df = pd.concat(li, axis=0, ignore_index=True)
    df = df.loc[(df['sport'] != 53) & (df['dport'] != 53) \
                & (df['p_count_f'] > 1) & (df['p_count_b'] > 1)]

    print(df.shape)
    df.to_csv(CC_FILE_NAME, index=False)

@cli.command(name='rename')
@click.argument('file', type=click.Path(exists=True))
def col_rename(file):
    df = pd.read_csv(file, index_col=0)
    df.rename(columns=RN_DIC, inplace=True)
    # Drop rows with empty labels
    df.dropna(subset=[LB_COL], inplace=True)
    print(df.shape)
    df.to_csv(RN_FILE_NAME, index=False)

@cli.command(name='clear')
@click.argument('file', type=click.Path(exists=True))
def empt_label(file):
    df = pd.read_csv(file)
    df[LB_COL] = np.nan
    df.to_csv(PRD_FILE_NAME, index=False)


if __name__ == "__main__":
    cli()
