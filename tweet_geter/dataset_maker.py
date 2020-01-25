import tweepy
import pandas as pd

from tqdm import tqdm

__author__ = 'aGn'

API_KEY = "UL3Q8hMA74wRB5RykuCnCJxkm"  # TODO :: Make them parametric.
API_SECRET = "WJuehel0rp0wPq8T2MdULr3Hxb21DSZfZXI94oqkV6U0zz00Db"
ACCESS_TOKEN = "1970308164-GCFz3fDbgt95gs9VkbtHi0yzhTN9f8FjfbE2Ciw"
ACCESS_TOKEN_SECRET = "jZ1KL5BbHlqIEsM4qSqN2fmvu0vN4cIay2vQxy9mE6xgP"

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def get_tweet(id_):
    """
    Get tweet through its ID using tweepy library.
    :param id_: tweet's ID.
    :return: tweet text.
    """
    tweet = api.get_status(id_)
    tweet_text = remove_symbol(tweet.text, '#')

    return tweet_text


def remove_symbol(text, *symbols):
    """
    Remove entered symbols from text.
    :param text: Text
    :param symbols: forbidden symbols.
    :return: Text without entered symbols.
    """
    entity_prefixes = symbols
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


def clean_data(start=None, end=None):
    """
    Read raw data and clean it.
    :param start: Start point of row.
    :param end: End point of row.
    :return: cleaned data.
    """
    df = pd.read_csv('dataset/tweetIds.csv')

    if start is not None:
        if end is not None:
            df = df.iloc[start:end, :]
        else:
            '''Start to the End of file'''
            df = df.iloc[start:, :]

    print("Shape before clean: ", df.shape)
    cleaned_df = df.dropna(how='any', axis=0)
    print("Shape after clean: ", cleaned_df.shape)

    return cleaned_df


def prepare_dataset(*args, **kwargs):
    """
    Preparing dataset through getting tweets per IDs and apply hashtag remover pre-process on it.
    :return:
    """
    chunked_start = kwargs.get('chunked_start', None)
    chunked_end = kwargs.get('chunked_end', None)

    '''Generating Postfix.'''
    if chunked_start is not None:
        _start = chunked_start
        if chunked_end is not None:
            _end = chunked_end
        else:
            _end = 'end'
    else:
        _start, _end = 0, 'end'

    data = clean_data(chunked_start, chunked_end)
    progress = data.shape[0]
    progress_bar = tqdm(total=progress)
    missing_tweets = 0

    with open(f'dataset/dataset_{_start}_to_{_end}.txt', mode='a') as file_:
        for i, row in data.iterrows():
            id_ = row.iloc[0]
            emotion_ = row.iloc[1]
            try:
                file_.write(f"{id_} {get_tweet(id_)} {emotion_}")
                file_.write("\n")
                progress_bar.update()
            except Exception as exp:
                print(exp)
                missing_tweets -=- 1

    print(f"We missed {missing_tweets} of tweets.")
    progress_bar.close()


if __name__ == '__main__':  # TODO :: Temporarily
    from configuration.configs import DATA_PREPARATION
    from easydict import EasyDict as edict

    params = edict(DATA_PREPARATION)
    prepare_dataset(params.chunked_start, params.chunked_end)
