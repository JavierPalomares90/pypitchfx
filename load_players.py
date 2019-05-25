import feather
def load_players():
    path = "data/py_players.feather"
    df = feather.read_dataframe(path)


def main():
    load_players()

if __name__=="__main__":
    main()
